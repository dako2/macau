import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
#from utilities import 
import json 
from utilities import Stringifier, print_emotions

stringifier = Stringifier()

class FileModifiedHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.cache = []

    def on_modified(self, event):
        if event.src_path.endswith('metadata.jsonl'):
            print("metadata.txt has been modified")
            with open(event.src_path, 'r') as file:
                # Read the new lines since the last modification
                new_lines = file.readlines()
                # Add the new lines to the cache
                self.cache.extend(new_lines)
                # Process the new lines
                for line in new_lines:
                    data = json.loads(line.strip())
                    # Iterate over the top-level keys in each entry
                    for _, value in data.items():
                        try:
                            emotions = value.get('face', {}).get('predictions', [])[0].get('emotions', [])
                            emo_score, emo_frame = stringifier.process(emotions)
                            #print(emo_score)
                            #print(emo_frame)
                            print(stringifier.scores_to_text(emo_score))
                            print()
                        except:
                            pass

def extract_emotions_from_jsonl(line):
    data = json.loads(line.strip())
    # Iterate over the top-level keys in each entry
    for _, value in data.items():
        try:
            emotions = value.get('face', {}).get('predictions', [])[0].get('emotions', [])
            return emotions
        except:
            pass

def check_emotions_from_jsonl(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            data = json.loads(line.strip())
            # Iterate over the top-level keys in each entry
            for key, value in data.items():
                try:
                    emotions = value.get('face', {}).get('predictions', [])[0].get('emotions', [])
                    emo_score, emo_frame = stringifier.process(emotions)
                    #print(emo_score)
                    #print(emo_frame)
                    print(stringifier.scores_to_text(emo_score))
                    print()
                except:
                    pass

#file_path = 'metadata.jsonl'
check_emotions_from_jsonl('metadata.jsonl')


if __name__ == "__main__":

    event_handler = FileModifiedHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
