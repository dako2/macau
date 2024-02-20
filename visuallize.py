from utilities import Stringifier, print_emotions, find_max_emotion

res = [{'name': 'Admiration', 'score': 0.06379243731498718}, {'name': 'Adoration', 'score': 0.07222934812307358}, {'name': 'Aesthetic Appreciation', 'score': 0.02808445133268833}, {'name': 'Amusement', 'score': 0.027589013800024986}, {'name': 'Anger', 'score': 0.0120259253308177}, {'name': 'Annoyance', 'score': 0.025653120130300522}, {'name': 'Anxiety', 'score': 0.004923961125314236}, {'name': 'Awe', 'score': 0.025031352415680885}, {'name': 'Awkwardness', 'score': 0.061385106295347214}, {'name': 'Boredom', 'score': 0.05333968624472618}, {'name': 'Calmness', 'score': 0.135557159781456}, {'name': 'Concentration', 'score': 0.010018930770456791}, {'name': 'Confusion', 'score': 0.09115109592676163}, {'name': 'Contemplation', 'score': 0.020809845998883247}, {'name': 'Contempt', 'score': 0.030744805932044983}, {'name': 'Contentment', 'score': 0.060751479119062424}, {'name': 'Craving', 'score': 0.008604105561971664}, {'name': 'Determination', 'score': 0.010685051791369915}, {'name': 'Disappointment', 'score': 0.03298037126660347}, {'name': 'Disapproval', 'score': 0.022201286628842354}, {'name': 'Disgust', 'score': 0.010582842864096165}, {'name': 'Distress', 'score': 0.011887000873684883}, {'name': 'Doubt', 'score': 0.01733436994254589}, {'name': 'Ecstasy', 'score': 0.014498891308903694}, {'name': 'Embarrassment', 'score': 0.01016779150813818}, {'name': 'Empathic Pain', 'score': 0.020176580175757408}, {'name': 'Enthusiasm', 'score': 0.02454438991844654}, {'name': 'Entrancement', 'score': 0.031809959560632706}, {'name': 'Envy', 'score': 0.0078100417740643024}, {'name': 'Excitement', 'score': 0.01086737122386694}, {'name': 'Fear', 'score': 0.002841347362846136}, {'name': 'Gratitude', 'score': 0.012725913897156715}, {'name': 'Guilt', 'score': 0.005438251420855522}, {'name': 'Horror', 'score': 0.0024618145544081926}, {'name': 'Interest', 'score': 0.06195246800780296}, {'name': 'Joy', 'score': 0.056471534073352814}, {'name': 'Love', 'score': 0.14727146923542023}, {'name': 'Nostalgia', 'score': 0.01013017725199461}, {'name': 'Pain', 'score': 0.020555714145302773}, {'name': 'Pride', 'score': 0.01391206681728363}, {'name': 'Realization', 'score': 0.021947279572486877}, {'name': 'Relief', 'score': 0.006897658109664917}, {'name': 'Romance', 'score': 0.09956834465265274}, {'name': 'Sadness', 'score': 0.031556904315948486}, {'name': 'Sarcasm', 'score': 0.02911987341940403}, {'name': 'Satisfaction', 'score': 0.03389870375394821}, {'name': 'Desire', 'score': 0.08503230661153793}, {'name': 'Shame', 'score': 0.019161522388458252}, {'name': 'Surprise (negative)', 'score': 0.047956954687833786}, {'name': 'Surprise (positive)', 'score': 0.030542362481355667}, {'name': 'Sympathy', 'score': 0.03246130049228668}, {'name': 'Tiredness', 'score': 0.03606246039271355}, {'name': 'Triumph', 'score': 0.01235896535217762}]

find_max_emotion(res)

stringifier = Stringifier()
