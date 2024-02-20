import cv2

def capture_video(camera_index=0):
    # Open the camera
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            print("Error: Failed to capture frame.")
            break

        # Display the resulting frame
        cv2.imshow('Camera Feed', frame)

        # Check for 'q' key press to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_video()
