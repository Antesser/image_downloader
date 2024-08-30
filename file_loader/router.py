import os
from typing import Dict, List

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
                    await add_filters(
                        file,
                        content,
                        first_threshold,
                        second_threshold,
                    )
                    # saving an original img
                    await out_file.write(content)
            else:
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content={
                        "files": f"{file.filename} have already been loaded"
                    },
                )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error_message": str(e)},
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"loaded_pictures": file_names},
        )


@router.get("/get_image")
async def file_downloader(file_name: str) -> FileResponse:
    """the main difficulty with this endpoint was implementation of
    file name usage in order to download required file without
    bothering about it's extensions
    """
    f_path = "".join([filtered_files_name, file_name])
    o_path = "".join([original_path, file_name])
    filtered_files = await create_dict(filtered_path)
    original_files = await create_dict(original_path)

    # we basically compare original files and filtered ones, if we have both - bingo
    for file in filtered_files:
        if f_path.split(sep="/")[-1] in file.split(".")[
            :-1
        ] and os.path.isfile(filtered_path + "".join(file)):
            return FileResponse(filtered_path + "".join(file))
    # if we have only one - meaning smt went wrong with filtering/it takes some time to finish
    for file in original_files:
        if o_path.split(sep="/")[-1] in file.split(".")[
            :-1
        ] and os.path.isfile(original_path + "".join(file)):
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


async def create_dict(path: str) -> Dict[str, int]:
    return dict(
        map(
            lambda i: (i, os.listdir(path).count(i)),
            os.listdir(path),
        )
    )


async def add_filters(
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
