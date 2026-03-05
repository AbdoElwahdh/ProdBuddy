from supabase import create_client
import os

supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

async def list_tasks(user_id):
    data, error = supabase.table("tasks").select("*").eq("user_id", user_id).execute()
    if error:
        return {"message": f"Error fetching tasks: {error}"}
    return {"tasks": data}