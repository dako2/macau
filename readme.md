Theme: Entertainment, Emotion, Music, Art, Game, Self-expression ...

(Action needed) Use Cases (Product): Somehow related to VR?????? Texas Holdem


UI/UX software/hardware platform: Browser? VR/AR kit? iPhone? 777 Machine? some IoTs? or a big screen???
1. I think Browser is a good step first (good to have a strong frontend webUI engineer)
2. webxr, three.js, webgl...
3. Themes: https://1955horsebit.gucci.com/#/handbags, https://lumalabs.ai/luma-web-library
webxr, three.js, webgl...
https://helloenjoy.itch.io/lights


1. camera_interface.py ==> Camera to HUME API
2. visualize.py ==> visualize the emotion (animation, small game, digital arts, sora ...??) 
3. prompts.py ==> Admiration, Adoration, happiness, Prompt: I am playing the game and generate the music based on my emotion status? {emotion1} {emotion2} {emotion3}
Open Prompt Lookup Dictionary
4. music_gen.py ==> input prompts and output background audio, suno api / musicLM
5. audio player 

Currently output of visualize.py

extremely calm: 0.74, quite focused: 0.55, moderately bored: 0.53, somewhat happy: 0.41, slightly contemplative: 0.29, slightly euphoric: 0.27, and slightly tired: 0.26

quite calm: 0.57, slightly bored: 0.35, slightly focused: 0.35, slightly desirous: 0.33, slightly tired: 0.29, and slightly happy: 0.27

very calm: 0.67, quite amused: 0.55, quite happy: 0.54, quite enamored: 0.53, moderately desirous: 0.45, somewhat content: 0.44, somewhat nostalgic: 0.37, and slightly focused: 0.32

very calm: 0.7, quite happy: 0.54, moderately amused: 0.52, moderately enamored: 0.5, somewhat desirous: 0.44, somewhat content: 0.44, somewhat nostalgic: 0.36, slightly focused: 0.33, and slightly bored: 0.27

very calm: 0.64, quite amused: 0.54, quite happy: 0.54, moderately enamored: 0.52, somewhat desirous: 0.44, somewhat content: 0.42, somewhat nostalgic: 0.36, and slightly focused: 0.32


===== next steps =====
1) i want to map the emotion to the colors visual effect using the colors git repo from hume 
2) i want to port the color into a js anmiation on a web UI. something like this: https://github.com/mattrossman/magic-marble-tutorial
 - I'm stuck here to change the color dynamically in this src/App.jsx code (my basic learning here I need to build up some sort of highlevel porting function to bridge this jsx code and python code in the backend)
// HSL values global value
const options = [
  [0, 100, 50],
  [60, 100, 50],
  [150, 100, 50],
  [240, 70, 60],
  [0, 0, 80],
]
3) need to make the output of emotions ===> suno.ai
 
