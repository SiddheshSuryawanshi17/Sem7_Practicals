# CSDF Assignment 2
# Implement a program to generate and verify CAPTCHA image.
#
# Run: python captcha_app.py
# Needs Pillow for the image (pip install pillow). Without Pillow it falls back to a text CAPTCHA.
import os
import random
import string

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    HAVE_PIL = True
except ImportError:
    HAVE_PIL = False

# Similar-looking characters (0/O, 1/l/I) are removed to make it fair for humans
CHARS = "".join(c for c in string.ascii_uppercase + string.digits if c not in "0O1IL")


def generate_text(length=6):
    return "".join(random.choice(CHARS) for _ in range(length))


def load_font(size):
    for name in ["arial.ttf", "Arial.ttf", "DejaVuSans-Bold.ttf", "/System/Library/Fonts/Supplemental/Arial.ttf",
                 "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "C:/Windows/Fonts/arial.ttf"]:
        try:
            return ImageFont.truetype(name, size)
        except (OSError, IOError):
            continue
    return ImageFont.load_default()


def generate_image(text, path="captcha.png", width=260, height=90):
    img = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = load_font(48)

    # Background noise dots
    for _ in range(1500):
        draw.point((random.randint(0, width), random.randint(0, height)),
                   fill=tuple(random.randint(120, 255) for _ in range(3)))

    # Each character drawn separately with random colour, position and rotation
    x = 15
    for ch in text:
        char_img = Image.new("RGBA", (55, 70), (255, 255, 255, 0))
        ImageDraw.Draw(char_img).text((5, 5), ch, font=font,
                                      fill=tuple(random.randint(0, 120) for _ in range(3)))
        char_img = char_img.rotate(random.randint(-30, 30), expand=1)
        img.paste(char_img, (x, random.randint(0, 15)), char_img)
        x += 38

    # Distortion lines across the text
    for _ in range(6):
        draw.line([(random.randint(0, width), random.randint(0, height)),
                   (random.randint(0, width), random.randint(0, height))],
                  fill=tuple(random.randint(0, 150) for _ in range(3)), width=2)

    img = img.filter(ImageFilter.SMOOTH)
    img.save(path)
    return path


def verify(expected, user_input):
    return expected.upper() == user_input.strip().upper()


def open_image(path):
    try:
        if os.name == "nt":
            os.startfile(path)
        elif os.uname().sysname == "Darwin":
            os.system(f"open '{path}'")
        else:
            os.system(f"xdg-open '{path}' >/dev/null 2>&1 &")
    except Exception:
        pass


if __name__ == "__main__":
    max_attempts = 3
    for attempt in range(1, max_attempts + 1):
        text = generate_text()
        if HAVE_PIL:
            path = generate_image(text)
            print(f"CAPTCHA image saved as '{os.path.abspath(path)}' (opening it...)")
            open_image(path)
        else:
            print("Pillow not installed -> text CAPTCHA:", " ".join(text))

        answer = input(f"Attempt {attempt}/{max_attempts} - Enter the CAPTCHA: ")
        if verify(text, answer):
            print("CAPTCHA verified successfully. You are human!")
            break
        print(f"Incorrect CAPTCHA (it was {text}). A new CAPTCHA is generated.\n")
    else:
        print("Too many failed attempts. Access blocked (possible bot).")
