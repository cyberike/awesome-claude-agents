#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
awesome-claude-agents/main.py
- Windows-safe UTF-8 console + file writes
- Orchestration loop: prompt -> assign tasks to role agents -> save outputs
- Uses your Problem statement as the shared context for ALL agents
"""

from __future__ import annotations

import os
import sys
import json
import time
import argparse
import datetime
import traceback
import re
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

# -----------------------------
# 0) Make stdout/stderr UTF-8 (fixes ✅ crash on Windows consoles)
# -----------------------------
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# Also hint Python to favor UTF-8 if not already set
os.environ.setdefault("PYTHONUTF8", "1")

# -----------------------------
# 1) Optional dotenv load
# -----------------------------
try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except Exception:
    # dotenv is optional; continue if not installed
    pass

# -----------------------------
# 2) Project-local imports with graceful fallbacks
# -----------------------------
def _fallback_save_agent_output(role: str, content: str, build_dir: Path) -> Path:
    """Fallback saver if save_outputs.save_agent_output not present."""
    filename = f"{role}.md"
    path = build_dir / filename
    _safe_write_text(path, content)
    return path

def _fallback_save_project_files(project_files: Dict[str, str], build_dir: Path) -> None:
    """Fallback saver if save_project_files.save_project_files not present."""
    for rel_path, text in project_files.items():
        out_path = build_dir / rel_path
        out_path.parent.mkdir(parents=True, exist_ok=True)
        _safe_write_text(out_path, text)

# Try to import repo utilities; otherwise use fallbacks
try:
    from save_outputs import save_agent_output as _repo_save_agent_output  # type: ignore
except Exception:
    _repo_save_agent_output = None

try:
    from save_project_files import save_project_files as _repo_save_project_files  # type: ignore
except Exception:
    _repo_save_project_files = None

def save_agent_output(role: str, content: str, build_dir: Path) -> Path:
    if _repo_save_agent_output is not None:
        # Ensure repo saver writes UTF-8; if not, our text is already sanitized
        return _repo_save_agent_output(role, _strip_emojis_for_files(content), build_dir)
    return _fallback_save_agent_output(role, _strip_emojis_for_files(content), build_dir)

def save_project_files(project_files: Dict[str, str], build_dir: Path) -> None:
    if _repo_save_project_files is not None:
        # Sanitize each file’s text
        sanitized = {k: _strip_emojis_for_files(v) for k, v in project_files.items()}
        return _repo_save_project_files(sanitized, build_dir)
    return _fallback_save_project_files(
        {k: _strip_emojis_for_files(v) for k, v in project_files.items()}, build_dir
    )

# Agent loader
try:
    from agent_loader import call_agent  # type: ignore
except Exception as e:
    raise RuntimeError(
        "Could not import agent_loader.call_agent. Please ensure your repo structure is intact."
    ) from e

# -----------------------------
# 3) Emoji handling for file outputs only
# -----------------------------
# Keep console pretty, but for files we strip high-plane emojis that break some Windows tools
_EMOJI_RE = re.compile(r"[\U00010000-\U0010FFFF]")

def _strip_emojis_for_files(text: str) -> str:
    return _EMOJI_RE.sub("", text)

def _safe_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)

# -----------------------------
# 4) Build directory helpers
# -----------------------------
def make_build_dir(root: Path) -> Path:
    ts = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    build_dir = root / "build" / f"superbuild_{ts}"
    build_dir.mkdir(parents=True, exist_ok=True)
    return build_dir

# -----------------------------
# 5) Role plan
# -----------------------------
ROLE_PLAN = {
    "ml_engineer": {
        "display": "ML Engineer",
        "task_hint": "Model strategy & quantization plan",
    },
    "voice_interface_developer": {
        "display": "Voice Interface Developer",
        "task_hint": "Offline voice UX & pipeline",
    },
    "ui_ux_developer": {
        "display": "UI/UX Developer",
        "task_hint": "Embedded UI flows & wireframes",
    },
    "devops_engineer": {
        "display": "DevOps Engineer",
        "task_hint": "Reproducible output packaging (Dockerfiles, compose, Makefile, CI hints)",
    },
}

# -----------------------------
# 6) Agent call with retries
# -----------------------------
def run_agent_with_retries(
    role_name: str,
    problem_statement: str,
    build_dir: Path,
    retries: int = 3,
    retry_sleep: float = 0.8,
) -> Tuple[Optional[str], Optional[Dict[str, str]]]:
    """
    Returns:
      (markdown_output, optional_project_files_dict)
    Agent may return:
      - plain string (markdown) OR
      - dict with keys {"markdown": str, "files": {relpath: text, ...}}
    """
    role_meta = ROLE_PLAN[role_name]
    display = role_meta["display"]
    task_hint = role_meta["task_hint"]

    # Shared prompt payload handed to the agent
    agent_input = {
        "role": display,
        "task_hint": task_hint,
        "context": problem_statement,
        "deliverables": [
            "A concise but actionable writeup in Markdown",
            "If code/config files are needed, return them as {relpath: content}",
        ],
        "return_schema": {
            "markdown": "string - required - agent report in Markdown",
            "files": "object - optional - mapping of relative file path -> file text",
        },
    }

    last_err = None
    for attempt in range(1, retries + 1):
        try:
            print(f"🛠 {display}: Working on task -> {task_hint}")
            result = call_agent(role_name, agent_input)  # user’s repo function
            # Normalize results
            md: Optional[str] = None
            files: Optional[Dict[str, str]] = None

            if isinstance(result, str):
                md = result
            elif isinstance(result, dict):
                md = result.get("markdown")
                files = result.get("files")
            else:
                md = str(result)

            if md:
                out_path = save_agent_output(role_name, md, build_dir)
                print(f"💾 Saved: {out_path}")
            if files:
                save_project_files(files, build_dir)
                print(f"📦 Project files saved for {display}")

            print(f"✅ {role_name} Done")
            return md, files

        except Exception as e:
            last_err = e
            print(
                f"[Retry {attempt}/{retries}] call_agent failed for '{role_name}': "
                f"{e.__class__.__name__}: {e}"
            )
            if attempt < retries:
                time.sleep(retry_sleep)

    # If we reach here, all retries failed
    print(f"❌ {role_name} error: {last_err}")
    # Also write a debug file for postmortem
    err_path = build_dir / f"{role_name}__error.txt"
    _safe_write_text(err_path, f"{type(last_err).__name__}: {last_err}\n\n{traceback.format_exc()}")
    return None, None

# -----------------------------
# 7) CLI / interactive loop
# -----------------------------
def main() -> int:
    parser = argparse.ArgumentParser(description="Awesome Claude Agents Orchestrator")
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run a single prompt from stdin/argument and exit (non-interactive).",
    )
    parser.add_argument(
        "--task",
        type=str,
        default="",
        help="Provide a task/problem non-interactively when using --once.",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent
    build_dir = make_build_dir(repo_root)

    def prompt_for_task() -> Optional[str]:
        try:
            task = input("🧠 Enter a task for the AI team (or press Enter to exit): ").strip()
            return task if task else None
        except (EOFError, KeyboardInterrupt):
            return None

    if args.once:
        problem = args.task.strip() or prompt_for_task()
        if not problem:
            return 0
        run_full_pipeline(problem, build_dir)
        return 0

    # Interactive loop
    while True:
        problem = prompt_for_task()
        if not problem:
            break
        run_full_pipeline(problem, build_dir)

    return 0

# -----------------------------
# 8) Pipeline that actually uses YOUR problem statement
# -----------------------------
def run_full_pipeline(problem_statement: str, build_dir: Path) -> None:
    banner = f"\n=== Orchestration Start ===\nContext: {problem_statement}\nBuild: {build_dir}\n"
    print(banner)

    # Save raw context for traceability
    _safe_write_text(build_dir / "context.txt", _strip_emojis_for_files(problem_statement))

    # Run each role in order; every agent gets the SAME context
    for role in ("ml_engineer", "voice_interface_developer", "ui_ux_developer", "devops_engineer"):
        run_agent_with_retries(role, problem_statement, build_dir)

    print("\n🎉 Orchestration complete.\n")

# -----------------------------
# 9) Entrypoint
# -----------------------------
if __name__ == "__main__":
    sys.exit(main())
