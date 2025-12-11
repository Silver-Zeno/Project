import json
import os

import httpx
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

app = FastAPI()


LAN_TOKEN = os.getenv("LAN_TOKEN")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_URL = "http://localhost:11434/api/chat"


@app.post("/api/chat")
async def chat(request: Request):
    body = await request.json()

    
    if LAN_TOKEN:
        incoming = request.headers.get("x-lan-token")
        if incoming != LAN_TOKEN:
            return {"error": "Unauthorized"}

    async def stream():
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream("POST", OLLAMA_URL, json=body) as response:
                async for chunk in response.aiter_text():
                    for line in chunk.splitlines():

                        if not line.strip():
                            continue
                        try:
                            data = json.loads(line)
                        except json.JSONDecodeError:
                            
                            yield line
                            continue

                        
                        if data.get("error"):
                            yield f"Error: {data['error']}"
                            continue

                        content = data.get("message", {}).get("content")
                        if content:
                            yield content

    return StreamingResponse(stream(), media_type="text/plain")
