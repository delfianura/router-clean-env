"""
Test script to verify optional dependency imports.
This should work without installing all optional dependencies.
"""

import sys
import os

# Add the local gllm-pipeline to the path
libs_path = os.path.join(
    os.path.dirname(__file__), "..", "dev2", "libs", "gllm-pipeline"
)
sys.path.insert(0, os.path.abspath(libs_path))

print("=" * 60)
print("Testing imports WITHOUT optional dependencies")
print("=" * 60)

# Check what's installed
print("\n[0] Checking installed packages...")
try:
    import gllm_datastore

    print("    ✓ gllm_datastore is installed")
except ImportError:
    print("    ✗ gllm_datastore is NOT installed")

try:
    import semantic_router

    print("    ✓ semantic_router is installed")
except ImportError:
    print("    ✗ semantic_router is NOT installed")

# Test 1: Base imports (should work)
print("\n[1] Testing base gllm_pipeline import...")
try:
    import gllm_pipeline

    print("    ✓ gllm_pipeline imported successfully")
except Exception as e:
    print(f"    ✗ Failed: {e}")

# Test 2: Import Aurelio backend module (should work)
print("\n[2] Testing gllm_pipeline.router.backend.aurelio import...")
try:
    from gllm_pipeline.router.backend import aurelio

    print("    ✓ aurelio backend imported successfully")
except Exception as e:
    print(f"    ✗ Failed: {type(e).__name__}: {e}")

# Test 3: Import encoders via lazy loading
print("\n[3] Testing lazy import of TEIEncoder...")
try:
    from gllm_pipeline.router.backend.aurelio.encoders import TEIEncoder

    print("    ✓ TEIEncoder class imported successfully")
    print(f"    Class: {TEIEncoder}")
except Exception as e:
    print(f"    ✗ Failed: {type(e).__name__}: {e}")

# Test 4: Import DataStoreAdapterIndex via lazy loading
print("\n[4] Testing lazy import of DataStoreAdapterIndex...")
try:
    from gllm_pipeline.router.backend.aurelio.index import DataStoreAdapterIndex

    print("    ✓ DataStoreAdapterIndex class imported successfully")
    print(f"    Class: {DataStoreAdapterIndex}")
except Exception as e:
    print(f"    ✗ Failed: {type(e).__name__}: {e}")

# Test 5: Import AzureAISearchAurelioIndex via lazy loading
print("\n[5] Testing lazy import of AzureAISearchAurelioIndex...")
try:
    from gllm_pipeline.router.backend.aurelio.index import AzureAISearchAurelioIndex

    print("    ✓ AzureAISearchAurelioIndex class imported successfully")
    print(f"    Class: {AzureAISearchAurelioIndex}")
except Exception as e:
    print(f"    ✗ Failed: {type(e).__name__}: {e}")

# Test 6: Try to instantiate DataStoreAdapterIndex
print("\n[6] Testing instantiation of DataStoreAdapterIndex...")
try:
    from gllm_pipeline.router.backend.aurelio.index import DataStoreAdapterIndex

    # Try with a mock/dict to see what happens
    try:
        index = DataStoreAdapterIndex(data_store={})
        print(f"    ✗ Should have failed but didn't! Got: {index}")
    except AttributeError as e:
        print(f"    ✓ Correctly failed with AttributeError: {e}")
    except ImportError as e:
        print(f"    ✓ Correctly failed with ImportError: {e}")
    except Exception as e:
        print(f"    ? Got different error: {type(e).__name__}: {e}")
except Exception as e:
    print(f"    ✗ Import failed: {type(e).__name__}: {e}")

# Test 7: Try to instantiate TEIEncoder
print("\n[7] Testing instantiation of TEIEncoder...")
try:
    from gllm_pipeline.router.backend.aurelio.encoders import TEIEncoder

    try:
        encoder = TEIEncoder(name="test", base_url="http://test", api_key="test")
        print(f"    ✗ Should have failed but didn't! Got: {encoder}")
    except (ImportError, ValueError) as e:
        print(f"    ✓ Correctly failed with {type(e).__name__}: {str(e)[:60]}...")
    except Exception as e:
        print(f"    ? Got different error: {type(e).__name__}: {str(e)[:60]}...")
except Exception as e:
    print(f"    ✗ Import failed: {type(e).__name__}: {e}")

# Test 8: Import EMInvokerEncoder (requires gllm-inference)
print("\n[8] Testing lazy import of EMInvokerEncoder...")
try:
    from gllm_pipeline.router.backend.aurelio.encoders import EMInvokerEncoder

    print("    ✓ EMInvokerEncoder class imported successfully")
    print(f"    Class: {EMInvokerEncoder}")
except Exception as e:
    print(f"    ✗ Failed: {type(e).__name__}: {e}")

print("\n" + "=" * 60)
print("Test complete!")
print("=" * 60)
