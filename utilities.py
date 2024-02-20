"""
https://github.com/HumeAI/CalHacks/blob/main/humechat/chat.py
"""

import numpy as np
from typing import Any, Dict, List
import numpy as np 

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
            frame_emo_dict = section #frame_dict['face']["predictions"][0]["emotions"]
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
    #0.26
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
            return 'neutral'

        # Construct phrases for all emotions that rate highly enough
        phrases = [""] * len(emotion_scores)
        for range_idx, (range_min, range_max) in enumerate(cls.RANGES):
            for emotion_idx, emotion_score in enumerate(emotion_scores):
                if range_min < emotion_score < range_max:
                    phrases[emotion_idx] = f"{cls.ADVERBS[range_idx]} {adjectives[emotion_idx]}"

        # Sort phrases by score
        sorted_indices = np.argsort(emotion_scores)[::-1]
        sorted_emotion_names = [phrases[i] for i in sorted_indices if phrases[i] != ""]

        combined_emotions = []

        # Combine emotion names with scores
        for emotion_name in sorted_emotion_names:
            score = emotion_scores[phrases.index(emotion_name)]
            combined_emotions.append(f"{emotion_name}: {round(score, 2)}")

        #print(phrases)
        # If there is only one phrase that rates highly, return it
        if len(combined_emotions) == 1:
            return combined_emotions[0]

        # Return all phrases separated by conjunctions
        return ", ".join(combined_emotions[:-1]) + ", and " + combined_emotions[-1]
    
    @classmethod
    def process(cls, res):
        try:
            emo_dict = {x["name"]: x["score"] for x in res}
            emo_frame = sorted(emo_dict.items())
            emo_score = np.array([x[1] for x in emo_frame])
            return emo_score, emo_frame
        except:
            pass

def print_emotions(emotions: List[Dict[str, Any]]) -> None:
    emotion_map = {e["name"]: e["score"] for e in emotions}
    for emotion in ["Excitement", "Joy", "Sadness", "Anger", "Confusion", "Fear"]:
        print(f"- {emotion}: {emotion_map[emotion]:4f}")

def something():
    emotion_embeddings = ["Excitement", "Joy", "Sadness", "Anger", "Confusion", "Fear"]
    stringifier = Stringifier()
    for emotion_embedding in emotion_embeddings:
        emotion_scores = [emotion["score"] for emotion in emotion_embedding]
        text = stringifier.scores_to_text(emotion_scores)
        print(text)


res = [{'name': 'Admiration', 'score': 0.06379243731498718}, {'name': 'Adoration', 'score': 0.07222934812307358}, {'name': 'Aesthetic Appreciation', 'score': 0.02808445133268833}, {'name': 'Amusement', 'score': 0.027589013800024986}, {'name': 'Anger', 'score': 0.0120259253308177}, {'name': 'Annoyance', 'score': 0.025653120130300522}, {'name': 'Anxiety', 'score': 0.004923961125314236}, {'name': 'Awe', 'score': 0.025031352415680885}, {'name': 'Awkwardness', 'score': 0.061385106295347214}, {'name': 'Boredom', 'score': 0.05333968624472618}, {'name': 'Calmness', 'score': 0.135557159781456}, {'name': 'Concentration', 'score': 0.010018930770456791}, {'name': 'Confusion', 'score': 0.09115109592676163}, {'name': 'Contemplation', 'score': 0.020809845998883247}, {'name': 'Contempt', 'score': 0.030744805932044983}, {'name': 'Contentment', 'score': 0.060751479119062424}, {'name': 'Craving', 'score': 0.008604105561971664}, {'name': 'Determination', 'score': 0.010685051791369915}, {'name': 'Disappointment', 'score': 0.03298037126660347}, {'name': 'Disapproval', 'score': 0.022201286628842354}, {'name': 'Disgust', 'score': 0.010582842864096165}, {'name': 'Distress', 'score': 0.011887000873684883}, {'name': 'Doubt', 'score': 0.01733436994254589}, {'name': 'Ecstasy', 'score': 0.014498891308903694}, {'name': 'Embarrassment', 'score': 0.01016779150813818}, {'name': 'Empathic Pain', 'score': 0.020176580175757408}, {'name': 'Enthusiasm', 'score': 0.02454438991844654}, {'name': 'Entrancement', 'score': 0.031809959560632706}, {'name': 'Envy', 'score': 0.0078100417740643024}, {'name': 'Excitement', 'score': 0.01086737122386694}, {'name': 'Fear', 'score': 0.002841347362846136}, {'name': 'Gratitude', 'score': 0.012725913897156715}, {'name': 'Guilt', 'score': 0.005438251420855522}, {'name': 'Horror', 'score': 0.0024618145544081926}, {'name': 'Interest', 'score': 0.06195246800780296}, {'name': 'Joy', 'score': 0.056471534073352814}, {'name': 'Love', 'score': 0.14727146923542023}, {'name': 'Nostalgia', 'score': 0.01013017725199461}, {'name': 'Pain', 'score': 0.020555714145302773}, {'name': 'Pride', 'score': 0.01391206681728363}, {'name': 'Realization', 'score': 0.021947279572486877}, {'name': 'Relief', 'score': 0.006897658109664917}, {'name': 'Romance', 'score': 0.09956834465265274}, {'name': 'Sadness', 'score': 0.031556904315948486}, {'name': 'Sarcasm', 'score': 0.02911987341940403}, {'name': 'Satisfaction', 'score': 0.03389870375394821}, {'name': 'Desire', 'score': 0.08503230661153793}, {'name': 'Shame', 'score': 0.019161522388458252}, {'name': 'Surprise (negative)', 'score': 0.047956954687833786}, {'name': 'Surprise (positive)', 'score': 0.030542362481355667}, {'name': 'Sympathy', 'score': 0.03246130049228668}, {'name': 'Tiredness', 'score': 0.03606246039271355}, {'name': 'Triumph', 'score': 0.01235896535217762}]
stringifier = Stringifier()
emo_score, emo_frame = stringifier.process(res)
print(stringifier.scores_to_text(emo_score))
