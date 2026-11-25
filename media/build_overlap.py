"""Draw the three constructed examples used by labs.box_overlap."""
from pathlib import Path
import sys
from PIL import Image, ImageDraw
from build_control import font
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from labs.box_overlap import examples, measure


def main():
    image = Image.new("RGB", (1280, 574), "#f4f3ec")
    draw = ImageDraw.Draw(image)
    ink, muted = "#1b383e", "#45605d"
    draw.text((45, 29), "PERCEPTION LAB  /  GENERATED GEOMETRY", font=font(16, True), fill="#486b63")
    draw.text((43, 72), "The denominator changes the interpretation", font=font(40, True), fill=ink)
    for i, (label, pair) in enumerate(examples().items()):
        x = 44 + 401 * i
        draw.rounded_rectangle((x, 158, x + 385, 499), radius=13, fill="#ffffff", outline="#c4d2c7", width=2)
        draw.text((x + 22, 178), label, font=font(25, True), fill=ink)
        for box, color in zip(pair, ("#126e66", "#ac643e")):
            k = 17
            pts = (x + 55 + k * box.left, 238 + k * box.top, x + 55 + k * box.right, 238 + k * box.bottom)
            draw.rectangle(pts, outline=color, width=5)
        values = measure(*pair)
        draw.text((x + 23, 409), f"IoU   {values.iou:.2f}", font=font(20, True), fill=ink)
        draw.text((x + 23, 453), f"Fraction of smaller box   {values.fraction_of_smaller:.2f}", font=font(17), fill=muted)
    draw.text((46, 531), "Boxes are synthetic. Geometry alone cannot establish whether two detections share an object identity.", font=font(19), fill=muted)
    image.save(Path(__file__).with_name("box-overlap.png"), optimize=True)


if __name__ == "__main__":
    main()
