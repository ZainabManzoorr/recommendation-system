from uuid import uuid4
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.supabase_services import supabase

router = APIRouter()

@router.post("/upload-avatar/{user_id}")
async def upload_avatar(user_id: str, file: UploadFile = File(...)):
    try:
        contents = await file.read()
        file_ext = file.filename.split(".")[-1]
        unique_filename = f"{uuid4().hex}.{file_ext}"
        file_path = f"{user_id}/{unique_filename}"

        # Upload (overwrite if exists)
        supabase.storage.from_("avatars").update(
            file_path,
            contents,
            {"content-type": file.content_type}
        )

        # Get public URL
        public_url = supabase.storage.from_("avatars").get_public_url(file_path)

        # Save URL to user record
        supabase.table("users").update({
            "avatar_url": public_url
        }).eq("id", user_id).execute()

        return {"message": "Avatar uploaded successfully", "avatar_url": public_url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
