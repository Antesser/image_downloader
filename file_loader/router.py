from typing import List

import aiofiles
import cv2 as cv
from fastapi import APIRouter, File, UploadFile, status
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/file_ops", tags=["File operations"])


@router.post("/upload_multiple_files/")
async def file_uploader(files: List[UploadFile] = File(...)) -> JSONResponse:
    file_names = []
    try:
        for file in files:
            file_names.append(file.filename)
            path = f"media/{file.filename}"
            async with aiofiles.open(path, "wb") as out_file:
                content = await file.read()
                await out_file.write(content)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": str(e)},
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"result": {"loaded pictures": file_names}},
        )
