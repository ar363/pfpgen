from typing import Optional
from fastapi import FastAPI
from fastapi.responses import Response
from random import Random
import colorsys
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
from io import BytesIO
from contrast import check_contrast

app = FastAPI()

INTER_FONT = PIL.ImageFont.truetype("./fonts/Inter-Regular.ttf", 56)


@app.get("/")
def get_pfp(username: str, name: Optional[str] = None):
    global INTER_FONT
    random = Random()
    random.seed(username, 2)

    h, s, l = random.random(), random.uniform(0.85, 1), random.uniform(0.35, 0.65)
    r, g, b = [int(256 * i) for i in colorsys.hls_to_rgb(h, l, s)]

    white_contrast = check_contrast((r / 255, g / 255, b / 255), (1, 1, 1))

    if white_contrast >= 3.5:
        sel_color_fg = (255, 255, 255)
    else:
        sel_color_fg = (0, 0, 0)

    draw_text = ""
    if name:
        name_spl = name.split(" ")
        if len(name_spl) > 1:
            draw_text = name_spl[0][0].upper() + name_spl[-1][0].upper()
        else:
            draw_text = name_spl[0][0].upper()
    else:
        draw_text = username[0:2].upper()

    width_image, height_image = 128, 128
    size_image = width_image, height_image

    im = PIL.Image.new(mode="RGB", size=size_image, color=(r, g, b))
    draw = PIL.ImageDraw.Draw(im)

    width_text, height_text = draw.textsize(draw_text, INTER_FONT)

    offset_x, offset_y = INTER_FONT.getoffset(draw_text)
    width_text += offset_x
    height_text += offset_y

    top_left_x = width_image / 2 - width_text / 2
    top_left_y = height_image / 2 - height_text / 2
    xy = top_left_x, top_left_y

    draw.text(xy, draw_text, sel_color_fg, font=INTER_FONT)

    membuf = BytesIO()
    im.save(membuf, format="webp")

    return Response(
        content=membuf.getvalue(),
        media_type="image/webp",
        headers={"Cache-Control": "max-age=31536000"},
    )
