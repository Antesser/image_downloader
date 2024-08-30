import os
from typing import List

import aiofiles
import cv2 as cv
import numpy as np
from fastapi import APIRouter, File, Request, UploadFile, status
from fastapi.responses import FileResponse, JSONResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/file_ops", tags=["File operations"])

templates = Jinja2Templates(directory="templates")

filtered_files_name = "media/with_filters/filtered_"
filtered_path = "media/with_filters/"
original_path = "media/"


@router.get("/upload")
def upload_files(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@router.get("/download")
def download_files(request: Request):
    return templates.TemplateResponse("download.html", {"request": request})


async def canny(
    file: UploadFile,
    content: str,
    first_threshold: int = 0,
    second_threshold: int = 0,
) -> None:
    save_path = "".join([filtered_files_name, file.filename])
    nparr = np.fromstring(content, np.uint8)
    img = cv.imdecode(nparr, cv.IMREAD_COLOR)
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img = cv.Canny(img, first_threshold, second_threshold)
    cv.imwrite(save_path, img)


@router.post("/upload_multiple_files/")
async def files_uploader(
    files: List[UploadFile] = File(...),
    first_threshold: int = 0,
    second_threshold: int = 0,
) -> JSONResponse:
    file_names = []
    try:
        for file in files:
            path = "".join([original_path, file.filename])
            if not os.path.isfile(path):
                file_names.append(file.filename)
                async with aiofiles.open(path, "wb") as out_file:
                    content = await file.read()
                    await canny(
                        file,
                        content,
                        first_threshold,
                        second_threshold,
                    )
                    # saving an original img
                    await out_file.write(content)

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error_message": str(e)},
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"loaded pictures": file_names},
        )


@router.get("/get_image")
async def file_downloader(file_name: str) -> FileResponse:
    f_path = "".join([filtered_files_name, file_name])
    filtered_files = os.listdir(filtered_path)
    o_path = "".join([original_path, file_name])
    for file in filtered_files:
        if f_path.split(sep="/")[-1] not in file.split(".")[:-1][
            0
        ] and os.path.isfile(o_path + "." + file.split(".")[-1]):
            return JSONResponse(
                status_code=200,
                content={
                    "message": f"pls wait, filtered picture {file_name} is being processed"
                },
            )
        if f_path.split(sep="/")[-1] == file.split(".")[:-1][
            0
        ] and os.path.isfile(filtered_path + file):
            return FileResponse(filtered_path + file)

    else:
        return JSONResponse(
            status_code=404,
            content={
                "message": f"picture {file_name} hasn`t been previously loaded, check provided name"
            },
        )
