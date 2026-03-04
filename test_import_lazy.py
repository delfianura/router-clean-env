"""Test import when optional deps are NOT installed."""

import sys

sys.path.insert(0, "../dev2/libs/gllm-pipeline")

print("=" * 60)
print("TEST: IMPORT WITHOUT OPTIONAL DEPS")
print("=" * 60)

results = []

print("\n[1] Check what's currently installed:")
packages = [
    ("semantic_router", "semantic-router"),
    ("gllm_datastore", "gllm-datastore"),
    ("azure.search", "azure-search-documents"),
    ("gllm_inference", "gllm-inference"),
]
for mod, pkg in packages:
    try:
        __import__(mod)
        print(f"  ✓ {pkg} - INSTALLED")
        results.append((pkg, "installed"))
    except ImportError:
        print(f"  ✗ {pkg} - NOT INSTALLED")
        results.append((pkg, "missing"))

print("\n[2] Test lazy imports (should work even if deps missing):")

print("\n  TEIEncoder (requires semantic_router):")
try:
    from gllm_pipeline.router.backend.aurelio.encoders import TEIEncoder

    print(f"    ✓ Import OK")
    results.append(("TEIEncoder_lazy", "ok"))
except ImportError as e:
    print(f"    ✗ ImportError: {e}")
    results.append(("TEIEncoder_lazy", str(e)))

print("\n  EMInvokerEncoder (requires semantic_router + gllm_inference):")
try:
    from gllm_pipeline.router.backend.aurelio.encoders import EMInvokerEncoder

    print(f"    ✓ Import OK")
    results.append(("EMInvokerEncoder_lazy", "ok"))
except ImportError as e:
    print(f"    ✗ ImportError: {e}")
    results.append(("EMInvokerEncoder_lazy", str(e)))

print("\n  LangchainEmbeddingsEncoder (requires semantic_router):")
try:
    from gllm_pipeline.router.backend.aurelio.encoders import LangchainEmbeddingsEncoder

    print(f"    ✓ Import OK")
    results.append(("LangchainEmbeddingsEncoder_lazy", "ok"))
except ImportError as e:
    print(f"    ✗ ImportError: {e}")
    results.append(("LangchainEmbeddingsEncoder_lazy", str(e)))

print("\n  DataStoreAdapterIndex (requires semantic_router + gllm_datastore):")
try:
    from gllm_pipeline.router.backend.aurelio.index import DataStoreAdapterIndex

    print(f"    ✓ Import OK")
    results.append(("DataStoreAdapterIndex_lazy", "ok"))
except ImportError as e:
    print(f"    ✗ ImportError: {e}")
    results.append(("DataStoreAdapterIndex_lazy", str(e)))

print("\n  AzureAISearchAurelioIndex (requires semantic_router + azure):")
try:
    from gllm_pipeline.router.backend.aurelio.index import AzureAISearchAurelioIndex

    print(f"    ✓ Import OK")
    results.append(("AzureAISearchAurelioIndex_lazy", "ok"))
except ImportError as e:
    print(f"    ✗ ImportError: {e}")
    results.append(("AzureAISearchAurelioIndex_lazy", str(e)))

print("\n" + "=" * 60)
print("REPORT:")
print("=" * 60)
for pkg, status in results:
    print(f"  {pkg}: {status}")
