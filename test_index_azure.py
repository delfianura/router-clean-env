"""Test AzureAISearchAurelioIndex."""

import sys

sys.path.insert(0, "../dev2/libs/gllm-pipeline")

print("=" * 60)
print("TEST: AZURE AI SEARCH INDEX")
print("=" * 60)

results = []

print("\n[1] Optional packages check:")
packages = [
    ("semantic_router", "semantic-router"),
    ("azure.search", "azure-search-documents"),
]
for mod, pkg in packages:
    try:
        __import__(mod)
        print(f"  ✓ {pkg}")
        results.append((pkg, "installed"))
    except ImportError:
        print(f"  ✗ {pkg}")
        results.append((pkg, "missing"))

print("\n[2] Import AzureAISearchAurelioIndex:")
try:
    from gllm_pipeline.router.backend.aurelio.index import AzureAISearchAurelioIndex

    print(f"  ✓ AzureAISearchAurelioIndex: {AzureAISearchAurelioIndex}")
    results.append(("AzureAISearchAurelioIndex_import", "ok"))
except Exception as e:
    print(f"  ✗ Import failed: {e}")
    results.append(("AzureAISearchAurelioIndex_import", str(e)))

print("\n[3] Construct AzureAISearchAurelioIndex:")
AZURE_CONFIG = {
    "endpoint": "https://test.search.windows.net",
    "index_name": "test-index",
    "api_key": "test-key",
}
try:
    index = AzureAISearchAurelioIndex(**AZURE_CONFIG)
    print(f"  ✓ Created index: {index}")
    results.append(("AzureAISearchAurelioIndex_construct", "ok"))
except Exception as e:
    print(f"  ✗ Failed: {type(e).__name__}: {e}")
    results.append(("AzureAISearchAurelioIndex_construct", f"{type(e).__name__}: {e}"))

print("\n[4] Use in SemanticRouter.aurelio():")
try:
    from gllm_pipeline import SemanticRouter
    from semantic_router import Route

    routes = [Route(name="test", utterances=["hello"])]
    router = SemanticRouter.aurelio(
        routes=routes,
        index=index,
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
