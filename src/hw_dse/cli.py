"""Command-line interface: ``hw-dse run | resume | ping | diagram``.

``hw-dse run --spec specs/dds_250msps.yaml``
    Start a run. Without ``--auto-approve`` the graph pauses at the spec
    confirmation ``interrupt()``; without ``--auto-select`` it pauses again
    to let you pick a design off the front. On a terminal you are asked
    inline; otherwise the command prints the thread id and exits, and the
    state waits in the SQLite checkpoint until ``hw-dse resume``.
``hw-dse resume --thread-id ID [--approve | --reject | --choice N|auto]``
    Continue a paused (or crashed) run from its last checkpoint.
``hw-dse ping``
    One tiny structured-output call to check a provider/model works
    (prints the parsed reply, token usage and cost; never the key).
``hw-dse diagram``
    Print the compiled graph as Mermaid (the README embeds this; a test
    fails if they drift apart).

Provider and model come from ``--provider``/``--model`` or the
environment (``HW_DSE_PROVIDER``, ``OPENROUTER_MODEL`` ...; see
``.env.example``). ``.env`` is loaded if present.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from hw_dse import accuracy_table
from hw_dse.agent.graph import build_graph
from hw_dse.agent.llm import make_llm
from hw_dse.agent.runner import REPO_ROOT, new_run_dir, sqlite_checkpointer
from hw_dse.agent.trace import Tracer

DEFAULT_DB = REPO_ROOT / "runs" / "checkpoints.sqlite"


def _load_env() -> None:
    try:
        from dotenv import load_dotenv

        load_dotenv()
    except ImportError:  # pragma: no cover
        pass


def _graph(args: argparse.Namespace, run_dir: Path) -> tuple[Any, Any]:
    tracer = Tracer(run_dir / "llm_trace.jsonl")
    llm = make_llm(args.provider, args.model, tracer=tracer, reasoning=args.reasoning)
    Path(args.db).parent.mkdir(parents=True, exist_ok=True)
    return build_graph(llm, sqlite_checkpointer(Path(args.db))), llm


def _config(args: argparse.Namespace) -> dict[str, Any]:
    return {"configurable": {"thread_id": args.thread_id, "auto_approve": getattr(args, "auto_approve", False),
                             "auto_select": getattr(args, "auto_select", False)},
            "recursion_limit": 100}


def _drive(graph: Any, config: dict[str, Any], payload: Any) -> dict[str, Any]:
    """Invoke, and keep answering interrupts on a TTY until the run ends."""
    from langgraph.types import Command

    state = graph.invoke(payload, config)
    while state.get("__interrupt__"):
        intr = state["__interrupt__"][0].value
        if not sys.stdin.isatty():
            tid = config["configurable"]["thread_id"]
            kind = intr.get("type")
            print(f"\nPaused at '{kind}' (thread {tid}).")
            if kind == "confirm_spec":
                print(intr["summary"])
                print(f"Resume with: hw-dse resume --thread-id {tid} --approve   (or --reject)")
            else:
                for row in intr["front"]:
                    print(f"  [{row['index']}] {row['key']}")
                print(f"Resume with: hw-dse resume --thread-id {tid} --choice N   (or --choice auto)")
            return state
        if intr.get("type") == "confirm_spec":
            print(intr["summary"])
            ans = input("Approve this spec? [y/N] ").strip().lower()
            resume: Any = {"approve": ans in ("y", "yes")}
        else:
            for row in intr["front"]:
                print(f"  [{row['index']}] {row['key']}")
            ans = input(f"Pick a design index (Enter = auto, rule picks {intr['auto_choice']}): ").strip()
            resume = {"choice": int(ans) if ans.isdigit() else "auto"}
        state = graph.invoke(Command(resume=resume), config)
    return state


def _print_result(state: dict[str, Any]) -> None:
    if state.get("report_path"):
        print(f"\nstatus: {state.get('status')}")
        sel = state.get("selected")
        print(f"selected: {sel['key'] if sel else None}")
        print(f"report: {state['report_path']}")


def cmd_run(args: argparse.Namespace) -> None:
    text = Path(args.spec).read_text() if args.spec else args.text
    if not text:
        raise SystemExit("give --spec FILE or --text 'natural-language request'")
    name = Path(args.spec).stem if args.spec else "adhoc"
    run_dir = new_run_dir(name)
    args.thread_id = args.thread_id or run_dir.name
    graph, _ = _graph(args, run_dir)
    print(f"run dir: {run_dir}\nthread id: {args.thread_id}")
    state = _drive(graph, _config(args), {"spec_text": text, "run_dir": str(run_dir), "seed": args.seed})
    _print_result(state)


def cmd_resume(args: argparse.Namespace) -> None:
    from langgraph.types import Command

    probe = build_graph(make_llm("fake"), sqlite_checkpointer(Path(args.db)))
    snap = probe.get_state(_config(args))
    if not snap.values:
        raise SystemExit(f"no checkpoint for thread {args.thread_id} in {args.db}")
    run_dir = Path(snap.values["run_dir"])
    graph, _ = _graph(args, run_dir)
    if args.approve or args.reject:
        payload: Any = Command(resume={"approve": bool(args.approve)})
    elif args.choice is not None:
        payload = Command(resume={"choice": int(args.choice) if args.choice.isdigit() else "auto"})
    else:
        payload = None  # crashed run: continue from the last checkpoint
    state = _drive(graph, _config(args), payload)
    _print_result(state)


class Ping(BaseModel):
    ok: bool = Field(description="always true")
    word: str = Field(description="one word naming a CORDIC architecture family")


def cmd_ping(args: argparse.Namespace) -> None:
    tracer = Tracer()
    llm = make_llm(args.provider, args.model, tracer=tracer, reasoning=args.reasoning)
    out = llm.structured(Ping, "Reply using the required structure.", "Say ok=true and name one CORDIC architecture.", node="ping")
    rec = tracer.records[-1]
    print(json.dumps({"provider": llm.provider, "model_requested": llm.model, "model_served": rec.get("model_served"),
                      "parsed": out.model_dump(), "usage": rec.get("usage"), "cost_usd": rec.get("cost_usd"),
                      "reasoning_tokens": rec.get("reasoning_tokens"), "attempts": len(tracer.records)}, indent=1))


def cmd_diagram(_: argparse.Namespace) -> None:
    print(mermaid())


def mermaid() -> str:
    return build_graph(make_llm("fake")).get_graph().draw_mermaid()


def main(argv: list[str] | None = None) -> None:
    _load_env()
    ap = argparse.ArgumentParser(prog="hw-dse", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p: argparse.ArgumentParser) -> None:
        p.add_argument("--provider", default=None, help="fake|anthropic|openai|gemini|ollama|openrouter (env HW_DSE_PROVIDER)")
        p.add_argument("--model", default=None)
        p.add_argument("--reasoning", default=None, help="OpenRouter reasoning: off|low|medium|high")
        p.add_argument("--db", default=str(DEFAULT_DB), help="SQLite checkpoint database")

    r = sub.add_parser("run")
    common(r)
    r.add_argument("--spec", help="YAML spec file")
    r.add_argument("--text", help="natural-language spec (uses the LLM intake)")
    r.add_argument("--seed", type=int, default=0)
    r.add_argument("--thread-id", default=None)
    r.add_argument("--auto-approve", action="store_true", help="skip the human spec confirmation (CI)")
    r.add_argument("--auto-select", action="store_true", help="select by the spec's rule instead of asking")
    r.set_defaults(fn=cmd_run)

    s = sub.add_parser("resume")
    common(s)
    s.add_argument("--thread-id", required=True)
    s.add_argument("--approve", action="store_true")
    s.add_argument("--reject", action="store_true")
    s.add_argument("--choice", default=None, help="front index or 'auto'")
    s.add_argument("--auto-select", action="store_true")
    s.set_defaults(fn=cmd_resume)

    p = sub.add_parser("ping")
    p.add_argument("--provider", default=None)
    p.add_argument("--model", default=None)
    p.add_argument("--reasoning", default=None)
    p.set_defaults(fn=cmd_ping)

    d = sub.add_parser("diagram")
    d.set_defaults(fn=cmd_diagram)

    args = ap.parse_args(argv)
    if args.cmd in ("run", "resume"):
        accuracy_table.preload()
    args.fn(args)


if __name__ == "__main__":
    main()
