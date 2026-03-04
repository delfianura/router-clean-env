"""
Simple test to verify lazy imports work correctly.
"""

import sys
import os

# Use local path
libs_path = os.path.join(
    os.path.dirname(__file__), "..", "dev2", "libs", "gllm-pipeline"
)
sys.path.insert(0, os.path.abspath(libs_path))

print("Testing lazy imports with different optional deps scenarios")
print("=" * 60)

# Scenario 1: Base imports (no optional deps needed)
print("\n[Scenario 1] Base gllm_pipeline import")
try:
    import gllm_pipeline

    print("  ✓ gllm_pipeline")
except Exception as e:
    print(f"  ✗ {type(e).__name__}: {e}")

# Scenario 2: Check what's currently installed
print("\n[Check] Optional packages installed:")
try:
    import gllm_datastore

    print("  ✓ gllm_datastore")
except ImportError:
    print("  ✗ gllm_datastore (not installed)")

try:
    import semantic_router

    print("  ✓ semantic_router")
except ImportError:
    print("  ✗ semantic_router (not installed)")

try:
    import azure.search

    print("  ✓ azure-search-documents")
except ImportError:
    print("  ✗ azure-search-documents (not installed)")

try:
    import gllm_inference

    print("  ✓ gllm_inference")
except ImportError:
    print("  ✗ gllm_inference (not installed)")

# Scenario 3: Test lazy imports
print("\n[Scenario 3] Test lazy imports (no instantiation)")

# TEIEncoder - requires semantic_router
print("\n  TEIEncoder (requires semantic_router):")
try:
    from gllm_pipeline.router.backend.aurelio.encoders import TEIEncoder

    print(f"    ✓ Import OK: {TEIEncoder.__module__}.{TEIEncoder.__name__}")
except Exception as e:
    print(f"    ✗ {type(e).__name__}: {e}")

# DataStoreAdapterIndex - requires semantic_router + gllm_datastore
print("\n  DataStoreAdapterIndex (requires semantic_router + gllm_datastore):")
try:
    from gllm_pipeline.router.backend.aurelio.index import DataStoreAdapterIndex

    print(
        f"    ✓ Import OK: {DataStoreAdapterIndex.__module__}.{DataStoreAdapterIndex.__name__}"
    )
except Exception as e:
    print(f"    ✗ {type(e).__name__}: {e}")

# AzureAISearchAurelioIndex - requires semantic_router + azure
print("\n  AzureAISearchAurelioIndex (requires semantic_router + azure):")
try:
    from gllm_pipeline.router.backend.aurelio.index import AzureAISearchAurelioIndex

    print(
        f"    ✓ Import OK: {AzureAISearchAurelioIndex.__module__}.{AzureAISearchAurelioIndex.__name__}"
    )
except Exception as e:
    print(f"    ✗ {type(e).__name__}: {e}")

# EMInvokerEncoder - requires semantic_router + gllm_inference
print("\n  EMInvokerEncoder (requires semantic_router + gllm_inference):")
try:
    from gllm_pipeline.router.backend.aurelio.encoders import EMInvokerEncoder

    print(f"    ✓ Import OK: {EMInvokerEncoder.__module__}.{EMInvokerEncoder.__name__}")
except Exception as e:
    print(f"    ✗ {type(e).__name__}: {e}")

# LangchainEmbeddingsEncoder - requires semantic_router
print("\n  LangchainEmbeddingsEncoder (requires semantic_router):")
try:
    from gllm_pipeline.router.backend.aurelio.encoders import LangchainEmbeddingsEncoder

    print(
        f"    ✓ Import OK: {LangchainEmbeddingsEncoder.__module__}.{LangchainEmbeddingsEncoder.__name__}"
    )
except Exception as e:
    print(f"    ✗ {type(e).__name__}: {e}")

print("\n" + "=" * 60)
print("Done!")
