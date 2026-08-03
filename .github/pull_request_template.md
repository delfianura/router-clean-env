## Summary

<!-- Brief description of what this PR does and why it's needed -->

## Release Notes

<!--
One or two sentences describing the USER-VISIBLE impact of this PR, for people who
do not read the diff: other engineers using the SDK, PMs, docs writers.

- Name the public API/class/function affected (in backticks).
- Say what it now lets the caller do, or what behavior changed for them.
- Do NOT describe implementation details (which file changed, internal refactors)
  unless that internal change is itself the user-facing point (e.g. a perf fix).
- If this PR has no user-visible effect (CI, internal refactor, test-only), write
  "internal" and it will be excluded from the generated release summary.
- If this PR breaks an existing public API, also fill in the "Breaking Change"
  block below — leave it empty otherwise.

Example:
`LoggerManager.register_global_json_field(...)` lets applications add dynamic fields
such as request IDs to every JSON log record, while preserving per-message `extra`
precedence and keeping logging resilient if a field factory fails.
-->

<!-- release-note:start -->
internal
<!-- release-note:end -->

<!-- release-note-breaking:start -->
<!-- release-note-breaking:end -->

## How to Test

<!-- Provide clear steps for reviewers to test your changes -->

1. Step 1
2. Step 2
3. Expected result

## Related Issues

<!-- Link related issues using: Closes #123, Fixes #456, Related to #789 -->

## Author Checklist

- [ ] Code follows team coding standards and style guide
- [ ] Self-reviewed the code changes
- [ ] Added/updated tests for new functionality
- [ ] All tests pass locally
- [ ] Code is properly documented
- [ ] Synced with latest `main` branch
- [ ] PR title follows conventional commit format
- [ ] Meaningful commit messages used
- [ ] Release Notes section filled in (or marked `internal`)

## Additional Notes

1. [GDP Labs Coding and Code Review Best Practices](https://docs.google.com/document/d/1QCzqnxXPEN_fatbTaSt-LVL9vFKoEBrQ6zTCt3tbCWU/edit)
