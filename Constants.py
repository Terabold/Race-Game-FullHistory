FPS = 60
WIDTH, HEIGHT = 1600, 900

# Colors
GOLD = (255, 215, 0)
GREEN = (0, 255, 0)
FOGGRAY = (50, 50, 50)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
DODGERBLUE = (30, 144, 255)
ORANGE = (255, 165, 0)
DARKORANGE = (255, 140, 0)
DARKGREEN = (0, 200, 0)
BLACK = (0, 0, 0)

LEVELS = [
{
    "track_image": r"photo\track1.png", 
    "border_image": r"photo\track1-border.png",
    "car_start_pos": (350, 200),
    "finishline_pos": [275, 250] ,
    "finishline_size": (150, 25),
    "target_time": 19.0,
    "Level": "Beginner's Path" 
},
{
    "track_image": r"photo\track2.png",
    "border_image": r"photo\track2-border.png",
    "car_start_pos": (400, 240),
    "finishline_pos": [300, 300],
    "finishline_size": (200, 25),
    "target_time": 20.0,
    "Level": "Challenger's Trial" 
},
{
    "track_image": r"photo\track3.png",
    "border_image": r"photo\track3-border.png",
    "car_start_pos": (380, 200),
    "finishline_pos": [295, 250],
    "finishline_size": (175, 25),
    "target_time": 17.0,
    "Level": "Adventurer's Circuit" 
},
{
    "track_image": r"photo\track4.png",
    "border_image": r"photo\track4-border.png",
    "car_start_pos": (510, 275),
    "finishline_pos": [460, 325],
    "finishline_size": (120, 25),
    "target_time": 17.0,
    "Level": "Elite Driver's Course" 
},
{
    "track_image": r"photo\track5.png",
    "border_image": r"photo\track5-border.png",
    "car_start_pos": (570, 175),
    "finishline_pos": [500, 220],
    "finishline_size": (135, 25),
    "target_time": 20.0,
    "Level": "Master's Challenge" 
},
]

FONT = r"fonts\Default.otf"
SPEEDOMETERFONT = r'fonts\speedometer.ttf'
COUNTDOWN_FONT = r'fonts\CountDownFont.otf'

MAXSPEED = 5
ROTATESPEED = 5
ACCELERATION = 0.12

# Assets
CAR_IMG = r"photo/car.png"
FINISHLINE = r'photo/finish.png'
GRASS = r'photo\grass2.jpg'

# Sound
WIN_SOUND = r'sound/victory.wav'
COUNTDOWN_SOUND = r'sound/countdown.mp3'
BACKGROUND_MUSIC = r'sound/background_music.mp3'
COLLIDE_SOUND = r'sound/collide.mp3'