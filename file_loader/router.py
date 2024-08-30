import os
from typing import List

import aiofiles
import cv2 as cv
from fastapi import APIRouter, File, UploadFile, status
from fastapi.responses import FileResponse, JSONResponse
import numpy as np

router = APIRouter(prefix="/file_ops", tags=["File operations"])


async def canny(
    content: str, threshold1: int = 0, threshold2: int = 0
) -> None:
    img = cv.imread(f"media/{content}")
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img = cv.Canny(img, threshold1, threshold2)
    cv.imwrite(f"media/with_filters/filtered_{content}", img)
    nparr = np.fromstring(content, np.uint8)
    img = cv.imdecode(nparr, cv.IMREAD_COLOR)

    # Save the image to a file
    save_path = f"media/with_filters/filtered_{file.filename}"
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
            path = f"media/{file.filename}"
            if not os.path.isfile(path):
                file_names.append(file.filename)
                async with aiofiles.open(path, "wb") as out_file:
                    content = await file.read()
                    await out_file.write(content)
                    await canny(file.filename, threshold1, threshold2)
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
# @router.post("/upload_multiple_files/")
# async def files_uploader(
#     files: List[UploadFile] = File(...),
#     threshold1: int = 0,
#     threshold2: int = 0,
# ) -> JSONResponse:
#     file_names = []
#     try:
#         for file in files:
#             path = f"media/{file.filename}"
#             if not os.path.isfile(path):
#                 file_names.append(file.filename)
#             with open(path, "wb"):
#                 content = await file.read()
#                 await canny(content, threshold1, threshold2)
#     except Exception as e:
#         return JSONResponse(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             content={"error_message": str(e)},
#         )
#     else:
#         return JSONResponse(
#             status_code=status.HTTP_200_OK,
#             content={"result": {"loaded pictures": file_names}},
#         )


@router.get("/get_image")
async def file_downloader(file_name: str) -> FileResponse:
    filtered_path = f"media/with_filters/filtered_{file_name}"
    original_path = f"media/{file_name}"
    if os.path.isfile(filtered_path):
        return FileResponse(path=filtered_path)
    elif os.path.isfile(original_path) and not os.path.isfile(filtered_path):
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
