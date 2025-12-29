"""
Retrieval Module - Enterprise RAG System
Making AI Simple 

This module provides production-ready retrieval methods:
- BM25 (keyword search)
- Vector search (semantic)
- Hybrid search (combined)
- Re-ranking with cross-encoders

Author: Jyotsna Bulchandani
"""

from typing import List, Dict, Optional
import numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer, CrossEncoder
from sklearn.metrics.pairwise import cosine_similarity


class BM25Retriever:
    """BM25 keyword-based retriever."""
    
    def __init__(self, chunks: List[str]):
        self.chunks = chunks
        tokenized = [chunk.lower().split() for chunk in chunks]
        self.bm25 = BM25Okapi(tokenized)
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        tokenized_query = query.lower().split()
        scores = self.bm25.get_scores(tokenized_query)
        top_indices = np.argsort(scores)[::-1][:top_k]
        
        return [
            {"index": int(idx), "chunk": self.chunks[idx], "score": float(scores[idx])}
            for idx in top_indices
        ]


class VectorRetriever:
    """Semantic vector-based retriever."""
    
    def __init__(
        self, 
        chunks: List[str], 
        model_name: str = "all-MiniLM-L6-v2"
    ):
        self.chunks = chunks
        self.model = SentenceTransformer(model_name)
        self.embeddings = self.model.encode(chunks, show_progress_bar=True)
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        query_embedding = self.model.encode([query])
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        return [
            {"index": int(idx), "chunk": self.chunks[idx], "score": float(similarities[idx])}
            for idx in top_indices
        ]


class HybridRetriever:
    """
    Hybrid retriever combining BM25 and vector search.
    
    Args:
        chunks: List of text chunks
        bm25_weight: Weight for BM25 scores (0-1). Vector weight = 1 - bm25_weight
        model_name: Sentence transformer model for embeddings
    """
    
    def __init__(
        self,
        chunks: List[str],
        metadata: Optional[List[Dict]] = None,
        bm25_weight: float = 0.3,
        model_name: str = "all-MiniLM-L6-v2"
    ):
        self.chunks = chunks
        self.metadata = metadata or [{"index": i} for i in range(len(chunks))]
        self.bm25_weight = bm25_weight
        
        # Initialize BM25
        tokenized = [chunk.lower().split() for chunk in chunks]
        self.bm25 = BM25Okapi(tokenized)
        
        # Initialize vector search
        self.embed_model = SentenceTransformer(model_name)
        self.embeddings = self.embed_model.encode(chunks, show_progress_bar=True)
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Hybrid search combining BM25 and vector similarity."""
        
        # BM25 scores
        tokenized_query = query.lower().split()
        bm25_scores = self.bm25.get_scores(tokenized_query)
        bm25_max = max(bm25_scores) + 1e-6
        bm25_normalized = bm25_scores / bm25_max
        
        # Vector scores
        query_embedding = self.embed_model.encode([query])
        vector_scores = cosine_similarity(query_embedding, self.embeddings)[0]
        
        # Combined scores
        combined_scores = (
            self.bm25_weight * bm25_normalized +
            (1 - self.bm25_weight) * vector_scores
        )
        
        top_indices = np.argsort(combined_scores)[::-1][:top_k]
        
        return [
            {
                "index": int(idx),
                "chunk": self.chunks[idx],
                "metadata": self.metadata[idx],
                "bm25_score": float(bm25_normalized[idx]),
                "vector_score": float(vector_scores[idx]),
                "combined_score": float(combined_scores[idx])
            }
            for idx in top_indices
        ]


class ReRanker:
    """Cross-encoder re-ranker for improved precision."""
    
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model = CrossEncoder(model_name)
    
    def rerank(self, query: str, results: List[Dict], top_k: int = 5) -> List[Dict]:
        """
        Re-rank results using cross-encoder.
        
        Args:
            query: Search query
            results: List of result dicts with 'chunk' key
            top_k: Number of results to return after re-ranking
        """
        if not results:
            return []
        
        pairs = [[query, r["chunk"]] for r in results]
        scores = self.model.predict(pairs)
        
        for i, result in enumerate(results):
            result["rerank_score"] = float(scores[i])
        
        reranked = sorted(results, key=lambda x: x["rerank_score"], reverse=True)
        return reranked[:top_k]


class ProductionRAG:
    """
    Production-ready RAG system with hybrid search and re-ranking.
    
    This is the main class to use for production deployments.
    
    Example:
        rag = ProductionRAG(chunks, metadata)
        results = rag.search("What is the PTO policy?")
        prompt = rag.build_prompt("What is the PTO policy?", results)
    """
    
    def __init__(
        self,
        chunks: List[str],
        metadata: Optional[List[Dict]] = None,
        bm25_weight: float = 0.35,
        embed_model: str = "all-MiniLM-L6-v2",
        rerank_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    ):
        self.hybrid = HybridRetriever(
            chunks=chunks,
            metadata=metadata,
            bm25_weight=bm25_weight,
            model_name=embed_model
        )
        self.reranker = ReRanker(model_name=rerank_model)
    
    def search(
        self,
        query: str,
        top_k: int = 5,
        candidates: int = 20,
        use_reranking: bool = True
    ) -> List[Dict]:
        """
        Search with hybrid retrieval and optional re-ranking.
        
        Args:
            query: Search query
            top_k: Final number of results
            candidates: Number of candidates for re-ranking
            use_reranking: Whether to use cross-encoder re-ranking
        """
        # Get candidates from hybrid search
        results = self.hybrid.search(query, top_k=candidates if use_reranking else top_k)
        
        # Re-rank if requested
        if use_reranking:
            results = self.reranker.rerank(query, results, top_k=top_k)
        
        return results
    
    def build_prompt(
        self,
        query: str,
        results: List[Dict],
        system_prompt: Optional[str] = None
    ) -> str:
        """Build prompt with retrieved context for LLM."""
        
        context = "\n\n---\n\n".join([r["chunk"] for r in results])
        
        default_system = """Answer the question based on the provided context.
If the answer is not in the context, say "I don't have information about that."
Be concise and cite relevant details from the context."""
        
        return f"""{system_prompt or default_system}

CONTEXT:
{context}

QUESTION: {query}

ANSWER:"""
    
    def query(self, question: str, top_k: int = 3) -> Dict:
        """
        Full RAG query: search + build prompt.
        
        Returns dict with prompt, results, and sources.
        """
        results = self.search(question, top_k=top_k)
        prompt = self.build_prompt(question, results)
        sources = list(set(r.get("metadata", {}).get("source", "unknown") for r in results))
        
        return {
            "prompt": prompt,
            "results": results,
            "sources": sources,
            "query": question
        }


# Convenience function for quick setup
def create_rag_system(
    chunks: List[str],
    metadata: Optional[List[Dict]] = None,
    **kwargs
) -> ProductionRAG:
    """
    Factory function to create a ProductionRAG instance.
    
    Args:
        chunks: List of text chunks
        metadata: Optional metadata for each chunk
        **kwargs: Additional arguments for ProductionRAG
    
    Returns:
        Configured ProductionRAG instance
    """
    return ProductionRAG(chunks=chunks, metadata=metadata, **kwargs)


if __name__ == "__main__":
    # Quick test
    test_chunks = [
        "Python is a programming language known for its simple syntax.",
        "Machine learning is a subset of artificial intelligence.",
        "RAG combines retrieval with generation for better AI responses.",
        "The employee handbook contains PTO and benefits information.",
        "Security incidents should be reported to the security team immediately."
    ]
    
    test_metadata = [{"id": i, "source": "test"} for i in range(len(test_chunks))]
    
    print("Testing ProductionRAG...")
    rag = ProductionRAG(test_chunks, test_metadata)
    
    results = rag.search("How do I report security issues?", top_k=2)
    print(f"\nQuery: 'How do I report security issues?'")
    print(f"Top result: {results[0]['chunk'][:50]}...")
    print(f"Rerank score: {results[0].get('rerank_score', 'N/A')}")
    
    print("\n ProductionRAG test passed!")
