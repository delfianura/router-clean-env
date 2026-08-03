#!/usr/bin/env python3
"""Deterministic release-note composer.

No LLM calls, no tag required to already exist, no dependency on PR labels.

The PR range is found from the last published release's timestamp (via the
Releases API), not from local/manual git tags. "## What's Changed" is a flat
list of merged PRs, in the same order GitHub's own generated notes use — no
category subheadings. Each merged PR's body is then read for the
`<!-- release-note:start -->...<!-- release-note:end -->` marker to build a
"### Summary" section directly beneath it, one bullet per user-facing PR.
A PR whose title carries the Conventional Commit "!" (`feat!: ...`) or whose
body has a filled-in `<!-- release-note-breaking:start -->...-end -->` marker
gets its summary bullet prefixed with "**Breaking:**" instead of a separate
section.

Usage:
    python extract.py --repo OWNER/REPO --tag v0.3.2
    python extract.py --repo OWNER/REPO --tag v0.3.2 --prefix gllm_inference-v --base main

Requires: `gh` CLI authenticated, Python 3.9+.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone

NOTE_RE = re.compile(
    r"<!--\s*release-note:start\s*-->(.*?)<!--\s*release-note:end\s*-->",
    re.DOTALL,
)
BREAKING_RE = re.compile(
    r"<!--\s*release-note-breaking:start\s*-->(.*?)<!--\s*release-note-breaking:end\s*-->",
    re.DOTALL,
)

# Conventional Commit PR title: "type(scope)!: subject". Scope and "!" optional.
# The "!" is the only part we need — it's the title-level breaking-change signal.
TITLE_RE = re.compile(r"^[a-zA-Z]+(?:\([^)]*\))?(?P<bang>!)?:\s*.+$")


def run_gh(args: list[str]) -> str:
    result = subprocess.run(["gh", *args], capture_output=True, text=True, check=True)
    return result.stdout


def get_last_release(repo: str, prefix: str | None, exclude_tag: str | None = None) -> dict | None:
    """Most recently published release, optionally scoped to a package's tag prefix.

    Reads straight from the Releases API — no local git tags involved, so this
    works even in a checkout that never fetched tags.

    `exclude_tag` matters when this runs *after* the release being composed has
    already been published (e.g. a post-publish workflow reacting to the
    release you just created) — without excluding it, "most recent" would just
    find itself and produce an empty range.
    """
    releases = json.loads(run_gh(["api", f"repos/{repo}/releases", "--paginate"]))
    if prefix:
        releases = [r for r in releases if r["tag_name"].startswith(prefix)]
    if exclude_tag:
        releases = [r for r in releases if r["tag_name"] != exclude_tag]
    if not releases:
        return None
    releases.sort(key=lambda r: r["published_at"], reverse=True)
    return releases[0]


def list_merged_prs(repo: str, base: str, since: str | None) -> list[dict]:
    """Merged PRs against `base`, merged after `since` (ISO8601), oldest first."""
    out = run_gh(
        [
            "pr",
            "list",
            "--repo",
            repo,
            "--state",
            "merged",
            "--base",
            base,
            "--limit",
            "200",
            "--json",
            "number,title,mergedAt,url,author",
        ]
    )
    prs = json.loads(out)
    if since:
        since_dt = datetime.fromisoformat(since.replace("Z", "+00:00"))
        prs = [p for p in prs if datetime.fromisoformat(p["mergedAt"].replace("Z", "+00:00")) > since_dt]
    prs.sort(key=lambda p: p["mergedAt"])
    return prs


def is_breaking_title(title: str) -> bool:
    """Whether a Conventional Commit PR title carries the "!" breaking marker."""
    m = TITLE_RE.match(title.strip())
    return bool(m and m.group("bang") == "!")


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


def compose(repo: str, tag: str, base: str, prefix: str | None) -> str:
    # Excluding `tag` itself is always safe: if it doesn't exist yet (the normal,
    # pre-publish case) this filters nothing; if it already exists (a workflow
    # reacting to the release it's about to rewrite) this stops "most recent
    # release" from just finding itself and producing an empty range.
    last_release = get_last_release(repo, prefix, exclude_tag=tag)
    since = last_release["published_at"] if last_release else None
    previous_tag = last_release["tag_name"] if last_release else None

    prs = list_merged_prs(repo, base, since)

    whats_changed_lines = []
    summary_lines = []
    for pr in prs:
        n = pr["number"]
        title_breaking = is_breaking_title(pr["title"])
        whats_changed_lines.append(f"* {pr['title']} by @{pr['author']['login']} in {pr['url']}")

        body = fetch_pr_body(repo, n)
        note = extract_note(body)
        breaking = extract_breaking(body) or (note if title_breaking else None)

        if breaking:
            summary_lines.append(f"- **Breaking:** {breaking} (#{n})")
        elif note:
            summary_lines.append(f"- {note} (#{n})")

    body_parts = ["## What's Changed\n" + "\n".join(whats_changed_lines)]

    if summary_lines:
        body_parts.append("### Summary\n\n" + "\n".join(summary_lines))

    if previous_tag:
        body_parts.append(f"**Full Changelog**: https://github.com/{repo}/compare/{previous_tag}...{tag}")

    return "\n\n".join(body_parts) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo", required=True, help="OWNER/REPO")
    parser.add_argument("--tag", required=True, help="the tag/release being cut (need not exist yet)")
    parser.add_argument("--base", default="master", help="base branch PRs merge into (default: master)")
    parser.add_argument(
        "--prefix",
        default=None,
        help="package tag prefix, e.g. 'gllm_inference-v' — scopes 'last release' "
        "to that package instead of the whole monorepo. Omit for single-package repos.",
    )
    args = parser.parse_args()

    print(compose(args.repo, args.tag, args.base, args.prefix))
    return 0


if __name__ == "__main__":
    sys.exit(main())
