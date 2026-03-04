"""Test base imports."""

import sys

sys.path.insert(0, "../dev2/libs/gllm-pipeline")

print("=" * 60)
print("TEST: BASE IMPORTS")
print("=" * 60)

results = []

print("\n[1] Check optional packages:")
packages = [
    ("semantic_router", "semantic-router"),
    ("gllm_datastore", "gllm-datastore"),
    ("azure.search", "azure-search-documents"),
    ("gllm_inference", "gllm-inference"),
]

for mod, pkg in packages:
    try:
        __import__(mod)
        print(f"  ✓ {pkg}")
        results.append((pkg, "installed"))
    except ImportError:
        print(f"  ✗ {pkg}")
        results.append((pkg, "missing"))

print("\n[2] Base imports:")
try:
    import gllm_pipeline

    print("  ✓ gllm_pipeline")
    results.append(("gllm_pipeline", "ok"))
except Exception as e:
    print(f"  ✗ gllm_pipeline: {e}")
    results.append(("gllm_pipeline", str(e)))

print("\n[3] Backend imports:")
try:
    from gllm_pipeline.router.backend import aurelio

    print("  ✓ aurelio backend")
    results.append(("aurelio", "ok"))
except Exception as e:
    print(f"  ✗ aurelio: {e}")
    results.append(("aurelio", str(e)))

print("\n" + "=" * 60)
print("REPORT:")
print("=" * 60)
for pkg, status in results:
    print(f"  {pkg}: {status}")
