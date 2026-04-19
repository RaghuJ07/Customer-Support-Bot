import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.vectorstores import InMemoryVectorStore
from langchain.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from langchain.messages import HumanMessage
import time
import gradio as gr

load_dotenv()

# Create the state for the whole graph
class State(TypedDict):
    messages: Annotated[list, add_messages]

google_api_key = os.getenv('GOOGLE_API_KEY')

# Integrating with the Google genAI LLM
google_llm = ChatGoogleGenerativeAI(
    model='gemini-2.5-flash',
    api_key=google_api_key,
)

# Converting and loading the data in vectorstore 


def convert_and_load():
    try:
        #  Load PDF
        loader = PyPDFLoader(r'knowleadge\test.pdf')
        docs = loader.load()

        #  Better chunking (IMPORTANT)
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=600,       #bigger chunks
            chunk_overlap=50
        )

        texts = text_splitter.split_text(
            " ".join(doc.page_content for doc in docs)
        )

        # Embedding model
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001"
        )

        # Create vector store manually (batch-safe)
        vector_store = InMemoryVectorStore(embedding=embeddings)

        # Batch + throttle
        BATCH_SIZE = 20  # safe for free tier

        for i in range(0, len(texts), BATCH_SIZE):
            batch = texts[i:i + BATCH_SIZE]

            vector_store.add_texts(batch)

            # ⏳ throttle to avoid 429
            time.sleep(1.2)
        return vector_store

    except Exception as e:
        print(f"Error in converting and loading: {e}")
        return None


# Working with importing, loading, converting the data to embeddings, and storing it
@tool
def retrive_the_data(query: str):
    """Fetch relevant data from the document according to the query. If data not found, return 'no related data in this document'."""
    try:
        retriver = convert_and_load()
        retrived_documents = retriver.similarity_search(query)
        # print(retrived_documents)

        if not retrived_documents:
            return "No related data in this document"
        
        return retrived_documents[0].page_content
    
    except Exception as e:
        print(f'Error in retriving the data and the error is {e}')
        return 'Error while retriving the data'

tools = [retrive_the_data]

def agent_node(state):
    response = google_llm.bind_tools(tools).invoke(state['messages'])
    return {'messages': response}

# Graph creation
builder = StateGraph(State)
builder.add_node("tools", ToolNode(tools))
builder.add_node("agent_node", agent_node)

# Logic
builder.add_edge(START, "agent_node")
builder.add_conditional_edges("agent_node", tools_condition)
builder.add_edge("agent_node", END)

# Compile and run the graph
graph = builder.compile()

while True:
    prompt = input('Ask me if you had any doubts in the polacies from the company:')
    messages = [HumanMessage(content=prompt)]
    response = graph.invoke({"messages": messages})
    # Print the value from the messages response
    print(response["messages"][-1].content)