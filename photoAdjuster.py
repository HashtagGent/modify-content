from PIL import Image, ImageEnhance
import random
import os

def modify_photo(input_path, output_path):
    image = Image.open(input_path)

    # Apply brightness adjustment
    brightness_factor = random.uniform(0.95, 1.05)
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(brightness_factor)

    # Apply slight rotation
    rotation_angle = random.choice([-1, 1])
    image = image.rotate(rotation_angle, resample=Image.BICUBIC, expand=True)

    # Apply a centered crop (reduce width by 30px)
    width, height = image.size
    crop_x = 15  # 30px total, so 15px off each side
    image = image.crop((crop_x, 0, width - crop_x, height))

    # Ensure final aspect ratio is still 4:5
    target_ratio = 4 / 5
    new_width, new_height = image.size
    if new_width / new_height != target_ratio:
        new_height = int(new_width / target_ratio)
        image = image.resize((new_width, new_height))

    # Save output
    image.save(output_path)
    print(f"Saved modified image to {output_path}")


if __name__ == "__main__":
    input_image = "input.png"  # Replace with actual file path from Make.com
    output_image = "output.png"  # Replace with the desired output path
    modify_photo(input_image, output_image)
