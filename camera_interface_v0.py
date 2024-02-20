import os
import cv2
import asyncio
from hume import HumeStreamClient, StreamSocket
from hume.models.config import FaceConfig
import time
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
from utilities import Stringifier

stringifier = Stringifier()
for emotion_embedding in emotion_embeddings:
    emotion_scores = [emotion["score"] for emotion in emotion_embedding]
    text = stringifier.scores_to_text(emotion_scores)
    print(text)

async def analyze_frame(file_path, api_key, metadata_file):
    client = HumeStreamClient(api_key)
    config = FaceConfig(identify_faces=True)
    async with client.connect([config]) as socket:
        # Send the PNG file for analysis
        result = await socket.send_file(file_path)
        print(result)
        # Process the result if needed
        # Write the result to the metadata file
        metadata_file.write(f"{file_path}: {result}\n")
        metadata_file.flush()  # Ensure the data is written immediately

async def capture_and_analyze_video(camera_index=1):
    # Open the camera
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Get API key from environment variables
    api_key = os.getenv("HUME_API_KEY")

    frame_count = 0  # Counter for naming saved frames
    with open("metadata.txt", "a") as metadata_file:
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()

            if not ret:
                print("Error: Failed to capture frame.")
                break

            # Save the frame as a PNG image
            frame_filename = f"data/frame_{int(time.time())}.png"
            cv2.imwrite(frame_filename, frame)
            print(f"Frame saved as {frame_filename}")

            # Analyze the frame asynchronously
            await analyze_frame(frame_filename, api_key, metadata_file)

            frame_count += 1  # Increment frame counter
            
            # Display the resulting frame
            cv2.imshow('Camera Feed', frame)

            time.sleep(3)

            # Check for 'q' key press to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    asyncio.run(capture_and_analyze_video())
    