"""Test EMInvokerEncoder."""

import sys

sys.path.insert(0, "../dev2/libs/gllm-pipeline")

print("=" * 60)
print("TEST: EM INVOKER ENCODER")
print("=" * 60)

results = []

print("\n[1] Optional packages check:")
packages = [
    ("semantic_router", "semantic-router"),
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

print("\n[2] Import EMInvokerEncoder:")
try:
    from gllm_pipeline.router.backend.aurelio.encoders import EMInvokerEncoder
    from gllm_inference.em_invoker.em_invoker import BaseEMInvoker
    from gllm_inference.schema.model_id import ModelId

    print(f"  ✓ EMInvokerEncoder: {EMInvokerEncoder}")
    results.append(("EMInvokerEncoder_import", "ok"))
except Exception as e:
    print(f"  ✗ Import failed: {e}")
    results.append(("EMInvokerEncoder_import", str(e)))

print("\n[3] Construct mock EMInvoker:")
try:

    class MockEMInvoker(BaseEMInvoker):
        async def _invoke(self, docs, hyperparameters):
            return [[0.1] * 384 for _ in docs]

        def to_langchain(self):
            raise NotImplementedError

    mock_invoker = MockEMInvoker(model_id=ModelId.from_string("openai/gpt-5-nano"))
    encoder = EMInvokerEncoder(mock_invoker, name="test-em-invoker")
    print(f"  ✓ Created encoder: {encoder}")
    results.append(("EMInvokerEncoder_construct", "ok"))
except Exception as e:
    print(f"  ✗ Failed: {type(e).__name__}: {e}")
    results.append(("EMInvokerEncoder_construct", f"{type(e).__name__}: {e}"))

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
