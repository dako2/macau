import os
import cv2
import asyncio
from hume import HumeStreamClient, StreamSocket, HumeClientException
from hume.models.config import FaceConfig
import time
import websockets
import traceback
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
from utilities import Stringifier, print_emotions

async def analyze_frame(file_path = 'data', camera_index = 1):
    cam = cv2.VideoCapture(camera_index)
    if not cam.isOpened():
        print("Error: Could not open camera.")
        return
    # Get API key from environment variables
    api_key = os.getenv("HUME_API_KEY")

    while True:
        try:
            client = HumeStreamClient(api_key)
            config = FaceConfig(identify_faces=True)
            async with client.connect([config]) as socket:
                print("Hume Connected")
                while True:
                    _, frame = cam.read()
                    TEMP_FILE = f"{file_path}/frame_{int(time.time())}.png"
                    cv2.imwrite(TEMP_FILE, frame)
                    # Send the PNG file for analysis
                    result = await socket.send_file(TEMP_FILE)
                    # Process the result if needed
                    # Write the result to the metadata file
                    print(result)
                    with open("metadata.txt", "a") as metadata_file:
                        metadata_file.write(f"{TEMP_FILE}: {result}\n")
                        metadata_file.flush()  # Ensure the data is written immediately
                    await asyncio.sleep(1 / 3)

        except websockets.exceptions.ConnectionClosedError:
            print("Connection lost. Attempting to reconnect in 1 seconds.")
            time.sleep(1)
        except HumeClientException:
            print(traceback.format_exc())
            break
        except Exception:
            print(traceback.format_exc())
        
        time.sleep(3)

        # Check for 'q' key press to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release the camera and close all OpenCV windows
    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    asyncio.run(analyze_frame())
    
