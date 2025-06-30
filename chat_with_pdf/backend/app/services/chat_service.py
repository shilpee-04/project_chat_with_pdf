from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from app.services.llm_service import LLMService
from typing import List, Dict, Tuple
import os
class ChatService:
    def __init__(self):
        self.embeddings = HuggingFaceInstructEmbeddings(
            model_name="hkunlp/instructor-large",
            model_kwargs={"device": "cpu"}
        )
        self.llm_service = LLMService()
        
    def load_vector_store(self, store_id: str) -> FAISS:
        """Load FAISS vector store by ID"""
        store_path = f"vector_stores/{store_id}"
        if not os.path.exists(store_path):
            raise ValueError(f"Vector store {store_id} not found")
        return FAISS.load_local(store_path, self.embeddings, allow_dangerous_deserialization=True)
    
    def get_relevant_context(self, question: str, store_ids: List[str], mode: str = "multi-turn") -> str:
        """Get relevant context from vector stores"""
        all_docs = []
        
        # Determine number of documents to retrieve based on mode
        k = 5 if mode == "multi-turn" else 10
        
        for store_id in store_ids:
            try:
                vector_store = self.load_vector_store(store_id)
                docs = vector_store.similarity_search(question, k=k)
                all_docs.extend(docs)
            except Exception as e:
                print(f"Error loading store {store_id}: {e}")
                continue
        
        # Format context with page numbers
        context_parts = []
        for doc in all_docs:
            page_num = doc.metadata.get('page', 'Unknown')
            context_parts.append(f"[Page {page_num}]: {doc.page_content}")
        
        return "\n\n".join(context_parts)
    
    def chat(self, question: str, store_ids: List[str], chat_history: List[Dict] = None, mode: str = "multi-turn") -> Tuple[str, str]:
        """Main chat function"""
        try:
            # Get relevant context
            context = self.get_relevant_context(question, store_ids, mode)
            
            if not context:
                return "I cannot find relevant information in the provided documents.", ""
            
            # Generate response
            response = self.llm_service.generate_response(question, context, chat_history)
            
            return response, context
            
        except Exception as e:
            print(f"Chat error: {e}")
            return "Sorry, I encountered an error processing your question.", ""
