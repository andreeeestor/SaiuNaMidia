from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
import cloudinary.api
from core.security import verify_token
from schemas.folder import FolderItem, CreateFolderRequest, CreateFolderResponse
import db.cloudinary_client  # ensures initialization

router = APIRouter(prefix="/folders", tags=["Folders"])


@router.get("", response_model=List[FolderItem])
async def list_folders(parent: Optional[str] = "", user=Depends(verify_token)):
    try:
        parent_clean = (parent or "").strip().strip("/")
        if parent_clean:
            res = cloudinary.api.sub_folders(parent_clean)
        else:
            res = cloudinary.api.root_folders()

        folders = []
        for f in res.get("folders", []):
            folders.append(FolderItem(name=f.get("name"), path=f.get("path")))
        return folders
    except Exception:
        return []


@router.post("", response_model=CreateFolderResponse)
async def create_folder(req: CreateFolderRequest, user=Depends(verify_token)):
    path_clean = req.path.strip().strip("/")
    if not path_clean:
        raise HTTPException(status_code=400, detail="Caminho da pasta é obrigatório")
    try:
        cloudinary.api.create_folder(path_clean)
        return CreateFolderResponse(success=True, path=path_clean)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar pasta no Cloudinary: {str(e)}")
