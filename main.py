from PIL import Image
from PIL.ImageDraw import ImageDraw

import shapes


size = (1000, 500)
relations = "5<4, 1<4, 3<2, 3<6, 4<7, 2<1, 2<5, 2<6, 8<3, 9<1"


def main():
    img = Image.new("RGB", size, "#ffffff")
    drawer = ImageDraw(img)

    cell0 = shapes.Cell(drawer, pos=(200, 50), k='0')
    cell0.draw(draw_count=False)
    cell0.draw_pointer()

    for i in range(1, 10):
        cell = shapes.Cell(drawer, pos=(60 * i + 200, 50), k=str(i), count='0')
        cell.draw()

        link = shapes.Ground(drawer) if i % 2 else shapes.Arrow(drawer)
        cell.draw_link(drawer, link)

    img.save("output/test_1.png")


if __name__ == "__main__":
    main()

