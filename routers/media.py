from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
import cloudinary.uploader
import cloudinary.api
from core.security import verify_token
from schemas.media import ImageItem, DeleteImageRequest, MoveImageRequest, ActionResponse
import db.cloudinary_client  # ensures initialization

router = APIRouter(tags=["Media"])


@router.get("/images", response_model=List[ImageItem])
async def list_images(folder: Optional[str] = "", user=Depends(verify_token)):
    try:
        folder_clean = (folder or "").strip().strip("/")
        prefix = f"{folder_clean}/" if folder_clean else ""

        res = cloudinary.api.resources(
            type="upload",
            prefix=prefix,
            max_results=500
        )

        images = []
        for resource in res.get("resources", []):
            public_id = resource.get("public_id", "")
            rel_id = public_id[len(prefix):] if prefix and public_id.startswith(prefix) else public_id
            if "/" in rel_id:
                continue

            name = public_id.split("/")[-1]
            images.append(ImageItem(
                key=public_id,
                url=resource.get("secure_url"),
                name=name,
                size=resource.get("bytes", 0),
                uploadedAt=resource.get("created_at", "")
            ))
        return images
    except Exception:
        return []


@router.post("/upload", response_model=ImageItem)
async def upload_image(
    file: UploadFile = File(...),
    folder: Optional[str] = Form(""),
    user=Depends(verify_token)
):
    try:
        folder_clean = (folder or "").strip().strip("/")
        res = cloudinary.uploader.upload(
            file.file,
            folder=folder_clean if folder_clean else None,
            use_filename=True,
            unique_filename=True,
            resource_type="auto"
        )
        public_id = res.get("public_id", "")
        return ImageItem(
            key=public_id,
            url=res.get("secure_url"),
            name=public_id.split("/")[-1],
            size=res.get("bytes", 0),
            uploadedAt=res.get("created_at", "")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao enviar arquivo para o Cloudinary: {str(e)}")


@router.delete("/images", response_model=ActionResponse)
async def delete_image(req: DeleteImageRequest, user=Depends(verify_token)):
    try:
        cloudinary.uploader.destroy(req.key)
        return ActionResponse(success=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar imagem no Cloudinary: {str(e)}")


@router.patch("/images", response_model=ImageItem)
async def move_image(req: MoveImageRequest, user=Depends(verify_token)):
    try:
        old_key = req.key
        target_folder = req.targetFolder.strip().strip("/")
        filename = old_key.split("/")[-1]
        new_key = f"{target_folder}/{filename}" if target_folder else filename

        res = cloudinary.uploader.rename(old_key, new_key, overwrite=True)
        return ImageItem(
            key=new_key,
            url=res.get("secure_url"),
            name=filename,
            size=res.get("bytes", 0),
            uploadedAt=res.get("created_at", "")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao mover imagem no Cloudinary: {str(e)}")
