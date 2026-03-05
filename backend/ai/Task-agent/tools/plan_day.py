from supabase import create_client
import os

supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

async def plan_day(user_id):
    # Simple example: fetch tasks and sort by due date
    data, error = supabase.table("tasks").select("*").eq("user_id", user_id).execute()
    if error:
        return {"message": f"Error planning day: {error}"}
    tasks = sorted(data, key=lambda x: x.get('due_date') or "")
    return {"today_plan": tasks}