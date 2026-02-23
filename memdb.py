from fastapi.responses import JSONResponse
from langchain_aws import BedrockEmbeddings
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from vector_store import MemoryDBStore

def get_embeddings_function() -> BedrockEmbeddings:
    embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0")
    return embeddings

app = FastAPI()
vector_store = MemoryDBStore()

@app.post("/upload")
async def upload(txt: str):
    try:
        ids = vector_store.add(txt)
        if not ids:
            return HTTPException(status_code=500, detail="Unable to add texts")
        return JSONResponse(content={
            "message": "Uploaded successfully",
            "ids": ids
        })
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Unknown error: {e}")


@app.post("/search")
async def search(query: str):
    try:
        res = vector_store.search(query)
        return JSONResponse(content={
            "message": "Search successfull",
            "docs": res
        })
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Unknown error: {e}")

@app.post("/search-with-filter")
async def search_with_filter(query: str, filter: str):
    try:
        res = vector_store.search_with_filter(query, filter)
        return JSONResponse(content={
            "message": "Search with filter successful",
            "docs": res
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Unknown error: {e}"})
