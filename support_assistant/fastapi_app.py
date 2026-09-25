from fastapi import FastAPI
import os

app = FastAPI()
MOCK_LLM = os.getenv("MOCK_LLM","1")

@app.get("/ask")
def ask(query: str):
    keywords = ["delivery","return","refund","membership","tracking","cancel","gift card","support hours"]
    if any(k in query.lower() for k in keywords):
        intent = "policy_question"
    else:
        intent = "general_question"
    if MOCK_LLM=="1":
        return {"intent":intent,"answer":"[Mock Answer] Based on Zepto policy corpus."}
    else:
        return {"intent":intent,"answer":"[Real LLM call would go here]"}
