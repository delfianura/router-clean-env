# Router Clean Environment Test

Test project to verify optional dependency imports for gllm-pipeline Aurelio backend.

## Setup

```bash
# Clone the repo
git clone https://github.com/delfianura/router-clean-env.git
cd router-clean-env

# Create virtual environment
uv venv
source .venv/bin/activate

# Install base dependencies
uv sync
```

## Optional Dependencies

Edit `pyproject.toml` to test different optional dependency combinations:

### 1. Base (semantic-router only)
```toml
dependencies = [
    "gllm-pipeline[aurelio]",
]
```

### 2. With DataStore
```toml
dependencies = [
    "gllm-pipeline[aurelio-datastore]",
]
```

### 3. With Azure
```toml
dependencies = [
    "gllm-pipeline[aurelio-azure]",
]
```

### 4. All extras
```toml
dependencies = [
    "gllm-pipeline[aurelio,aurelio-datastore,aurelio-azure]",
]
```

After editing, run:
```bash
uv sync
```

## Test Commands

### 1. Test Lazy Imports (without optional deps)
```bash
python test_import_lazy.py
```

### 2. Test Base Imports
```bash
python test_import_base.py
```

### 3. Test Encoders

```bash
python test_encoder_tei.py
python test_encoder_em_invoker.py
python test_encoder_langchain.py
```

### 4. Test Indexes

```bash
python test_index_datastore.py
python test_index_azure.py
```

## Running Unit Tests

```bash
cd ../libs/gllm-pipeline
source .venv/bin/activate
python -m pytest tests/unit_tests/router/backend/aurelio/encoders/ tests/unit_tests/router/backend/aurelio/index/ -v
```

## Expected Results

| Test | Optional Deps Required |
|------|----------------------|
| TEIEncoder | semantic-router |
| EMInvokerEncoder | semantic-router, gllm-inference |
| LangchainEmbeddingsEncoder | semantic-router, langchain-openai |
| DataStoreAdapterIndex | semantic-router, gllm-datastore |
| AzureAISearchAurelioIndex | semantic-router, azure-search-documents |

## Using Local gllm-pipeline

To test a local version of gllm-pipeline, edit `pyproject.toml`:

```toml
[tool.uv.sources]
gllm-pipeline = { path = "../dev2/libs/gllm-pipeline", editable = true }
```

Then run:
```bash
uv sync
```

## Simulated feature: per-call timeout

## Simulated fix: retry leak
