# import cv2

# points = []

# def select_points(event, x, y, flags, param):
#     if event == cv2.EVENT_LBUTTONDOWN:
#         points.append((x, y))
#         print(f"Point selected: {x, y}")
        
#         if len(points) == 4:
#             cv2.destroyAllWindows()

# cap = cv2.VideoCapture('video2.mp4')
# ret, img = cap.read()
# cap.release()

# cv2.imshow("Select 4 Points", img)
# cv2.setMouseCallback("Select 4 Points", select_points)
# cv2.waitKey(0)

# coord = points  # Use the selected points as coordinates
# print("Coordinates of polygon:", coord)


import cv2

points = []

def select_points(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        print(f"Point selected: {x, y}")
        
        if len(points) == 4:
            cv2.destroyAllWindows()

# Load the video and capture the first frame
cap = cv2.VideoCapture('video2.mp4')
ret, img = cap.read()
cap.release()

# Resize the image to a more manageable size if it's too large
scale_percent = 50  # Percentage of original size
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
resized_img = cv2.resize(img, (width, height))

cv2.imshow("Select 4 Points", resized_img)
cv2.setMouseCallback("Select 4 Points", select_points)
cv2.waitKey(0)

# Adjust the coordinates based on the scaling factor
coord = [(int(x * 100 / scale_percent), int(y * 100 / scale_percent)) for x, y in points]
print("Coordinates of polygon:", coord)
