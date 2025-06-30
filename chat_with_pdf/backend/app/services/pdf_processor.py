import os
import uuid
import io
from pypdf import PdfReader
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain_community.vectorstores import FAISS

class PDFProcessor:
    def __init__(self):
        self.embeddings = HuggingFaceInstructEmbeddings(
            model_name="hkunlp/instructor-large",
            model_kwargs={"device": "cpu"}
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )


    def extract_text_with_pages(self, file_content: bytes):
        pdf_stream = io.BytesIO(file_content)        
        reader = PdfReader(pdf_stream)               
        pages = []
        for i, page in enumerate(reader.pages, 1):
            text = page.extract_text() or ""
            if text.strip():
                pages.append((i, text))
        return pages


    def create_chunks_with_metadata(self, pages: list[tuple[int, str]]) -> list[dict]:
        """Split text into chunks with metadata"""
        documents = []
        for page_num, text in pages:
            chunks = self.text_splitter.split_text(text)
            for chunk in chunks:
                documents.append({
                    "text": chunk,
                    "metadata": {"page": page_num, "source": f"page_{page_num}"}
                })
        return documents

    def create_vector_store(self, documents: list[dict]) -> FAISS:
        """Create FAISS vector store from documents"""
        texts = [doc["text"] for doc in documents]
        metadatas = [doc["metadata"] for doc in documents]
        return FAISS.from_texts(texts, self.embeddings, metadatas=metadatas)

    def process_pdf(self, file_content: bytes, filename: str) -> str:
        """Process PDF and return vector store ID"""
        pages = self.extract_text_with_pages(file_content)
        documents = self.create_chunks_with_metadata(pages)
        vector_store = self.create_vector_store(documents)
        
        # Generate unique ID for this document session
        store_id = f"{filename}_{uuid.uuid4().hex}"
        vector_store.save_local(f"vector_stores/{store_id}")
        return store_id
