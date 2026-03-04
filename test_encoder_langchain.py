"""Test LangchainEmbeddingsEncoder."""

import sys

sys.path.insert(0, "../dev2/libs/gllm-pipeline")

print("=" * 60)
print("TEST: LANGCHAIN EMBEDDINGS ENCODER")
print("=" * 60)

results = []

print("\n[1] Optional packages check:")
packages = [
    ("semantic_router", "semantic-router"),
    ("langchain_openai", "langchain-openai"),
]
for mod, pkg in packages:
    try:
        __import__(mod)
        print(f"  ✓ {pkg}")
        results.append((pkg, "installed"))
    except ImportError:
        print(f"  ✗ {pkg}")
        results.append((pkg, "missing"))

print("\n[2] Import LangchainEmbeddingsEncoder:")
try:
    from gllm_pipeline.router.backend.aurelio.encoders import LangchainEmbeddingsEncoder

    print(f"  ✓ LangchainEmbeddingsEncoder: {LangchainEmbeddingsEncoder}")
    results.append(("LangchainEmbeddingsEncoder_import", "ok"))
except Exception as e:
    print(f"  ✗ Import failed: {e}")
    results.append(("LangchainEmbeddingsEncoder_import", str(e)))

print("\n[3] Construct Langchain encoder:")
try:
    from langchain_openai import OpenAIEmbeddings

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key="sk-test",
    )
    encoder = LangchainEmbeddingsEncoder(embeddings)
    print(f"  ✓ Created encoder: {encoder}")
    results.append(("LangchainEmbeddingsEncoder_construct", "ok"))
except Exception as e:
    print(f"  ✗ Failed: {type(e).__name__}: {e}")
    results.append(("LangchainEmbeddingsEncoder_construct", f"{type(e).__name__}: {e}"))

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
