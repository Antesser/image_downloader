import os
from typing import List

import aiofiles
import cv2 as cv
from fastapi import APIRouter, File, UploadFile, status
from fastapi.responses import FileResponse, JSONResponse
import numpy as np

router = APIRouter(prefix="/file_ops", tags=["File operations"])


filtered_path = "media/with_filters/filtered_"
original_path = "media/"


async def canny(
    file: UploadFile, content: str, threshold1: int = 0, threshold2: int = 0
) -> None:
    save_path = "".join([filtered_path, file.filename])
    nparr = np.fromstring(content, np.uint8)
    img = cv.imdecode(nparr, cv.IMREAD_COLOR)
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img = cv.Canny(img, threshold1, threshold2)
    cv.imwrite(save_path, img)


@router.post("/upload_multiple_files/")
async def files_uploader(
    files: List[UploadFile] = File(...),
    threshold1: int = 0,
    threshold2: int = 0,
) -> JSONResponse:
    file_names = []
    try:
        for file in files:
            path = "".join([original_path, file.filename])
            print(path)
            if not os.path.isfile(path):
                file_names.append(file.filename)
                async with aiofiles.open(path, "wb") as out_file:
                    content = await file.read()
                    await canny(
                        file,
                        content,
                        threshold1,
                        threshold2,
                    )
                    await out_file.write(content)

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error_message": str(e)},
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"result": {"loaded pictures": file_names}},
        )


@router.get("/get_image")
async def file_downloader(file_name: str) -> FileResponse:
    f_path = "".join([filtered_path, file_name])
    o_path = "".join([original_path, file_name])
    if os.path.isfile(f_path):
        return FileResponse(f_path)
    elif os.path.isfile(o_path) and not os.path.isfile(f_path):
        return JSONResponse(
            status_code=200,
            content={
                "message": f"pls wait, filtered picture {file_name} is being processed"
            },
        )
    else:
        return JSONResponse(
            status_code=404,
            content={
                "message": f"picture {file_name} hasn`t been previously loaded, check provided name"
            },
        )
