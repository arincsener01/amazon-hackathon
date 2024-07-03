from chatbot.chain import get_default_chain, get_summarize_chain
from chatbot.embeddings import get_db
from langchain.vectorstores import Chroma

class Chatbot:

    def __init__(self, codebase):
        self.db: Chroma = get_db(codebase)
        self.retriever = self.db.as_retriever()
        self.retriever.search_kwargs["distance_metric"] = "cos"
        self.retriever.search_kwargs["fetch_k"] = 20
        self.retriever.search_kwargs["maximal_marginal_relevance"] = True
        self.retriever.search_kwargs["k"] = 20
        self.chain = get_default_chain()
        self.summarize_chain = get_summarize_chain()

    def get_response(self, question):
        self.last_question = question
        docs = self.db.similarity_search(question, 10)
        result = self.chain({"input_documents": docs, "question": question}, return_only_outputs=True)
        self.last_answer = result['output_text']
        self.last_related_docs = '\n'.join([doc.metadata['source'] for doc in docs])
        return {'answer': self.last_answer, 'related_docs': self.last_related_docs}
