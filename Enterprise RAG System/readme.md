#  Enterprise RAG System

**Building a Production-Grade RAG System in 7 Days**

Part of the [Making AI Simple](https://www.linkedin.com/in/jyotsnabulchandani/) series.


## What We're Building

A complete, production-ready Retrieval-Augmented Generation (RAG) system that goes far beyond basic tutorials:

| Day | Topic | What You'll Learn |
|-----|-------|-------------------|
| [Day 1](notebooks/day_12_rag_fundamentals.ipynb) | RAG Fundamentals | Chunking, embeddings, vector search, basic pipeline |
| [Day 2](notebooks/day_13_hybrid_search.ipynb) | Hybrid Search | BM25 + vectors, cross-encoder re-ranking |
| [Day 3](notebooks/day_14_advanced_patterns.ipynb) | Advanced Patterns | HyDE, Self-RAG, Corrective RAG |
| [Day 4](notebooks/day_15_graphrag.ipynb) | GraphRAG | Knowledge graphs, Neo4j, entity extraction |
| [Day 5](notebooks/day_16_multimodal_rag.ipynb) | Multi-modal RAG | PDFs, tables, images, vision models |
| [Day 6](notebooks/day_17_production_deployment.ipynb) | Production Deployment | Azure AI Search, Terraform, FastAPI |
| [Day 7](notebooks/day_18_evaluation.ipynb) | Evaluation & Monitoring | RAGAS, A/B testing, live dashboard |


## Quick Start

### Option 1: Run in Google Colab (Recommended)

Each notebook has a "Open in Colab" button. No setup required.

| Day | Colab Link |
|-----|------------|
| Day 12 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1Xp93Bm3IS2KT1YWSwqJ9z-SVbHBZcE3p?usp=sharing) |
| Day 13 | [![Open In Colab](https://colab.research.google.com/drive/1fd0TNVdpcVxcdgt3HVCOR8jmtOd4OhAm?usp=sharinghttps://colab.research.google.com/drive/1fd0TNVdpcVxcdgt3HVCOR8jmtOd4OhAm?usp=sharing) |
| Day 14 | Coming soon |
| Day 15 | Coming soon |
| Day 16 | Coming soon |
| Day 17 | Coming soon |
| Day 18 | Coming soon |

### Option 2: Run Locally

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/enterprise-rag-system.git
cd enterprise-rag-system

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run notebooks
jupyter notebook
```

---

## Project Structure

```
enterprise-rag-system/
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/                          # Sample dataset (TechCorp documentation)
│   ├── raw/                       # Original documents
│   ├── processed/                 # Chunked and embedded
│   └── README.md
│
├── notebooks/                     # Daily Colab notebooks
│   ├── day_12_rag_fundamentals.ipynb
│   ├── day_13_hybrid_search.ipynb
│   ├── day_14_advanced_patterns.ipynb
│   ├── day_15_graphrag.ipynb
│   ├── day_16_multimodal_rag.ipynb
│   ├── day_17_production_deployment.ipynb
│   └── day_18_evaluation.ipynb
│
├── src/                           # Production-ready source code
│   ├── __init__.py
│   ├── chunking.py               # Chunking strategies
│   ├── embeddings.py             # Embedding models
│   ├── retrieval.py              # Retrieval (vector, hybrid, graph)
│   ├── reranking.py              # Cross-encoder re-ranking
│   ├── pipeline.py               # Complete RAG pipeline
│   └── evaluation.py             # RAGAS metrics
│
├── infrastructure/                # Terraform & deployment
│   ├── terraform/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── docker/
│   │   └── Dockerfile
│   └── api/
│       └── main.py               # FastAPI backend
│
├── evaluation/                    # Test datasets & results
│   ├── test_questions.json
│   ├── ground_truth.json
│   └── results/
│
├── docs/                          # Additional documentation
│   ├── architecture.md
│   ├── deployment_guide.md
│   └── troubleshooting.md
│
└── assets/                        # Images, diagrams
    └── rag-architecture.png
```


##  The Dataset: TechCorp Documentation

We use a **consistent fictional dataset** across all 7 days — internal documentation for "TechCorp", a fictional tech company.

**Why this dataset?**
- Realistic enterprise content (HR policies, technical docs, product specs)
- Contains text, tables, org charts — tests multi-modal capabilities
- Has cross-document relationships — tests GraphRAG
- Small enough to run free, complex enough to be realistic

**Included documents:**
- `employee_handbook.md` — HR policies, benefits, leave policies
- `technical_architecture.md` — System design, API documentation
- `product_catalog.pdf` — Product specs with tables and images
- `org_structure.md` — Team structure, reporting lines
- `security_policies.md` — Access controls, compliance requirements


## Tech Stack

| Category | Technologies |
|----------|--------------|
| **Embeddings** | sentence-transformers, OpenAI, Cohere |
| **Vector DBs** | ChromaDB, Pinecone, Weaviate, Azure AI Search |
| **Graph DB** | Neo4j |
| **Frameworks** | LangChain, LlamaIndex |
| **LLMs** | GPT-4, Claude, Llama 3 |
| **Deployment** | Azure, Terraform, Docker, FastAPI |
| **Evaluation** | RAGAS, custom metrics |


## Progress Tracker

- [x] Day 12: RAG Fundamentals ✅
- [ ] Day 13: Hybrid Search & Re-ranking
- [ ] Day 14: Advanced Retrieval Patterns
- [ ] Day 15: GraphRAG with Neo4j
- [ ] Day 16: Multi-modal RAG
- [ ] Day 17: Production Deployment
- [ ] Day 18: Evaluation & Dashboard



## Contributing

Found a bug? Have a better approach? PRs welcome!

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -m 'Add improvement'`)
4. Push (`git push origin feature/improvement`)
5. Open a Pull Request



## License

MIT License — use it, learn from it, build on it.


## Connect

**Author:** [Jyotsna Bulchandani](https://www.linkedin.com/in/jyotsnabulchandani/)

**Series:** Making AI Simple — follow along on LinkedIn

**Questions?** Open an issue or reach out on LinkedIn.



⭐ **Star this repo** if you find it useful — it helps others discover it!
