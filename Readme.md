Image Filtering API

This is a test FastAPI application that allows you to upload multiple images, apply a Canny edge detection filter and BGR2GRAY color to them, and then download the filtered images.

Installation is completed via docker with following command:
```zsh
docker build . -t file_loader:0.0.1
```

To start the application, run the following command, port is your preferense:
```zsh
docker run -dp 7329:8000 file_loader:0.0.1
```

This will start the FastAPI server on http://localhost:7329.

To upload images, open Swagger at http://localhost:7329/docs and use /file_ops/upload_multiple_files/ handler. You can include multiple images in the request, you can also specify the first_threshold and second_threshold parameters as integers to customize the Canny edge detection filter, BGR2GRAY color will apply automatically. In return you'll receive JSONResponse with errors/additional information about request.

To get a filtered image open handler file_ops/get_image/ with the file_name parameter set to the name of the image you want to get **without** file type, for example:

> uploading image was Пикачу.jpeg, in order to get the image you shoul use just Пикачу

If the filtered image is not yet available, the server will return a JSONResponse indicating that the filtered image is being processed. You can then wait a few moments and try again.