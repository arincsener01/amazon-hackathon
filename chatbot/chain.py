from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain.chains import LLMChain

PROMPT_TEMPLATE = """You are expected to help software engineers by providing them useful tips. You will be asked questions about codebase, you should give detailed explanations by using the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {question}
Answer:"""
PROMPT = PromptTemplate(
    template=PROMPT_TEMPLATE, input_variables=["context", "question"]
)

JIRA_TEMPLATE = """You are expected to help software engineers by providing them useful tips. A Jira task's description and snippets from our codebase will be shared with you, you should give detailed explanations by using the following pieces of context (code snippets) to explain how to implement the jira task. If you don't know the answer, just say that you don't know, don't try to make up an answer.`

{context}

Jira Task: {jira_task}
Answer:"""
JIRA_PROMPT = PromptTemplate(
    template=JIRA_TEMPLATE, input_variables=["context", "jira_task"]
)


SUMMARIZE_PROMPT_TEMPLATE = """
Summarize the following text in 1-2 sentences. Use first person narrative. Just give a summarization, nothing else.

Example:

text: "This feature will allow uses to delete business asset. 
On the business asset detail view you can select “Delete” from the action icon. 
Deleting is only possible with “double confirmation”
Deleting a business asset, will also automatically reset the bookkeeping and VAT category of the linked transaction (we already have this logic for the backoffice)
"

summary:"I need to allow users to delete business assets by adding a Delete action on asset detail view and it should only be possible with double comfirmation. When deleting asset, it should automatically reset the bookkeping and VAT category of the linked transaction."

text:

{jira_description}

summary:"""

SUMMARIZE_PROMPT = PromptTemplate(
    template=SUMMARIZE_PROMPT_TEMPLATE, input_variables=["jira_description"]
)


def get_default_chain():
    return load_qa_chain(
        ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k"),
        chain_type="stuff",
        prompt=PROMPT,
    )


def get_summarize_chain():
    return LLMChain(llm=ChatOpenAI(model="gpt-3.5-turbo"), prompt=SUMMARIZE_PROMPT)


def get_jira_chain():
    return load_qa_chain(
        ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k"),
        chain_type="stuff",
        prompt=JIRA_PROMPT,
    )