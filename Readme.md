**Image Filtering API**

This is a test FastAPI application that allows you to upload multiple images, apply a Canny edge detection filter and BGR2GRAY color to them, and then get the filtered images.

Installation is completed via docker with following command in order to build an image:
```zsh
docker build . -t file_loader:0.0.1
```
To start the application, run next command in a new container, pulling the image if needed and starting the container, use your preferred port:
```zsh
docker run -dp 7329:8000 file_loader:0.0.1
```
This will start the FastAPI server on http://localhost:7329.

To upload images, open Swagger on http://localhost:7329/docs and use /file_ops/upload_multiple_files/ handler or you can use **really** simplistic JINJA2 templates via http://localhost:7329/file_ops/upload. You can include multiple images in the request, you can also specify the first_threshold and second_threshold parameters as integers to customize the Canny edge detection filter, while BGR2GRAY color will apply automatically *as it looks great*. In return you'll receive JSONResponse with errors/additional information about request.

To get a filtered image open handler file_ops/get_image/ or http://localhost:7329/file_ops/download with the file_name parameter set to the name of the image as string you want to get **without** file type, for example:

> uploading image was *Пикачу.jpeg*, in order to get the image you should paste just *Пикачу*

If the filtered image is not yet available, the server will return a JSONResponse indicating that the filtered image is being processed. You can then wait a few moments and try again. If required image wasn't even loaded you'll receive a JSONResponse with information about it as well. If you try to upload image with the same name again proper JSONResponse will be returned. If everything is ok you'll get FileResponse with requested image.