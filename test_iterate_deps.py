"""
Test script to verify optional dependency imports with different configurations.
"""

import subprocess
import sys
import os

# Path to local gllm-pipeline
LOCAL_GLLM_PATH = os.path.abspath("../dev2/libs/gllm-pipeline")
TEST_SCRIPT = """
import sys
sys.path.insert(0, "{local_path}")

print("=" * 60)
print("Testing imports")
print("=" * 60)

# Check what's installed
print("\\n[0] Checking installed packages...")
try:
    import gllm_datastore
    print("    ✓ gllm_datastore")
except ImportError:
    print("    ✗ gllm_datastore")

try:
    import semantic_router
    print("    ✓ semantic_router")
except ImportError:
    print("    ✗ semantic_router")

try:
    import azure.search
    print("    ✓ azure-search-documents")
except ImportError:
    print("    ✗ azure-search-documents")

try:
    import gllm_inference
    print("    ✓ gllm_inference")
except ImportError:
    print("    ✗ gllm_inference")

# Test imports
print("\\n[1] Base gllm_pipeline import...")
try:
    import gllm_pipeline
    print("    ✓ gllm_pipeline")
except Exception as e:
    print(f"    ✗ {type(e).__name__}")

print("\\n[2] Aurelio backend import...")
try:
    from gllm_pipeline.router.backend import aurelio
    print("    ✓ aurelio")
except Exception as e:
    print(f"    ✗ {type(e).__name__}")

print("\\n[3] TEIEncoder import...")
try:
    from gllm_pipeline.router.backend.aurelio.encoders import TEIEncoder
    print(f"    ✓ TEIEncoder: {{TEIEncoder}}")
except Exception as e:
    print(f"    ✗ {type(e).__name__}")

print("\\n[4] DataStoreAdapterIndex import...")
try:
    from gllm_pipeline.router.backend.aurelio.index import DataStoreAdapterIndex
    print(f"    ✓ DataStoreAdapterIndex: {{DataStoreAdapterIndex}}")
except Exception as e:
    print(f"    ✗ {type(e).__name__}")

print("\\n[5] AzureAISearchAurelioIndex import...")
try:
    from gllm_pipeline.router.backend.aurelio.index import AzureAISearchAurelioIndex
    print(f"    ✓ AzureAISearchAurelioIndex: {{AzureAISearchAurelioIndex}}")
except Exception as e:
    print(f"    ✗ {type(e).__name__}")

print("\\n[6] EMInvokerEncoder import...")
try:
    from gllm_pipeline.router.backend.aurelio.encoders import EMInvokerEncoder
    print(f"    ✓ EMInvokerEncoder: {{EMInvokerEncoder}}")
except Exception as e:
    print(f"    ✗ {type(e).__name__}")

print("\\n" + "=" * 60)
""".format(local_path=LOCAL_GLLM_PATH)

# Test configurations
configs = [
    ("base (no extra)", ""),
    ("aurelio", "aurelio"),
    ("aurelio-datastore", "aurelio-datastore"),
    ("aurelio-azure", "aurelio-azure"),
]

for name, extra in configs:
    print(f"\n{'=' * 60}")
    print(f"Testing: {name}")
    print(f"{'=' * 60}")

    deps = ["gllm-pipeline"]
    if extra:
        deps.append(f"gllm-pipeline[{extra}]")

    # Create a temporary venv and test
    result = subprocess.run(
        ["python", "-c", TEST_SCRIPT],
        capture_output=True,
        text=True,
        cwd=os.path.dirname(__file__),
    )

    print(result.stdout)
    if result.stderr:
        # Filter out INFO logs
        stderr_lines = [
            l for l in result.stderr.split("\n") if "INFO" not in l and l.strip()
        ]
        if stderr_lines:
            print("STDERR:", "\n".join(stderr_lines[:5]))
