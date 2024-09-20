from fastapi import UploadFile
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import os
from app.utils.error_handlers import PDFProcessingError
from app.utils.logger import structlog
from app.config.env_manager import get_settings

logger = structlog.get_logger(__name__)
env_settings = get_settings()

class DocumentProcessor:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(model=env_settings.EMBEDDING_MODEL)

    def process_pdf(self, pdf_file: UploadFile) -> FAISS:
        try:
            with open("temp.pdf", "wb") as temp_file:
                temp_file.write(pdf_file.file.read())
            
            loader = PyPDFLoader("temp.pdf")
            documents = loader.load()
            
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            texts = text_splitter.split_documents(documents)
            
            vector_db = FAISS.from_documents(texts, self.embeddings)
            
            os.remove("temp.pdf")
            
            return vector_db
        except Exception as e:
            logger.error(e)
            raise PDFProcessingError(str(e))

    def get_relevant_context(self, vector_db: FAISS, question: str, k: int = 3) -> str:
        docs = vector_db.similarity_search(question, k=k)
        return " ".join([doc.page_content for doc in docs])