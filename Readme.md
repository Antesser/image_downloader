Image Filtering API

This is a test FastAPI application that allows you to upload multiple images, apply a Canny edge detection filter and BGR2GRAY color to them, and then download the filtered images.

Installation is completed via docker with following command:
```zsh
docker build . -t file_loader:0.0.1 or any version you desire
```
To start the application, run the following command:
```zsh
docker run -dp 7329:8000 file_loader:0.0.1 or any port you want
```

This will start the FastAPI server on 
```zsh
http://localhost:7329.
```
To upload images, open Swagger at http://localhost:7329/docs and use /file_ops/upload_multiple_files/ handler. You can include multiple images in the request, you can also specify the first_threshold and second_threshold parameters to customize the Canny edge detection filter, BGR2GRAY color will apply automatically.

To download a filtered image open handler file_ops/get_image/ with the file_name parameter set to the name of the image you want to download without file type, for example:

uploading image was Пикачу.jpeg, in order to get the image you shoul use just Пикачу

If the filtered image is not yet available, the server will return a JSON response indicating that the filtered image is being processed. You can then wait a few moments and try again.



# example-fastapi
Example of eventsourcing with FastAPI

## Getting Started
1. Install dependencies
```zsh
pip install -r requirements.txt
```
2. Start FastAPI process
```zsh
python main.py
```
3. Open local API docs [http://localhost:5000/docs](http://localhost:5000/docs)