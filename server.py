from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class SubmitRequest(BaseModel):
    message: str
    runner_id: str

@app.post("/submit")
def submit_result(req: SubmitRequest):
    return {"status": "ok", "message": req.message, "runner_id": req.runner_id}