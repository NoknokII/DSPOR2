import cv2

# Load the image
image = cv2.imread('textimages-generator/images/bathymetrie.tiff')

# Get the dimensions of the image
height, width, _ = image.shape

# Define normalized coordinates (replace with your actual values)
x_normalized, y_normalized, w_normalized, h_normalized = (0.271500, 0.162500, 0.021000, 0.085000) 

# Convert normalized coordinates to pixel values
x = x_normalized * width
y = y_normalized * height
w = w_normalized * width
h = h_normalized * height

# Draw the bounding box
cv2.rectangle(image, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2)), (0, 255, 0), 2)  # Green color, thickness = 2

# Display the image with the bounding box
cv2.imshow('Bounding Box', image)
cv2.waitKey(0)
cv2.destroyAllWindows()