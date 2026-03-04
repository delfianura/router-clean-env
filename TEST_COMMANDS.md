# Test Commands Guide

## Prerequisite: Install dependencies

```bash
cd libs/gllm-pipeline
uv sync
```

---

## 1. Test Import Without Optional Dependencies

**Command:**
```bash
cd gllm-test-project
source .venv/bin/activate
python test_import_lazy.py
```

**Expected output (all should pass when deps missing):**
- Lazy imports should succeed (no ModuleNotFoundError at import time)
- Instantiation should fail with clear error

---

## 2. Test Base Imports

**Command:**
```bash
cd gllm-test-project
source .venv/bin/activate
python test_import_base.py
```

---

## 3. Test TEIEncoder

**Command:**
```bash
cd gllm-test-project
source .venv/bin/activate
python test_encoder_tei.py
```

**Checks:**
- [ ] Optional package check (semantic_router)
- [ ] Import TEIEncoder
- [ ] Construct TEIEncoder
- [ ] Use in SemanticRouter.aurelio()
- [ ] Invoke router

---

## 4. Test EMInvokerEncoder

**Command:**
```bash
cd gllm-test-project
source .venv/bin/activate
python test_encoder_em_invoker.py
```

**Checks:**
- [ ] Optional package check (semantic_router, gllm_inference)
- [ ] Import EMInvokerEncoder
- [ ] Construct mock EMInvoker + encoder
- [ ] Use in SemanticRouter.aurelio()
- [ ] Invoke router

---

## 5. Test LangchainEmbeddingsEncoder

**Command:**
```bash
cd gllm-test-project
source .venv/bin/activate
python test_encoder_langchain.py
```

**Checks:**
- [ ] Optional package check (semantic_router, langchain_openai)
- [ ] Import LangchainEmbeddingsEncoder
- [ ] Construct encoder with OpenAIEmbeddings
- [ ] Use in SemanticRouter.aurelio()
- [ ] Invoke router

---

## 6. Test DataStoreAdapterIndex

**Command:**
```bash
cd gllm-test-project
source .venv/bin/activate
python test_index_datastore.py
```

**Checks:**
- [ ] Optional package check (semantic_router, gllm_datastore)
- [ ] Import DataStoreAdapterIndex
- [ ] Construct with mock BaseDataStore
- [ ] Use in SemanticRouter.aurelio()
- [ ] Invoke router

---

## 7. Test AzureAISearchAurelioIndex

**Command:**
```bash
cd gllm-test-project
source .venv/bin/activate
python test_index_azure.py
```

**Checks:**
- [ ] Optional package check (semantic_router, azure-search-documents)
- [ ] Import AzureAISearchAurelioIndex
- [ ] Construct with endpoint/api_key
- [ ] Use in SemanticRouter.aurelio()
- [ ] Invoke router

---

## Unit Tests

### Run all encoder + index tests
```bash
cd libs/gllm-pipeline
source .venv/bin/activate
python -m pytest tests/unit_tests/router/backend/aurelio/encoders/ tests/unit_tests/router/backend/aurelio/index/ -v
```

### Run specific encoder tests
```bash
cd libs/gllm-pipeline
source .venv/bin/activate
python -m pytest tests/unit_tests/router/backend/aurelio/encoders/test_tei_encoder.py -v
python -m pytest tests/unit_tests/router/backend/aurelio/encoders/test_em_invoker_encoder.py -v
python -m pytest tests/unit_tests/router/backend/aurelio/encoders/test_langchain_encoder.py -v
```

### Run specific index tests
```bash
cd libs/gllm-pipeline
source .venv/bin/activate
python -m pytest tests/unit_tests/router/backend/aurelio/index/test_data_store_adapter_index.py -v
python -m pytest tests/unit_tests/router/backend/aurelio/index/test_azure_ai_search_aurelio_index.py -v
```

---

## Evaluation Checklist

| Test | Import | Construct | Use in Router | Invoke |
|------|--------|-----------|---------------|--------|
| TEIEncoder | [ ] | [ ] | [ ] | [ ] |
| EMInvokerEncoder | [ ] | [ ] | [ ] | [ ] |
| LangchainEmbeddingsEncoder | [ ] | [ ] | [ ] | [ ] |
| DataStoreAdapterIndex | [ ] | [ ] | [ ] | [ ] |
| AzureAISearchAurelioIndex | [ ] | [ ] | [ ] | [ ] |

**Unit tests:** 54 passed [ ]
