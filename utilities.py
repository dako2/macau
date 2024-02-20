"""
https://github.com/HumeAI/CalHacks/blob/main/humechat/chat.py
"""

import numpy as np
from typing import Any, Dict, List

EMOTIONS = np.array([
    "admiring", "adoring", "appreciative", "amused", "angry", "anxious", "awestruck", "uncomfortable", "bored", "calm",
    "focused", "contemplative", "confused", "contemptuous", "content", "hungry", "determined", "disappointed",
    "disgusted", "distressed", "doubtful", "euphoric", "embarrassed", "disturbed", "entranced", "envious", "excited",
    "fearful", "guilty", "horrified", "interested", "happy", "enamored", "nostalgic", "pained", "proud", "inspired",
    "relieved", "smitten", "sad", "satisfied", "desirous", "ashamed", "negatively surprised", "positively surprised",
    "sympathetic", "tired", "triumphant"
])

def find_max_emotion(predictions):

    def get_adjective(score):
        if 0.26 <= score < 0.35:
            return "slightly"
        elif 0.35 <= score < 0.44:
            return "somewhat"
        elif 0.44 <= score < 0.53:
            return "moderately"
        elif 0.53 <= score < 0.62:
            return "quite"
        elif 0.62 <= score < 0.71:
            return "very"
        elif 0.71 <= score <= 3:
            return "extremely"
        else:
            return ""

    if len(predictions) == 0:
        return ["calm", "bored"]

    def process_section(section):
        emotion_predictions = []
        for frame_dict in section:
            if 'predictions' not in frame_dict['face']:
                continue
            frame_emo_dict = frame_dict['face']["predictions"][0]["emotions"]
            emo_dict = {x["name"]: x["score"] for x in frame_emo_dict}
            emo_frame = sorted(emo_dict.items())
            emo_frame = np.array([x[1] for x in emo_frame])
            emotion_predictions.append(emo_frame)
        if len(emotion_predictions) == 0:
            return 'calm'
        # Assuming 'emotion_predictions' is a 2D array
        mean_predictions = np.array(emotion_predictions).mean(axis=0)
        # Get the index of the highest value
        top_index = np.argmax(mean_predictions)

        # Add adjectives to the top emotion based on the prediction score
        top_emotion_adjective = f"{get_adjective(mean_predictions[top_index])} {EMOTIONS[top_index]}"
        return top_emotion_adjective

    # Split predictions into 2 sections
    section_size = len(predictions) // 2
    sections = [predictions[i * section_size:(i + 1) * section_size] for i in range(2)]

    # Get top emotion for each section
    top_emotions = [process_section(section) for section in sections]
    return top_emotions

class Stringifier:
    RANGES = [(0.26, 0.35), (0.35, 0.44), (0.44, 0.53), (0.53, 0.62), (0.62, 0.71), (0.71, 10)]
    ADVERBS = ["slightly", "somewhat", "moderately", "quite", "very", "extremely"]

    ADJECTIVES_48 = [
        "admiring", "adoring", "appreciative", "amused", "angry", "anxious", "awestruck", "uncomfortable", "bored",
        "calm", "focused", "contemplative", "confused", "contemptuous", "content", "hungry", "determined",
        "disappointed", "disgusted", "distressed", "doubtful", "euphoric", "embarrassed", "disturbed", "entranced",
        "envious", "excited", "fearful", "guilty", "horrified", "interested", "happy", "enamored", "nostalgic",
        "pained", "proud", "inspired", "relieved", "smitten", "sad", "satisfied", "desirous", "ashamed",
        "negatively surprised", "positively surprised", "sympathetic", "tired", "triumphant"
    ]

    ADJECTIVES_53 = [
        "admiring", "adoring", "appreciative", "amused", "angry", "annoyed", "anxious", "awestruck", "uncomfortable",
        "bored", "calm", "focused", "contemplative", "confused", "contemptuous", "content", "hungry", "desirous",
        "determined", "disappointed", "disapproving", "disgusted", "distressed", "doubtful", "euphoric", "embarrassed",
        "disturbed", "enthusiastic", "entranced", "envious", "excited", "fearful", "grateful", "guilty", "horrified",
        "interested", "happy", "enamored", "nostalgic", "pained", "proud", "inspired", "relieved", "smitten", "sad",
        "satisfied", "desirous", "ashamed", "negatively surprised", "positively surprised", "sympathetic", "tired",
        "triumphant"
    ]

    @classmethod
    def scores_to_text(cls, emotion_scores: List[float]) -> str:
        if len(emotion_scores) == 48:
            adjectives = cls.ADJECTIVES_48
        elif len(emotion_scores) == 53:
            adjectives = cls.ADJECTIVES_53
        else:
            raise ValueError(f"Invalid length for emotion_scores {len(emotion_scores)}")

        # Return "neutral" if no emotions rate highly
        if all(emotion_score < cls.RANGES[0][0] for emotion_score in emotion_scores):
            return "neutral"

        # Construct phrases for all emotions that rate highly enough
        phrases = [""] * len(emotion_scores)
        for range_idx, (range_min, range_max) in enumerate(cls.RANGES):
            for emotion_idx, emotion_score in enumerate(emotion_scores):
                if range_min < emotion_score < range_max:
                    phrases[emotion_idx] = f"{cls.ADVERBS[range_idx]} {adjectives[emotion_idx]}"

        # Sort phrases by score
        sorted_indices = np.argsort(emotion_scores)[::-1]
        phrases = [phrases[i] for i in sorted_indices if phrases[i] != ""]

        # If there is only one phrase that rates highly, return it
        if len(phrases) == 0:
            return phrases[0]

        # Return all phrases separated by conjunctions
        return ", ".join(phrases[:-1]) + ", and " + phrases[-1]

def print_emotions(emotions: List[Dict[str, Any]]) -> None:
    emotion_map = {e["name"]: e["score"] for e in emotions}
    for emotion in ["Excitement", "Joy", "Sadness", "Anger", "Confusion", "Fear"]:
        print(f"- {emotion}: {emotion_map[emotion]:4f}")


def xx():
    emotion_embeddings = []
    stringifier = Stringifier()
    for emotion_embedding in emotion_embeddings:
        emotion_scores = [emotion["score"] for emotion in emotion_embedding]
        text = stringifier.scores_to_text(emotion_scores)
        print(text)
