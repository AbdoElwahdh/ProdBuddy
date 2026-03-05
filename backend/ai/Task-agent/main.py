from fastapi import FastAPI

app = FastAPI()

# class AgentRequest():
    # message: str

@app.post("/Task-agent")
async def run_agent(message: str):
    # message = request.message
    return {
        "reply": f"I received: {message}"
    }
@app.get("/")
async def root():
    return {"message": "Productivity Copilot AI Agent running"}