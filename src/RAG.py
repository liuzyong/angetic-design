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
# OpenAI 模型（备选方案）
from langchain_community.embeddings import OpenAIEmbeddings
# Ollama 嵌入模型（本地部署方案）
from langchain_ollama import OllamaEmbeddings
from langchain_openai import ChatOpenAI
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

def create_embedding_model():
    """创建嵌入模型，优先使用 Google 模型，失败则回退到 Ollama 或 OpenAI"""
    try:
        # 尝试使用 Google Generative AI 的嵌入模型
        if config.Config.GOOGLE_API_KEY:
            # 在程序中设置 Google 嵌入模型的地址和其他客户端选项
            embedding = GoogleGenerativeAIEmbeddings(
                model="models/embedding-001",
                google_api_key=config.Config.GOOGLE_API_KEY,
                # 设置自定义端点（如果需要）
                # client_options={"api_endpoint": "generativelanguage.googleapis.com"},
                # 使用 REST 传输而不是 gRPC（如果需要）
                # transport="rest",
                # 设置超时时间
                timeout=120
            )
            # 测试模型是否可用
            embedding.embed_query("test")
            print("✓ 使用 Google Generative AI 嵌入模型")
            return embedding
    except Exception as e:
        print(f"✗ Google Generative AI 嵌入模型不可用: {e}")
    
    try:
        # 尝试使用 Ollama 的嵌入模型（本地部署）
        embedding = OllamaEmbeddings(
            model="nomic-embed-text",  # Ollama 默认的嵌入模型
            # 如果 Ollama 运行在不同的地址，可以指定 base_url
            # base_url="http://localhost:11434"
        )
        # 测试模型是否可用
        embedding.embed_query("test")
        print("✓ 使用 Ollama 嵌入模型")
        return embedding
    except Exception as e:
        print(f"✗ Ollama 嵌入模型不可用: {e}")
    
    try:
        # 回退到 OpenAI 的嵌入模型
        if config.Config.OPENAI_API_KEY:
            embedding = OpenAIEmbeddings(
                openai_api_key=config.Config.OPENAI_API_KEY,
                openai_api_base=config.Config.OPENAI_BASE_URL
            )
            print("✓ 使用 OpenAI 嵌入模型")
            return embedding
    except Exception as e:
        print(f"✗ OpenAI 嵌入模型不可用: {e}")
    
    raise Exception("无法初始化任何嵌入模型")

def create_llm_model():
    """创建语言模型，优先使用 Google 模型，失败则回退到 OpenAI"""
    try:
        # 尝试使用 Google Generative AI 模型
        if config.Config.GOOGLE_API_KEY:
            llm = ChatGoogleGenerativeAI(
                model="gemini-pro",
                google_api_key=config.Config.GOOGLE_API_KEY,
                temperature=0,
                # 同样可以设置 Google 语言模型的客户端选项
                # client_options={"api_endpoint": "generativelanguage.googleapis.com"},
                # transport="rest",
                timeout=120
            )
            print("✓ 使用 Google Generative AI 语言模型")
            return llm
    except Exception as e:
        print(f"✗ Google Generative AI 语言模型不可用: {e}")
    
    try:
        # 回退到 OpenAI 模型
        if config.Config.OPENAI_API_KEY:
            llm = ChatOpenAI(
                model_name=config.Config.OPENAI_MODEL,
                temperature=0,
                openai_api_key=config.Config.OPENAI_API_KEY,
                openai_api_base=config.Config.OPENAI_BASE_URL
            )
            print("✓ 使用 OpenAI 语言模型")
            return llm
    except Exception as e:
        print(f"✗ OpenAI 语言模型不可用: {e}")
    
    raise Exception("无法初始化任何语言模型")

# 创建嵌入模型
embedding = create_embedding_model()

vectorstore = Weaviate.from_documents(
    client=client,
    documents=chunks,
    embedding=embedding,
    by_text=False
)

retriever = vectorstore.as_retriever()

# 创建语言模型
llm = create_llm_model()

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