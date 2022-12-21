from PIL import Image, ImageDraw
from PIL import Image, ImageTk


def add_checkerboard_pattern(image):
    if image.mode == "RGBA":
        width, height = image.size

        # Create a new image with a checkerboard pattern
        checkerboard = Image.new("RGBA", (width, height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(checkerboard)
        square_size = 10

        for i in range(0, width, square_size):
            for j in range(0, height, square_size):
                color = (128, 128, 128, 255) if (i + j) // square_size % 2 else (192, 192, 192, 255)
                draw.rectangle([i, j, i + square_size, j + square_size], fill=color)

        # Composite the checkerboard pattern over the transparent parts of the image
        result = Image.alpha_composite(image, checkerboard)

        return result
    else:
        return image


def image_scale_down(path, max_width=172, max_height=120):

    original_img = Image.open(path)
    width, height = original_img.size

    if int(height * (max_width / width)) > max_height:
        scaling_factor = max_height / height
        return ImageTk.PhotoImage(original_img.resize((int(width * scaling_factor), max_height)))
    else:
        scaling_factor = max_width / width
        return ImageTk.PhotoImage(original_img.resize((max_width, int(height * scaling_factor))))
