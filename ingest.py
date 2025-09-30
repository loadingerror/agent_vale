from langchain_chroma import Chroma
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv
from uuid import uuid4

load_dotenv('.env')
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

def add_file_paths(embeddings, file_paths):
    def gen_documents(file_paths):
        def get_document(file_path):
            with open(file_path, 'r') as f:
                return [Document(page_content=doc.page_content, 
                                 metadata={"source": file_path}, 
                                 id=str(uuid4())) for doc in SemanticChunker(embeddings).create_documents([f.read()])]
        documents = sum(list(map(get_document, file_paths)), [])
        return documents, [str(uuid4()) for _ in range(len(documents))]
    def add_documents(documents, ids):
        Chroma(collection_name="test_ai",
               embedding_function=embeddings,
               persist_directory="./vector_db").add_documents(documents=documents, ids=ids)
    add_documents(*gen_documents(file_paths))
    
add_file_paths(embeddings,
               ['test.md',
                'requirements.txt'])
