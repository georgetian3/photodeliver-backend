from PIL.ImageFile import ImageFile
from PIL.ImageFilter import GaussianBlur
from PIL import Image, ImageFont, ImageDraw
from models.photo import PhotoVersion


async def resize_image(image: ImageFile, photo_version: PhotoVersion) -> ImageFile:
    if photo_version.scale == 1:
        return image
    return image.resize((
        round(photo_version.width * photo_version.scale),
        round(photo_version.height * photo_version.scale)
    ))

async def blur_image(image: ImageFile, photo_version: PhotoVersion) -> ImageFile:
    if photo_version.blur == 0:
        return image
    return image.filter(GaussianBlur(min(photo_version.width, photo_version.height) * photo_version.blur))

ALPHA_MODE = "RGBA"

async def watermark_image(image: ImageFile, photo_version: PhotoVersion) -> ImageFile:
    if (photo_version.watermark_text == "" or
        photo_version.watermark_opacity == 0 or
        photo_version.watermark_font_size == 0
    ):
        return image
    
    opaque = photo_version.watermark_opacity == 1

    if opaque:
        watermark = image
    else:
        watermark = Image.new(ALPHA_MODE, image.size, (0, 0, 0, 0))
        if image.mode != ALPHA_MODE:
            image = image.convert(ALPHA_MODE)


    font = ImageFont.truetype("arial.ttf", int(100))
    draw = ImageDraw.Draw(watermark)
    draw.text((image.width / 2, image.height / 2), photo_version.watermark_text, font=font, fill=(255,255,255,1), anchor='ms')

    image = watermark if opaque else Image.alpha_composite(image, watermark)
    image.show()
    return image