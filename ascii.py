import sys
from PIL import Image

ASCII_CHARS = '@%#*+=-:. '
ASCII_COLORS = {
    '@': '\033[91m',  # bright red
    '%': '\033[93m',  # bright yellow
    '#': '\033[92m',  # bright green
    '*': '\033[94m',  # bright blue
    '+': '\033[95m',  # bright magenta
    '=': '\033[96m',  # bright cyan
    '-': '\033[90m',  # bright black
    ':': '\033[37m',  # white
    '.': '\033[0m',  # reset
}

def scale_image(image, new_width=100):
    (original_width, original_height) = image.size
    aspect_ratio = original_height/float(original_width)
    new_height = int(aspect_ratio * new_width)
    new_image = image.resize((new_width, new_height))
    return new_image

def grayscale_image(image):
    return image.convert('L')

def map_pixels_to_ascii(image, range_width=25):
    pixels = image.getdata()
    ascii_str = ''
    for pixel_value in pixels:
        if pixel_value < len(ASCII_CHARS) * range_width:
            ascii_str += ASCII_CHARS[pixel_value//range_width]
        else:
            ascii_str += ASCII_CHARS[-1]
    return ascii_str

def convert_image_to_ascii(image_path):
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(e)
        return
    image = scale_image(image)
    image = grayscale_image(image)

    ascii_str = map_pixels_to_ascii(image)
    img_width = image.width
    ascii_str_len = len(ascii_str)
    ascii_img=""
    for i in range(0, ascii_str_len, img_width):
        for char in ascii_str[i:i+img_width]:
            if char in ASCII_COLORS:
                ascii_img += ASCII_COLORS[char] + char + '\033[0m'
            else:
                ascii_img += char
        ascii_img += "\n"
    return ascii_img

def main(image_path):
    ascii_img = convert_image_to_ascii(image_path)
    print(ascii_img)

if __name__ == '__main__':
    if len(sys.argv)!= 2:
        print("Usage: python ascii_art.py <image_path>")
        sys.exit(1)
    main(sys.argv[1])