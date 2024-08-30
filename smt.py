import os


a = "media/with_filters/filtered_1.jpg"
f_path = "media/with_filters/filtered_1"
filtered_files = ['filtered_4.jpg', 'filtered_1.jpg', 'filtered_2.png', '.gitkeep']
f_name = "filtered_2.png"
filtered_path = "media/with_filters/"



# for file in filtered_files:
#     if f_path.split(sep="/")[-1] in file.split(".")[:-1][
#         0
#     ] and os.path.isfile(filtered_path + file):
#         print("hedlhjsdkfgjh")

res = f_name.split(".")[-1]
print(res)