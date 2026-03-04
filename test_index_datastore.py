"""Test DataStoreAdapterIndex."""

import sys

sys.path.insert(0, "../dev2/libs/gllm-pipeline")

print("=" * 60)
print("TEST: DATASTORE ADAPTER INDEX")
print("=" * 60)

results = []

print("\n[1] Optional packages check:")
packages = [
    ("semantic_router", "semantic-router"),
    ("gllm_datastore", "gllm-datastore"),
]
for mod, pkg in packages:
    try:
        __import__(mod)
        print(f"  ✓ {pkg}")
        results.append((pkg, "installed"))
    except ImportError:
        print(f"  ✗ {pkg}")
        results.append((pkg, "missing"))

print("\n[2] Import DataStoreAdapterIndex:")
try:
    from gllm_pipeline.router.backend.aurelio.index import DataStoreAdapterIndex

    print(f"  ✓ DataStoreAdapterIndex: {DataStoreAdapterIndex}")
    results.append(("DataStoreAdapterIndex_import", "ok"))
except Exception as e:
    print(f"  ✗ Import failed: {e}")
    results.append(("DataStoreAdapterIndex_import", str(e)))

print("\n[3] Construct DataStoreAdapterIndex:")
try:
    from gllm_datastore.data_store.base import BaseDataStore, CapabilityType
    from unittest.mock import MagicMock

    mock_store = MagicMock(spec=BaseDataStore)
    mock_store.registered_capabilities = {CapabilityType.VECTOR}
    mock_store.get_size = MagicMock(return_value=0)

    index = DataStoreAdapterIndex(data_store=mock_store)
    print(f"  ✓ Created index: {index}")
    results.append(("DataStoreAdapterIndex_construct", "ok"))
except Exception as e:
    print(f"  ✗ Failed: {type(e).__name__}: {e}")
    results.append(("DataStoreAdapterIndex_construct", f"{type(e).__name__}: {e}"))

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
