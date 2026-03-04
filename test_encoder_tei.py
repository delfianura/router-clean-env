"""Test TEIEncoder."""

import sys

sys.path.insert(0, "../dev2/libs/gllm-pipeline")

print("=" * 60)
print("TEST: TEI ENCODER")
print("=" * 60)

results = []

print("\n[1] Optional packages check:")
packages = [
    ("semantic_router", "semantic-router"),
]
for mod, pkg in packages:
    try:
        __import__(mod)
        print(f"  ✓ {pkg}")
        results.append((pkg, "installed"))
    except ImportError:
        print(f"  ✗ {pkg}")
        results.append((pkg, "missing"))

print("\n[2] Import TEIEncoder:")
try:
    from gllm_pipeline.router.backend.aurelio.encoders import TEIEncoder

    print(f"  ✓ TEIEncoder: {TEIEncoder}")
    results.append(("TEIEncoder_import", "ok"))
except Exception as e:
    print(f"  ✗ TEIEncoder: {e}")
    results.append(("TEIEncoder_import", str(e)))

print("\n[3] Construct TEIEncoder:")
TEI_CONFIG = {
    "name": "test-tei-encoder",
    "base_url": "http://localhost:8080",
    "api_key": "test-key",
}
try:
    encoder = TEIEncoder(**TEI_CONFIG)
    print(f"  ✓ Created: {encoder}")
    results.append(("TEIEncoder_construct", "ok"))
except Exception as e:
    print(f"  ✗ Failed: {type(e).__name__}: {e}")
    results.append(("TEIEncoder_construct", f"{type(e).__name__}: {e}"))

print("\n[4] Use in SemanticRouter.aurelio():")
try:
    from gllm_pipeline import SemanticRouter

    routes = [{"name": "test", "utterances": ["hello"]}]
    router = SemanticRouter.aurelio(
        routes=routes,
        encoder=encoder,
    )
    print(f"  ✓ Created router: {router}")
    results.append(("SemanticRouter_aurelio", "ok"))
except Exception as e:
    print(f"  ✗ Failed: {type(e).__name__}: {e}")
    results.append(("SemanticRouter_aurelio", f"{type(e).__name__}: {e}"))

print("\n[5] Invoke router:")
try:
    result = router("hello")
    print(f"  ✓ Result: {result}")
    results.append(("router_invoke", "ok"))
except Exception as e:
    print(f"  ✗ Failed: {type(e).__name__}: {e}")
    results.append(("router_invoke", f"{type(e).__name__}: {e}"))

print("\n" + "=" * 60)
print("REPORT:")
print("=" * 60)
for pkg, status in results:
    print(f"  {pkg}: {status}")
