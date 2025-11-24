import os
from typing import List
# from langchain.vectorstores import Chroma
# from langchain.embeddings import OpenAIEmbeddings
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.document_loaders import GenericLoader
# from langchain.document_loaders.parsers import LanguageParser

class RAGMemory:
    """
    'RAG Memory' System.
    Personalized AI that learns from user's old code.
    """

    def __init__(self, user_id: str):
        self.user_id = user_id
        self.persist_directory = f"./db/chroma/{user_id}"
        # self.embeddings = OpenAIEmbeddings()
        # self.vectorstore = None

    def ingest_codebase(self, zip_file_path: str):
        """
        Ingests a zip file of code, chunks it, and stores it in ChromaDB.
        """
        # 1. Unzip file (Mocked)
        extracted_path = f"./temp/{self.user_id}/code"
        
        # 2. Load and Split Code
        # loader = GenericLoader.from_filesystem(
        #     extracted_path,
        #     glob="**/*",
        #     suffixes=[".py", ".js"],
        #     parser=LanguageParser()
        # )
        # documents = loader.load()
        # splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        # texts = splitter.split_documents(documents)
        
        # 3. Store in Vector DB
        # self.vectorstore = Chroma.from_documents(
        #     documents=texts, 
        #     embedding=self.embeddings, 
        #     persist_directory=self.persist_directory
        # )
        # self.vectorstore.persist()
        
        print(f"Ingested codebase for user {self.user_id}")
        return {"status": "success", "message": "Codebase ingested and indexed."}

    def search_patterns(self, query: str) -> List[str]:
        """
        Searches the vector store for relevant code patterns.
        """
        # if not self.vectorstore:
        #     self.vectorstore = Chroma(persist_directory=self.persist_directory, embedding_function=self.embeddings)
            
        # docs = self.vectorstore.similarity_search(query, k=3)
        # return [doc.page_content for doc in docs]
        
        # Mock Return
        return [
            "def old_function():\n    # User prefers 4 spaces indentation",
            "class LegacyAuth:\n    # User uses JWT tokens"
        ]
