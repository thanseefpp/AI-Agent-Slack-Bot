import asyncio
import tempfile
import os
from fastapi import UploadFile
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from app.utils.error_handlers import PDFProcessingError
from app.utils.error_handlers import DataHanlderError
from app.utils.caching import get_cache_key, get_cache
from app.utils.logger import structlog
from app.config.env_manager import get_settings

logger = structlog.get_logger(__name__)
env_settings = get_settings()

class DocumentProcessor:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(model=env_settings.EMBEDDING_MODEL)
        self.chunk_size = 1000
        self.chunk_overlap = 100

    async def process_pdf(self, pdf_content: UploadFile) -> FAISS:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
                temp_pdf.write(pdf_content)
                temp_pdf_path = temp_pdf.name
            
            loader = PyPDFLoader(temp_pdf_path)
            documents = await asyncio.to_thread(loader.load)
            
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.chunk_size, 
                chunk_overlap=self.chunk_overlap, 
                separators=["\n\n", "\n", ".", " "]
            )
            texts = await asyncio.to_thread(text_splitter.split_documents, documents)
            
            vector_db = await asyncio.to_thread(FAISS.from_documents, texts, self.embeddings)
            os.unlink(temp_pdf_path)
            return vector_db
        except Exception as e:
            if 'temp_pdf_path' in locals():
                os.unlink(temp_pdf_path)
            logger.error(e)
            raise PDFProcessingError(str(e))

    def get_relevant_context(self, vector_db: FAISS, question: str, k: int = 3) -> str:
        docs = vector_db.similarity_search(question, k=k)
        return " ".join([doc.page_content for doc in docs])
    

async def get_loaded_document(pdf_file: UploadFile) -> FAISS:
    pdf_content = await pdf_file.read()
    if not pdf_content:
        raise DataHanlderError(status_code=400, detail="Empty PDF file")
    document_cache = get_cache()
    cache_key = get_cache_key(pdf_content)
    doc_processor = DocumentProcessor()
    if cache_key in document_cache:
        db = document_cache[cache_key]
    else:
        db = await doc_processor.process_pdf(pdf_content)
        document_cache[cache_key] = db
    return db