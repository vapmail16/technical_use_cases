# 🛠️ TROUBLESHOOTING LOG — Compliance Report Generator

This file logs common errors encountered during development of the AI-powered compliance assistant, along with their reasons and resolutions.

---

## ✅ Summary of Errors & Fixes

| #  | Error Message (Short)                                                    | 📍 Source File                   | 💥 Root Cause                                     | ✅ Resolution                                                                 |
|----|---------------------------------------------------------------------------|----------------------------------|--------------------------------------------------|----------------------------------------------------------------------------------|
| 1  | `ModuleNotFoundError: No module named 'langchain_community'`             | `retrial_chain.py`, `ingest.py` | LangChain split into modular packages            | `poetry add langchain-openai` or `langchain-community`                          |
| 2  | `ModuleNotFoundError: No module named 'tiktoken'`                         | `ingest.py`                      | OpenAI embeddings need tokenizer                 | `poetry add tiktoken`                                                           |
| 3  | `NameError: name 'client' is not defined`                                 | `ingest.py`                      | Qdrant client used before defined               | Move `QdrantClient(...)` above usage                                           |
| 4  | `ImportError: create_structured_output_chain`                             | `doc_to_graph.py`               | Function deprecated in LangChain >= 0.1.1        | Replaced with `with_structured_output()`                                       |
| 5  | `No fulltext schema index: entityIndex`                                   | `neo4j_utils.py`                | Neo4j index not created                         | Created via `CREATE FULLTEXT INDEX...` or automated                            |
| 6  | `ProcedureNotFound: CALL db.indexes`                                      | `neo4j_utils.py`                | Not supported on Neo4j Free/Aura                | Use `CREATE FULLTEXT INDEX ... IF NOT EXISTS` directly                         |
| 7  | `Invalid input type <class 'dict'>`                                       | `doc_to_graph.py`               | Passed dict to `.invoke()`                      | Use a prompt string, not a dict                                                |
| 8  | `OpenAIEmbeddings deprecated`                                             | `retrial_chain.py`, `ingest.py` | Legacy class removed in LangChain 1.0            | Use `from langchain_openai import OpenAIEmbeddings`                            |
| 9  | `LangChain uses pydantic v2` warning                                      | `doc_to_graph.py`               | Deprecated use of `pydantic_v1`                 | Replace with `from pydantic import ...`                                        |
| 10 | `SyntaxError: Invalid input 'WITH'`                                       | `neo4j_utils.py`                | `WITH` used incorrectly after `SHOW INDEXES`     | Replaced with `CREATE FULLTEXT INDEX ... IF NOT EXISTS`                        |
| 11 | `Neo.ClientError.Procedure.ProcedureCallFailed`                           | `neo4j_utils.py`                | Index `entityIndex` missing or malformed         | Ensure index using portable `CREATE FULLTEXT INDEX ...`                        |
| 12 | `ParseException: Encountered <EOF> ...`                                   | `neo4j_utils.py`                | Empty string passed to `queryNodes`              | Add check to skip query if `question.strip()` is empty                         |
| 13 | `ValidationError: context not found in llm_chain input_variables`         | `memory_aware_agent.py`         | `{context}` missing in QA chain prompt           | Use `PromptTemplate` and pass via `chain_type_kwargs`                          |
| 14 | `ValueError: Missing some input keys: {'graph_memory', 'role'}`            | `main.py`                      | Inputs required by the chain (role + memory) not passed | Use `.invoke()` with all expected keys: `question`, `role`, `graph_memory`         |
| 15 | `ValidationError: document_variable_name context not found`               | `memory_aware_agent.py`       | Chain expecting a variable `context` not present in prompt | Ensure prompt input variables match: use `question`, `graph_memory`, `role`        |
| 16 |	Missing some input keys: {'query'}	| main.py	| RetrievalQA expects "query" not "question"	| Use {"query": question} instead of {"question": question}
| 17 |	Missing some input keys: {'role', 'graph_memory'} |	main.py |	RetrievalQA expects only keys in prompt's input variables |	Remove extra keys from .invoke() or update the prompt
| 18 | `ValueError: Missing some input keys: {'role', 'graph_memory'}`          | `main.py` → `memory_aware_agent.py` | `input_key="question"` restricts accepted keys to just `question` | ✅ Remove `input_key="question"` from `RetrievalQA(...)` to allow full input dictionary |
| 19 |	ImportError: cannot import name 'StuffDocumentsChain'	memory_aware_agent.py	StuffDocumentsChain is deprecated or removed in newer LangChain	Replace with from langchain.chains.combine_documents.base import CombineDocumentsChain and use CombineDocumentsChain(...)
| 20 |	ImportError: cannot import name 'CombineDocumentsChain'	 |memory_aware_agent.py	|LangChain removed this class in favor of Runnable-based chaining	|Use RunnablePassthrough + RunnableLambda + LLMChain instead
| 21 |	ImportError: cannot import name 'get_retriever'	|memory_aware_agent.py	|retrieval_chain.py didn't define get_retriever() as a separate function	|Added a get_retriever() wrapper in retrieval_chain.py returning Qdrant retriever
| 22 |	AttributeError: 'RunnableSequence' object has no attribute 'get'	|memory_aware_agent.py	|RetrievalQA class deprecated post LangChain 0.1.17	|Use create_retrieval_chain() from langchain.chains.retrieval_qa instead
| 23 |	ImportError: cannot import name 'create_retrieval_chain'	memory_aware_agent.py	create_retrieval_chain moved from retrieval_qa to combine_documents	Use from langchain.chains.combine_documents import create_retrieval_chain
| 24 |	ImportError: cannot import name 'create_retrieval_chain' from combine_documents	memory_aware_agent.py	The function is not in root combine_documents module	Use from langchain.chains.combine_documents.base import create_retrieval_chain
| 25 |	ImportError: cannot import name 'create_retrieval_chain' from combine_documents	memory_aware_agent.py	Incorrect import path for latest LangChain version	Use from langchain.chains.retrieval_qa.base import create_retrieval_chain
| 26 |	ImportError: cannot import name 'create_stuff_documents_chain' from base	memory_aware_agent.py	Function was moved to higher-level module in LangChain update	Use from langchain.chains.combine_documents import create_stuff_documents_chain
| 27 |	ImportError: cannot import name 'create_retrieval_chain' from retrieval_qa.base	memory_aware_agent.py	Function moved to top-level langchain.chains in newer LangChain	Use from langchain.chains import create_retrieval_chain
| 28 |	KeyError: 'input'	main.py	create_retrieval_chain expects input key	Replace question=... with input=... in .invoke() call
| 29 |	KeyError: Input to PromptTemplate is missing variable	main.py, memory_aware_agent.py	PromptTemplate expects question, but input was passed	Either: (1) Rename input to question in .invoke() OR (2) use {input} in template
| 30 |	KeyError: 'result'	main.py	create_retrieval_chain() returns answer not result	Replace result['result'] with result['answer']
| 31 |	KeyError: 'source_documents'	main.py	create_retrieval_chain() returns context not source_documents	Replace result["source_documents"] with result["context"]
| 32 |	KeyError: 'result'	main.py	create_retrieval_chain() uses answer key instead of result	Replace result["result"] with result["answer"]
| 33 |	Error fetching news: ...	news_tool.py	.env not loaded, missing NEWS_API_KEY	Added from dotenv import load_dotenv; load_dotenv()
| 34 |	ModuleNotFoundError: No module named 'test_compliance_lookup.py'	CLI test	File didn’t exist	Created test file tools/test_compliance_lookup.py
| 35 |	ImportError: cannot import name 'calculate_risk_score'	test_risk_calculator.py	Function name mismatch	Corrected import to calculate_risk
| 36 |	LangChainDeprecationWarning: __call__ deprecated	test_risk_calculator.py	Used __call__ instead of .invoke()	Updated to use tool.invoke(...)
| 37 |	AttributeError: 'str' object has no attribute 'parent_run_id'	test_risk_calculator.py	Called tool like function instead of using .invoke()	Wrapped input in dict and used invoke() method
| 38 |	openai.OpenAIError: The api_key client option must be set...	summary_filter_tool.py	OPENAI_API_KEY not loaded into env	Added load_dotenv() and ensured .env is populated
| 39 |	LangChainDeprecationWarning: run()	All tools	Use of deprecated run() and __call__ methods	Moved to .invoke() pattern in test scripts
| 40 |	No module named 'tools'	tool_calling_agent.py	Python couldn't resolve tools because the folder wasn't a package	Added __init__.py to the tools/ directory
| 41 |	No module named 'tool_calling_agent'	CLI test run	Incorrect relative import	Used python -m agents.test_tool_agent instead of direct execution
| 42 |	cannot import name 'lookup_compliance'	registry.py	The function was located in compliance_lookup.py, not the previously named compliance_lookup_tool.py	Updated import path correctly
| 43 |	No module named 'compliance_lookup_tool'	compliance_lookup.py	Renamed file caused import mismatch	Changed import to match updated file name
| 44 |	ZeroShotAgent does not support multi-input tool	tool_calling_agent.py	LangChain ZeroShotAgent only supports tools with one input	Used tool.as_tool() for those with one input, excluded multi-input tools or adapted them
| 45 |	Agent stuck in loop calling lookup_compliance	tool_calling_agent.py	Tool returned message saying "Try 'GDPR'" even when correct term was provided	Fixed tool to avoid quoting term='GDPR', ensured case normalization and prompt formatting
| 46 |	OPENAI_API_KEY missing	summary_filter_tool.py	Environment variable not loaded	Added from dotenv import load_dotenv and called load_dotenv() at top
| 47 |	DeprecationWarning: BaseTool.__call__	CLI tests for tools	LangChain deprecated direct tool() calls	Replaced with .invoke() method during testing
| 48 |	Tool returning incorrect structure	Streamlit (ToolAgent)	Agent output included raw {'input': ..., 'output': ...} format	Updated agent to parse and present just the output in the UI
| 49 |	agent.run() deprecated	test_tool_agent.py	LangChain recommends .invoke() over .run()	Plan to update to .invoke() method for future-proofing
| 50 |	ValueError: Must provide state_schema or input and output	checkpoint_graph.py	Missing StateGraph(MyTypedDict) definition	Defined schema using WorkflowState or State class
| 51 |	NameError: name 'ingest_documents' is not defined	checkpoint_graph.py	Function used before imported	Added from vector_store.ingest import ingest_documents
| 52 |	NameError: name 'store_in_vector_db' is not defined	checkpoint_graph.py	Used placeholder not defined	Replaced with actual call to ingest_documents(file_path) again
| 53 |	UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe2...	checkpoint_graph.py (Graph Node)	Tried reading binary PDF file as plain text	Switched to pdfplumber and extracted text safely
| 54 |	OpenAIError: context_length_exceeded	doc_to_graph.py	Entire PDF text sent to LLM for graph extraction	Chunked input to stay within token limits
| 55 |	ModuleNotFoundError: No module named 'langgraph'	CLI Run	Dependency not installed in venv	Ran poetry add langgraph and re-activated venv
| 56 |	ModuleNotFoundError: No module named 'graph.checkpoint_graph'	CLI Run (python -m graph.test...)	Path not resolved properly by Python module system	Activated poetry shell, used python -m ... instead of python ...
| 57 |	TypeError: 'NoneType' object is not callable	(not shown, but common)	Usually caused by a missing return in LangGraph edge node function	Checked return statements and ensured correct state propagation
| 58 |	graph_status: failed despite valid ingestion	checkpoint_graph.py	File read success but LLM failed due to hidden token overload	Traced back to model context and added chunking or fallback logic
| 59 | `ModuleNotFoundError: No module named 'security'`                         | `test_safety.py`                  | Python couldn’t recognize folder as module                      | Added `__init__.py` to `security/` folder                                        |
| 60 | `Unsafe prompt not detected for "How to bypass the law"`                  | `pii_filter.py`                   | Phrase not matched by regex or keyword rules                    | Improved regex and keyword filters inside `guardrails.py`                         |
| 61 | `Unsafe question detected: Unsafe content detected`                       | `main.py`                         | Streamlit UI stopped unsafe query from reaching the agent       | Integrated `run_safety_checks()` before invoking agent                            |




---

## ✅ Maintenance Notes
- 📄 This file will be updated every few days or after major integration blocks.
- 🧪 Useful for onboarding contributors or deploying to new environments.
- 📌 Suggest creating a `diagnostics.py` or `health_check.py` for runtime checks.

---

Let’s keep this clean and evolving! ✅
