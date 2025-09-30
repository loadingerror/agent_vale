import json
import uvicorn
from fastapi import FastAPI, Request
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.runnables import RunnableConfig
from uuid import uuid4
from dotenv import load_dotenv
from graph import gen_graph
from tools import AIToolKit
from langchain_chroma import Chroma
from langchain_core.tracers import LangChainTracer

load_dotenv('.env')

# FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

def sse_format(payload):
    return f"data: {json.dumps(payload)}\n\n"

llm = ChatOpenAI(model="gpt-4o-mini", callbacks=[LangChainTracer()])
v_store = Chroma(
    collection_name="test_ai",
    embedding_function=OpenAIEmbeddings(model="text-embedding-3-large"),
    persist_directory="./vector_db",
)
tools = AIToolKit.from_llm(llm).get_tools()
graph = gen_graph(v_store, llm.bind_tools(tools), tools)

@app.post("/generate")
async def generate_content(request: Request):
    data = await request.json()
    async def stream_generator():
        async for msg, metadata in graph.astream(
            {'messages': data.get('messages', [])},
            stream_mode="messages",
            config=RunnableConfig(configurable={"thread_id": uuid4()})
        ):
            match metadata["langgraph_node"]:
                case "agent":
                    if msg.content:
                        print(f"AGENT: {msg.content}")
                    yield sse_format(
                        {"content": msg.content, "type": "agent"}
                    )
                case "tools":
                    if msg.content:
                        print(f"TOOLS: {msg}")

    return StreamingResponse(stream_generator(), media_type="text/event-stream")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
