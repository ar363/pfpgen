from typing import Optional
from fastapi import FastAPI
import random

app = FastAPI()

@app.get('/')
def get_pfp(username: str, name: Optional[str] = None):
    random.seed(username, 2)

    sel_color_rgb = (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        )

    if (sel_color_rgb[0] + sel_color_rgb[1] + sel_color_rgb[2]) / 3 < 128:
        sel_color_fg = (255, 255, 255)
    else:
        sel_color_fg = (0, 0, 0)
    
    return {'colors': sel_color_rgb}