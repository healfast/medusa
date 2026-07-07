"""
medusa_agent.py

Local-only Medusa agent implementation.

This agent does not require API keys. It inspects the repository source and
returns helpful, deterministic responses using simple heuristics and codebase
searches. It can optionally use a local GGUF model or the Ollama CLI when
those are available.
"""

from __future__ import annotations

import os
import re
import subprocess
from typing import Any, Dict, List

from local_llm import generate_local_reply, get_default_model_path


def _classify_intent(prompt: str) -> str:
    text = (prompt or "").lower()
    if any(word in text for word in ("plan", "steps", "roadmap", "todo", "project")):
        return "planning"
    if any(word in text for word in ("code", "implement", "build", "debug", "fix", "write")):
        return "coding"
    if any(word in text for word in ("explain", "what is", "why", "how")):
        return "explanation"
    return "chat"


def _safe_project_path(path: str) -> str | None:
    repo_root = os.path.realpath(os.path.join(os.path.dirname(__file__), "."))
    candidate = os.path.realpath(os.path.join(repo_root, path))
    if os.path.commonpath([repo_root, candidate]) != repo_root:
        return None
    return candidate


def _list_project_files(max_entries: int = 500) -> str:
    repo_root = os.path.realpath(os.path.join(os.path.dirname(__file__), "."))
    entries: List[str] = []
    for dirpath, _, filenames in os.walk(repo_root):
        rel_dir = os.path.relpath(dirpath, repo_root)
        for filename in sorted(filenames):
            rel_path = os.path.normpath(os.path.join(rel_dir, filename))
            entries.append(rel_path if rel_dir != "." else filename)
            if len(entries) >= max_entries:
                break
        if len(entries) >= max_entries:
            break
    return "\n".join(entries) or "No files found in the project."


def _read_project_file(path: str) -> str:
    safe_path = _safe_project_path(path)
    if not safe_path or not os.path.isfile(safe_path):
        return f"Cannot access file: {path}. Make sure the path is inside the project."
    max_size = 200 * 1024
    if os.path.getsize(safe_path) > max_size:
        return f"File is too large to display (>{max_size} bytes)."
    try:
        with open(safe_path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except Exception as exc:
        return f"Failed to read file {path}: {exc}"


def _extract_project_path(prompt: str) -> str | None:
    patterns = [
        r"read(?: the)? file\s+[\"']?([^\"']+)[\"']?",
        r"show(?: me)?(?: the)? file\s+[\"']?([^\"']+)[\"']?",
        r"open(?: the)? file\s+[\"']?([^\"']+)[\"']?",
        r"cat\s+[\"']?([^\"']+)[\"']?",
    ]
    for pattern in patterns:
        match = re.search(pattern, prompt, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None


def _search_codebase(prompt: str, max_results: int = 5) -> str:
    """Return short excerpts from files that best match `prompt` keywords."""
    repo_root = os.path.realpath(os.path.join(os.path.dirname(__file__), "."))
    keywords = [word for word in re.findall(r"\w{3,}", prompt.lower()) if len(word) > 2]
    scores: Dict[str, int] = {}
    excerpts: Dict[str, str] = {}

    for dirpath, _, filenames in os.walk(repo_root):
        for fname in filenames:
            if fname.endswith((".pyc", ".png", ".jpg", ".jpeg", ".gif")):
                continue
            path = os.path.join(dirpath, fname)
            try:
                with open(path, "r", encoding="utf-8", errors="replace") as f:
                    text = f.read().lower()
            except Exception:
                continue
            score = sum(text.count(keyword) for keyword in keywords) if keywords else 0
            if score > 0:
                rel = os.path.relpath(path, repo_root)
                scores[rel] = score
                start = max(0, text.find(keywords[0]) - 80) if keywords else 0
                excerpt = text[start:start + 300].strip()
                excerpts[rel] = excerpt

    if not scores:
        return "No relevant project snippets found. Try a different query or ask for a file listing."

    top = sorted(scores.items(), key=lambda item: -item[1])[:max_results]
    parts = []
    for fname, score in top:
        parts.append(f"File: {fname} (score: {score})\n...{excerpts.get(fname, '')}...\n")
    return "\n".join(parts)


def generate_reply(
    prompt: str,
    history: List[Dict[str, Any]] | None = None,
    provider: str = "local",
    jailbreak: bool = False,
    **kwargs,
) -> str:
    """Local-only reply generator."""
    prompt = (prompt or "").strip()
    history = history or []

    if not prompt:
        return "Hello! I am Medusa, a local assistant that uses the repository source to help you."

    file_path = _extract_project_path(prompt)
    if "list files" in prompt.lower() or "show files" in prompt.lower() or "project files" in prompt.lower():
        return _list_project_files()
    if file_path:
        return _read_project_file(file_path)

    intent = _classify_intent(prompt)
    prefix = "[Hermes - direct] " if jailbreak else ""

    history_text = " ".join(
        str(item.get("content", "")) for item in history if isinstance(item, dict)
    ).lower()

    if "blog" in history_text and any(word in prompt.lower() for word in ["continue", "plan", "next", "step", "follow"]):
        return (
            f"{prefix}I remember you were discussing a blog project. Here's a plan to continue:\n"
            f"1. Choose a tech stack (e.g., Flask + SQLite for simplicity).\n"
            f"2. Set up models for BlogPost and User.\n"
            f"3. Create views for listing, creating, and viewing posts.\n"
            f"4. Add authentication if needed."
        )

    normalized = (provider or "").lower()
    external_names = {"claude", "claude_code", "openai", "fable", "huggingface", "venice", "omni", "ollama"}

    if normalized in external_names and normalized != "local":
        try:
            cmd = ["ollama", "run", "llama2-uncensored", prompt]
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if proc.returncode == 0 and proc.stdout:
                return f"{prefix}{proc.stdout.strip()}"
        except (FileNotFoundError, subprocess.SubprocessError):
            pass

    if normalized == "local":
        model_path = kwargs.get("model_path") or os.getenv("LOCAL_MODEL_PATH") or get_default_model_path()
        if model_path:
            try:
                llm_reply = generate_local_reply(prompt, model_path=model_path)
                if llm_reply and not llm_reply.startswith("Failed to load") and not llm_reply.startswith("Local LLM generation"):
                    return f"{prefix}{llm_reply.strip()}"
            except Exception:
                pass

    if any(keyword in prompt.lower() for keyword in ("file", "repo", "project", "function", "class", "module")):
        snippets = _search_codebase(prompt)
        return f"{prefix}I found these relevant snippets:\n\n{snippets}"

    if intent == "planning":
        return (
            f"{prefix}Here is a concise plan for '{prompt}':\n"
            "1) Define the goal and acceptance criteria.\n"
            "2) Break into small milestones.\n"
            "3) Implement the first milestone and add tests."
        )

    if intent == "coding":
        return (
            f"{prefix}Coding suggestion for '{prompt}':\n"
            "Start with a minimal reproducible example, add unit tests, and iterate. If you want, ask 'read file <path>' to show relevant source."
        )

    if intent == "explanation":
        return (
            f"{prefix}Explanation for '{prompt}':\n"
            "I'll give a short definition, a concrete example, and note tradeoffs. Ask to expand any part."
        )

    search = _search_codebase(prompt)
    if "No relevant project snippets" not in search:
        return f"{prefix}Based on the repository, here are matches:\n\n{search}"

    return f"{prefix}I can help with planning, coding, or explanations. Try asking 'list files' or 'read file README.md'."
