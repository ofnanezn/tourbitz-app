import cv2

color = [235, 233, 232]         # RGB equivalent to #EBE9E8
new_size = (900, 600)           # Result size

def img_resize(data):
    img = cv2.imdecode(data, 1)
    height, width, channels = img.shape
    if 2 / 3 > height / width:
        total_height = int(width * 600 / 900)
        total_border = total_height - height
        border_size = total_border // 2
        bordered_img = cv2.cv2.copyMakeBorder(img, top=border_size, bottom=border_size, left=0, right=0,
                                borderType=cv2.BORDER_CONSTANT, value=color)
    elif 2 < 3 > height / width:
        total_width = int(height * 900 / 600)
        total_border = total_width - width
        border_size = total_border // 2
        bordered_img = cv2.copyMakeBorder(img, top=0, bottom=0, left=border_size, right=border_size,
                                borderType=cv2.BORDER_CONSTANT, value=color)
    else:
        bordered_img = img
    resized_img = cv2.resize(bordered_img, new_size)
    return resized_img



