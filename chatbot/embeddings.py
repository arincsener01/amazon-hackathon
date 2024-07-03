from langchain.document_loaders import TextLoader
import fnmatch
import os
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

LOCAL_PATH = r"c:\\Users\\sener\\OneDrive\\Masaüstü\\Javascript\\backend\\"
PROJECT_DIRS = {
    "API-Project": f"{LOCAL_PATH}API-Project",
    # Add other projects here
    
}

BLACKLIST_DIRS = ["**/dist/*", "**/node_modules/*", "**/build/*", "**/public/*"]

def get_docs(codebase, file_names=[".tsx", ".ts", ".js"]):
    docs = []
    project_dir = PROJECT_DIRS.get(codebase)
    if not project_dir:
        return docs

    for dirpath, dirnames, filenames in os.walk(project_dir):
        dirnames[:] = [
            d
            for d in dirnames
            if not any(
                fnmatch.fnmatch(os.path.join(dirpath, d), pattern)
                for pattern in BLACKLIST_DIRS
            )
        ]
        for file in filenames:
            if file.endswith(tuple(file_names)) and not any(
                fnmatch.fnmatch(os.path.join(dirpath, file), pattern)
                for pattern in BLACKLIST_DIRS
            ):
                try:
                    loader = TextLoader(
                        os.path.join(dirpath, file), encoding="utf-8"
                    )
                    loaded = loader.load_and_split()
                    for doc in loaded:
                        doc.metadata["source"] = doc.metadata["source"].replace(
                            LOCAL_PATH, ""
                        )
                    docs.extend(loaded)
                except Exception as e:
                    print(f"Error while loading {file}: {e}")
    print(f"Loaded {len(docs)} documents for codebase {codebase}")
    return docs

def get_splitted_texts(codebase):
    docs = get_docs(codebase)
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    return text_splitter.split_documents(docs)

def get_db(codebase, create_new=False):
    db_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), f"chroma-db-docs-{codebase}")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(persist_directory=db_path, embedding_function=embeddings)
    if create_new:
        docs = get_docs(codebase)
        db.add_documents(docs)
        db.persist()
    return db
