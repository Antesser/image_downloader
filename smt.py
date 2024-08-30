import os


a = "media/with_filters/filtered_1.jpg"
f_path = "media/with_filters/filtered_1"
lst = ['filtered_4.jpg', 'filtered_1.jpg', 'filtered_2.png', '.gitkeep']



for file_name in lst:
    if f_path.split("/")[-1] == "".join(file_name.split(".")[:-1]):
        print(file_name)
