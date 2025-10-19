import os
import requests
from typing import List, Dict, Any, TypedDict
from langchain_community.document_loaders import TextLoader

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
# 将 OpenAI 嵌入模型替换为 Google Generative AI 嵌入模型
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Weaviate
# 将 OpenAI 模型替换为 Google Generative AI 模型
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough
from langgraph.graph import StateGraph, END
import weaviate
from weaviate.embedded import EmbeddedOptions
import dotenv

# 加载项目配置
import config

dotenv.load_dotenv()

url = "https://github.com/langchain-ai/langchain/blob/master/docs/docs/how_to/state_of_the_union.txt"
res = requests.get(url)

with open("state_of_the_union.txt", "w") as f:
    f.write(res.text)

loader = TextLoader('./state_of_the_union.txt')
documents = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = text_splitter.split_documents(documents)

# 修复 Weaviate v3 客户端初始化方式
client = weaviate.Client(
    embedded_options=EmbeddedOptions()
)

# 使用 Google Generative AI 的嵌入模型替换 OpenAI 的嵌入模型
embedding = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    # google_api_key=config.Config.GOOGLE_API_KEY
)

vectorstore = Weaviate.from_documents(
    client=client,
    documents=chunks,
    embedding=embedding,
    by_text=False
)

retriever = vectorstore.as_retriever()
# 使用 Google Generative AI 模型替换 OpenAI 模型
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=config.Config.GOOGLE_API_KEY,  # 使用配置中的 Google API 密钥
    temperature=0
)

class RAGGraphState(TypedDict):
    question: str
    documents: List[Document]
    generation: str

def retrieve_documents_node(state: RAGGraphState) -> RAGGraphState:
    question = state["question"]
    documents = retriever.invoke(question)
    return {"documents": documents, "question": question, "generation": ""}

def generate_response_node(state: RAGGraphState) -> RAGGraphState:
    question = state["question"]
    documents = state["documents"]

    template = """You are an assistant for question-answering tasks.
                Use the following pieces of retrieved context to answer the question.
                If you don't know the answer, just say that you don't know.
                Use three sentences maximum and keep the answer concise.
                Question: {question}
                Context: {context}
                Answer:
                """
    prompt = ChatPromptTemplate.from_template(template)
    context = "\n\n".join([doc.page_content for doc in documents])
    rag_chain = prompt | llm | StrOutputParser()
    generation = rag_chain.invoke({"context": context, "question": question})
    return {"question": question, "documents": documents, "generation": generation}

workflow = StateGraph(RAGGraphState)
workflow.add_node("retrieve", retrieve_documents_node)
workflow.add_node("generate", generate_response_node)
workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", END)
app = workflow.compile()

if __name__ == "__main__":
    print("\n--- Running RAG Query ---")
    query = "What did the president say about Justice Breyer"
    inputs = {"question": query}
    for s in app.stream(inputs):
        print(s)

    print("\n--- Running another RAG Query ---")
    query_2 = "What did the president say about the economy?"
    inputs_2 = {"question": query_2}
    for s in app.stream(inputs_2):
        print(s)