#!/usr/bin/env python3
"""Deterministic release-note composer.

No LLM calls. Pulls the GitHub-generated changelog (respects .github/release.yml
label categories) via the generate-notes API, then reads the per-PR
`<!-- release-note:start -->...<!-- release-note:end -->` marker block out of
each merged PR's body to build a "### Summary" section.

Usage:
    python extract.py --repo OWNER/REPO --tag v0.2.0 --previous-tag v0.0.9

Requires: `gh` CLI authenticated, Python 3.9+.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys

NOTE_RE = re.compile(
    r"<!--\s*release-note:start\s*-->(.*?)<!--\s*release-note:end\s*-->",
    re.DOTALL,
)
BREAKING_RE = re.compile(
    r"<!--\s*release-note-breaking:start\s*-->(.*?)<!--\s*release-note-breaking:end\s*-->",
    re.DOTALL,
)
PR_LINE_RE = re.compile(r"^\*\s.*?/pull/(\d+)\s*$", re.MULTILINE)


def run_gh(args: list[str]) -> str:
    result = subprocess.run(["gh", *args], capture_output=True, text=True, check=True)
    return result.stdout


def generate_notes(repo: str, tag: str, previous_tag: str) -> str:
    out = run_gh(
        [
            "api",
            f"repos/{repo}/releases/generate-notes",
            "-f",
            f"tag_name={tag}",
            "-f",
            f"previous_tag_name={previous_tag}",
        ]
    )
    return json.loads(out)["body"]


def pr_numbers_in_order(generated_body: str) -> list[int]:
    # Only the "## What's Changed" section lists merged PRs; "## New Contributors"
    # bullets have the same "* ... /pull/N" shape and would otherwise duplicate PRs.
    whats_changed = generated_body.split("## New Contributors")[0]
    seen: dict[int, None] = {}
    for n in PR_LINE_RE.findall(whats_changed):
        seen[int(n)] = None
    return list(seen)


def fetch_pr_body(repo: str, number: int) -> str:
    out = run_gh(["pr", "view", str(number), "--repo", repo, "--json", "body"])
    return json.loads(out)["body"] or ""


def extract_note(body: str) -> str | None:
    m = NOTE_RE.search(body)
    if not m:
        return None
    text = m.group(1).strip()
    if not text or text.lower() == "internal":
        return None
    return " ".join(text.split())


def extract_breaking(body: str) -> str | None:
    m = BREAKING_RE.search(body)
    if not m:
        return None
    text = m.group(1).strip()
    if not text:
        return None
    return " ".join(text.split())


def compose(repo: str, tag: str, previous_tag: str) -> str:
    generated = generate_notes(repo, tag, previous_tag)
    numbers = pr_numbers_in_order(generated)

    summary_lines = []
    breaking_lines = []
    for n in numbers:
        body = fetch_pr_body(repo, n)
        note = extract_note(body)
        if note:
            summary_lines.append(f"- {note} (#{n})")
        breaking = extract_breaking(body)
        if breaking:
            breaking_lines.append(f"- {breaking} (#{n})")

    # Strip the HTML config comment GitHub prepends; keep What's Changed + Full Changelog.
    body = re.sub(r"^<!--.*?-->\n\n?", "", generated, flags=re.DOTALL)

    whats_changed, _, rest = body.partition("## New Contributors")
    if not rest:
        whats_changed, _, rest = body.partition("**Full Changelog**")
        full_changelog = "**Full Changelog**" + rest
    else:
        # Drop New Contributors section; keep Full Changelog line from what follows it.
        fc_match = re.search(r"\*\*Full Changelog\*\*.*", rest, re.DOTALL)
        full_changelog = fc_match.group(0) if fc_match else ""

    parts = [whats_changed.rstrip()]

    if breaking_lines:
        parts.append("### Breaking Changes\n\n" + "\n".join(breaking_lines))

    if summary_lines:
        parts.append("### Summary\n\n" + "\n".join(summary_lines))

    parts.append(full_changelog.strip())

    return "\n\n".join(p for p in parts if p) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, help="OWNER/REPO")
    parser.add_argument("--tag", required=True, help="the tag/release being cut")
    parser.add_argument(
        "--previous-tag",
        required=True,
        help="the previous tag FOR THIS PACKAGE (not just 'the last release')",
    )
    args = parser.parse_args()

    print(compose(args.repo, args.tag, args.previous_tag))
    return 0


if __name__ == "__main__":
    sys.exit(main())
