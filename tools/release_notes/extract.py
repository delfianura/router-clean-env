#!/usr/bin/env python3
"""Deterministic release-note composer.

No LLM calls. Uses GitHub's own `generate-notes` API (the same one behind the
"Generate release notes" button and `gh release create --generate-notes`) for
the "## What's Changed" list and "Full Changelog" link — that endpoint already
handles PR discovery, author attribution, and edge cases (co-authors, force-
pushes, etc.) robustly, so there's no reason to reimplement it.

The one thing that endpoint gets wrong by default is `previous_tag_name`: left
unset, it picks "the most recent release across the whole repo," not "the
most recent release for this package" — wrong the moment a repo has more than
one release lineage. So this script computes that tag itself (most recently
published release, optionally scoped by `--prefix`, always excluding `--tag`
itself so re-running after publish doesn't just find itself) and passes it in
explicitly.

On top of GitHub's own body, each merged PR's body is read for the
`<!-- release-note:start -->...<!-- release-note:end -->` marker to build a
"### Summary" section directly beneath it, one bullet per user-facing PR.
A PR whose title carries the Conventional Commit "!" (`feat!: ...`) or whose
body has a filled-in `<!-- release-note-breaking:start -->...-end -->` marker
gets its summary bullet prefixed with "**Breaking:**" instead of a separate
section.

Note: for "## What's Changed" to come back as a flat list with no category
subheadings, don't add a `.github/release.yml` with `changelog.categories` —
that's what triggers GitHub's own label-based grouping.

Usage:
    python extract.py --repo OWNER/REPO --tag v0.3.2
    python extract.py --repo OWNER/REPO --tag v0.3.2 --prefix gllm_inference-v

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

# Conventional Commit PR title: "type(scope)!: subject". Scope and "!" optional.
TITLE_RE = re.compile(r"^[a-zA-Z]+(?:\([^)]*\))?(?P<bang>!)?:\s*.+$")

PR_LINE_RE = re.compile(r"^\*\s.*?/pull/(\d+)\s*$", re.MULTILINE)


def run_gh(args: list[str]) -> str:
    result = subprocess.run(["gh", *args], capture_output=True, text=True, check=True)
    return result.stdout


def get_last_release(repo: str, prefix: str | None, exclude_tag: str | None = None) -> dict | None:
    """Most recently published release, optionally scoped to a package's tag prefix.

    `exclude_tag` matters when this runs *after* the release being composed has
    already been published (e.g. a workflow reacting to the tag push that just
    created it) — without excluding it, "most recent" would just find itself
    and produce an empty range.
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


def generate_notes(repo: str, tag: str, previous_tag: str | None) -> str:
    args = ["api", f"repos/{repo}/releases/generate-notes", "-f", f"tag_name={tag}"]
    if previous_tag:
        args += ["-f", f"previous_tag_name={previous_tag}"]
    out = run_gh(args)
    return json.loads(out)["body"]


def pr_numbers_in_order(generated_body: str) -> list[int]:
    # "## New Contributors" bullets have the same "* ... /pull/N" shape as the
    # "## What's Changed" PR list and would otherwise duplicate PRs.
    whats_changed = generated_body.split("## New Contributors")[0]
    seen: dict[int, None] = {}
    for n in PR_LINE_RE.findall(whats_changed):
        seen[int(n)] = None
    return list(seen)


def is_breaking_title(title: str) -> bool:
    """Whether a Conventional Commit PR title carries the "!" breaking marker."""
    m = TITLE_RE.match(title.strip())
    return bool(m and m.group("bang") == "!")


def fetch_pr(repo: str, number: int) -> dict:
    out = run_gh(["pr", "view", str(number), "--repo", repo, "--json", "title,body"])
    return json.loads(out)


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


def compose(repo: str, tag: str, prefix: str | None) -> str:
    last_release = get_last_release(repo, prefix, exclude_tag=tag)
    previous_tag = last_release["tag_name"] if last_release else None

    generated = generate_notes(repo, tag, previous_tag)
    numbers = pr_numbers_in_order(generated)

    # Strip GitHub's own leading HTML comment (only present when release.yml exists).
    generated = re.sub(r"^<!--.*?-->\n\n?", "", generated, flags=re.DOTALL)

    # Isolate "**Full Changelog**:" first — with zero PRs in range there's no
    # "## What's Changed" heading at all, so partitioning on "## New
    # Contributors" (usually absent too) would leave the changelog line stuck
    # inside `whats_changed`, and it'd get emitted twice.
    full_changelog_match = re.search(r"\*\*Full Changelog\*\*.*", generated, re.DOTALL)
    full_changelog = full_changelog_match.group(0).strip() if full_changelog_match else None
    before_changelog = generated[: full_changelog_match.start()] if full_changelog_match else generated
    whats_changed = before_changelog.split("## New Contributors")[0].strip()

    summary_lines = []
    for n in numbers:
        pr = fetch_pr(repo, n)
        title_breaking = is_breaking_title(pr["title"])
        body = pr["body"] or ""
        note = extract_note(body)
        breaking = extract_breaking(body) or (note if title_breaking else None)

        if breaking:
            summary_lines.append(f"- **Breaking:** {breaking} (#{n})")
        elif note:
            summary_lines.append(f"- {note} (#{n})")

    body_parts = [whats_changed or "## What's Changed\n_No PRs found in range._"]

    if summary_lines:
        body_parts.append("### Summary\n\n" + "\n".join(summary_lines))

    if full_changelog:
        body_parts.append(full_changelog.strip())

    return "\n\n".join(body_parts) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo", required=True, help="OWNER/REPO")
    parser.add_argument("--tag", required=True, help="the tag/release being cut (need not exist yet)")
    parser.add_argument(
        "--prefix",
        default=None,
        help="package tag prefix, e.g. 'gllm_inference-v' — scopes 'last release' "
        "to that package instead of the whole monorepo. Omit for single-package repos.",
    )
    args = parser.parse_args()

    print(compose(args.repo, args.tag, args.prefix))
    return 0


if __name__ == "__main__":
    sys.exit(main())
