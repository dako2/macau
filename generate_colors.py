from flask import Flask, jsonify
import random
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/color')
def get_color():
    # Generate a random color in HSL format
    h = random.randint(0, 360)  # Hue between 0 and 360
    s = random.randint(40, 100)  # Saturation between 40% and 100%
    l = random.randint(40, 60)  # Lightness between 40% and 60% for decent brightness
    color = [h, s, l]
    print(color)
    return jsonify(color)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5001, debug=True)
