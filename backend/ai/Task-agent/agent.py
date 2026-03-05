from agent.prompts.system_prompt import system_prompt
from agent.tools.create_task import create_task
from agent.tools.list_tasks import list_tasks
from agent.tools.plan_day import plan_day
from gemini_adk import GeminiClient  # pseudo-import, adapt to actual ADK client

gemini = GeminiClient(api_key="YOUR_KEY")

async def run_agent(user_id, message):
    prompt = f"{system_prompt}{message}"
    response = await gemini.generate(prompt)
    # Gemini returns JSON with: tool + parameters
    decision = response.json()  # {"intent": "", "tool": "", "parameters": {...}}

    tool = decision.get("tool")
    params = decision.get("parameters", {})

    if tool == "create_task":
        return await create_task(user_id=user_id, **params)
    elif tool == "list_tasks":
        return await list_tasks(user_id=user_id)
    elif tool == "plan_day":
        return await plan_day(user_id=user_id)
    else:
        return {"message": "Sorry, I couldn't understand the request."}