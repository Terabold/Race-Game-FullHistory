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
    "Level": "Beginner's Path",
    "checkpoints": [
        {"pos": [40, 200], "size": (170, 20)}, 
        {"pos": [700, 700], "size": (200, 20)},  
        {"pos": [1380, 600], "size": (180, 20)},  
        {"pos": [1050, 245], "size": (20, 100)},  
        {"pos": [1380, 190], "size": (170, 20)}, 
        {"pos": [735, 40], "size": (20, 100)}, 
        {"pos": [470, 250], "size": (170, 20)}, 
    ],
},
{
    "track_image": r"photo\track2.png",
    "border_image": r"photo\track2-border.png",
    "car_start_pos": (400, 240),
    "finishline_pos": [300, 300],
    "finishline_size": (200, 25),
    "target_time": 20.0,
    "Level": "Challenger's Trial" ,
    "checkpoints": [
        {"pos": [75, 260], "size": (170, 20)},  
        {"pos": [600, 700], "size": (20, 120)},  
        {"pos": [1380, 600], "size": (170, 20)},  
        {"pos": [1040, 460], "size": (20, 150)},  
        {"pos": [1320, 160], "size": (170, 20)},  
        {"pos": [505, 360], "size": (170, 20)}, 
    ],
},
{
    "track_image": r"photo\track3.png",
    "border_image": r"photo\track3-border.png",
    "car_start_pos": (380, 200),
    "finishline_pos": [295, 250],
    "finishline_size": (175, 25),
    "target_time": 17.0,
    "Level": "Adventurer's Circuit" ,
    "checkpoints": [
        {"pos": [70, 230], "size": (170, 20)}, 
        {"pos": [260, 680], "size": (20, 100)},  
        {"pos": [530, 460], "size": (20, 100)}, 
        {"pos": [1160, 560], "size": (170, 20)},  
        {"pos": [1380, 460], "size": (170, 20)},  
        {"pos": [700, 320], "size": (20, 100)},  
    ],
},
{
    "track_image": r"photo\track4.png",
    "border_image": r"photo\track4-border.png",
    "car_start_pos": (510, 275),
    "finishline_pos": [460, 325],
    "finishline_size": (120, 25),
    "target_time": 17.0,
    "Level": "Elite Driver's Course" ,
    "checkpoints": [
        {"pos": [255, 70], "size": (20, 150)}, 
        {"pos": [540, 690], "size": (20, 150)},  
        {"pos": [1075, 280], "size": (20, 150)},  
        {"pos": [1420, 480], "size": (150, 20)},  
        {"pos": [1050, 70], "size": (20, 150)},  
        {"pos": [680, 500], "size": (20, 150)},  
    ],
},
{
    "track_image": r"photo\track5.png",
    "border_image": r"photo\track5-border.png",
    "car_start_pos": (570, 175),
    "finishline_pos": [500, 220],
    "finishline_size": (135, 25),
    "target_time": 20.0,
    "Level": "Master's Challenge" ,
    "checkpoints": [
        {"pos": [300, 230], "size": (170, 20)},  
        {"pos": [80, 600], "size": (170, 20)},  
        {"pos": [430, 580], "size": (170, 20)},  
        {"pos": [1200, 540], "size": (170, 20)}, 
        {"pos": [1000, 780], "size": (20, 100)}, 
        {"pos": [1390, 400], "size": (170, 20)}, 
        {"pos": [890, 230], "size": (170, 20)}, 
    ],
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
CHECKPOINT = r'photo\checkpoint.jpg'
# Sound
WIN_SOUND = r'sound/victory.wav'
COUNTDOWN_SOUND = r'sound/countdown.mp3'
BACKGROUND_MUSIC = r'sound/background_music.mp3'
COLLIDE_SOUND = r'sound/collide.mp3'
CHECKPOINT_SOUND = r'sound\CHECKPOINT_SOUND.mp3'