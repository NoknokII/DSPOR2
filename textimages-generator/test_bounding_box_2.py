import cv2

path = r"C:\Studium\Semester5\DSPRO2\DSPOR2\textimages-generator\debug\acharne.tiff"
# Load the image
image = cv2.imread(path)

# Get the dimensions of the image
height, width, _ = image.shape

# Define normalized coordinates (replace with your actual values)
x_normalized, y_normalized, w_normalized, h_normalized = (0.750000, 0.090000, 0.048780, 0.140000)

# Convert normalized coordinates to pixel values
x = x_normalized * width
y = y_normalized * height
w = w_normalized * width
h = h_normalized * height

# Draw the bounding box
cv2.rectangle(image, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2)), (0, 255, 0), 1)  # Green color, thickness = 2
cv2.imwrite(r"C:\Studium\Semester5\DSPRO2\DSPOR2\textimages-generator\debug\bbox.tiff",image)
# Display the image with the bounding box
cv2.imshow('Bounding Box', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
