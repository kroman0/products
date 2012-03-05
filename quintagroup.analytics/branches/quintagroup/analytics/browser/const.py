""" Module dedicated to provide const for treemap """

from PIL import Image
import os

DATA_PATH = os.path.abspath(os.path.dirname(__file__)) + '/data'
FONT_PATH = DATA_PATH + '/fonts'

IMAGE_MASK = Image.open( DATA_PATH + "/rect.png" )
USER_FONT = "BI"
WIDTH= 900
HEIGHT= 700

TEXT_SATURATION = 0.5
TEXT_LIGHT = 0.3

MAX_PERCENT = 100
MAX_ANGLE = 360

DIV_RGB = 255.0
DIV_SIDE = 11

# FATHER - it means root rectangle
DIVERSION_FATHER = 6

# CHILD - it means in user rectangle
DIVERSION_CHILD = 2
DIVERSION_VERTICAL = 10

DIVERSION_TEXT_BORDER = 1

# V - vertical
DIVERSION_TEXT_CHILD_V = 8

# H - horizontal
DIVERSION_TEXT_CHILD_H = 8

FONT_SIZE_FATHER = DIVERSION_VERTICAL + 5
FONT_SIZE_CHILDREN_MIN = 15

FRAME_COLOR = "grey"
FRAME_DIVERSION = 10

USER_COLOR = ["#814949","#806000","#3f5d29",
              "#3c3c7b","purple","Brown","Magenta","Cyan",
              "Maroon","Navy","Aquamarine","Turquoise","Violet","Pink"]


COLOR_FIELD =["#fde5be",
              "#4af6a0",
              "#9c1b9c",
              "#ad3333",
              "#f4a889",
              "#ccafcc",
              "#db76d8",
              "#0dd0d3",
              "#6f6f6f",
              "#72932d",
              "#647841",
              "#161695",
              "#c064d7",
              "#c3bd78",
              "#c93f3f",
              "#b049db",
              "#ecbc41",
              "#ed2e54",
              "#5252e0",
              "#4aeaea",
              "#ffafbd",
              "#f7f64b",
              "#7d94ac",
              "#6ee793",
              "#fb7439",
              "#d37272",
              "#e3e0ff",
              "#93db93",
              "#768594",
              "#a3d63e",
              "#cd853f",
              "#ffc0cb",
              "#dda0dd",
              "#b0e0e6",
              "#800080",
              "#ff0000",
              "#bc8f8f",
              "#4169e1",
              "#8b4513",
              "#fa8072",
              "#f4a460",
              "#2e8b57",
              "#a0522d",
              "#c0c0c0",
              "#87ceeb",
              "#6a5acd",
              "#708090",
              "#708090",
              "#fffafa",
              "#00ff7f",
              "#4682b4",
              "#d2b48c",
              "#008080",
              "#d8bfd8",
              "#ff6347",
              "#40e0d0",
              "#ee82ee",
              "#f5deb3",
              "#f5f5f5",
              "#ffff00",
              "#9acd32"]

