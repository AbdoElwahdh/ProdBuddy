from supabase import create_client
import os

supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

async def create_task(user_id, title, description="", due_date=None):
    data, error = supabase.table("tasks").insert({
        "user_id": user_id,
        "title": title,
        "description": description,
        "due_date": due_date
    }).execute()
    if error:
        return {"message": f"Error creating task: {error}"}
    return {"message": f'Task "{title}" created successfully'}