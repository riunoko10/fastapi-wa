from fastapi import FastAPI, Request, Response, Query
from fastapi.responses import HTMLResponse, PlainTextResponse
import uvicorn
from typing import Optional
from dotenv import load_dotenv
import os

load_dotenv()

os.environ["GRAPH_API_TOKEN"] = os.getenv("GRAPH_API_TOKEN")
os.environ["WEBHOOK_VERIFY_TOKEN"] = os.getenv("WEBHOOK_VERIFY_TOKEN")


app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    return 'Simple WhatsApp Webhook tester</br>There is no front-end, see main.py for implementation!'

@app.get("/webhook")
async def verify_webhook(
    hub_mode: str = Query(..., alias="hub.mode"),
    hub_verify_token: str = Query(..., alias="hub.verify_token"),
    hub_challenge: str = Query(..., alias="hub.challenge")
):
    if hub_mode == 'subscribe' and hub_verify_token == os.getenv("WEBHOOK_VERIFY_TOKEN"):
        return PlainTextResponse(content=hub_challenge)
    return Response(status_code=400)

@app.post("/webhook")
async def webhook(request: Request):
    body = await request.json()
    print(body)
    print('Incoming webhook: ' + str(body))
    return Response(status_code=200)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
