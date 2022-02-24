import svgwrite
from PIL import Image
from . import utils, shapes
from .svg2emf import export_emf


def draw_cards(cards):
    card_size = (148, 230)
    offset = (30, 30)
    scale = 0.4

    path = f"output/images/cards/{len(cards)}.png"
    size = (
        card_size[0] + offset[0] * (len(cards) - 1),
        card_size[1] + offset[1] * (len(cards) - 1)
    )

    utils.check_path(path)
    img = Image.new("RGBA", size)

    for i, c in enumerate(cards):
        card_path = f"src/cards/" + ("BACK" if c['TAG'] else f"SUIT_{str(c['SUIT'])}/{c['RANK']:X}") + ".png"
        card = Image.open(card_path, 'r').convert("RGBA")
        img.paste(card, (offset[0] * i, offset[1] * i), card)

    img.save(path)
    return {'path': path, 'size': (size[0] * scale, size[1] * scale), 'align': "left", 'first_line': 709}


def draw_scheme(filename: str, cards: list, pointer_pos: int = None):
    padding = (50, 30)
    spacing = 20
    size = (
        len(cards) * shapes.Card.get_size()[0] + padding[0] * 2 + spacing * (len(cards) - 1),
        shapes.Card.get_size()[1] + padding[1] * 2
    )

    path = f"output/images/schemes/{filename}.svg"
    utils.check_path(path)

    dwg = svgwrite.Drawing(path, size)

    shapes.Pointer(dwg, (padding[0], padding[1] + shapes.Card.h // 2), "TOP", False, -90).draw()
    for i, c in enumerate(reversed(cards)):
        pos = (padding[0] + spacing * i + shapes.Card.get_size()[0] * i, padding[1])
        card = shapes.Card(dwg, pos, c, ['X'] if pointer_pos == i else [])
        card.draw()

        if i < len(cards) - 1:
            shapes.StraightArrow(dwg, card.get_arrow(), (pos[0] + card.get_size()[0] + spacing, pos[1] + card.h // 2)).draw()
        else:
            shapes.Ground(dwg, card.get_arrow()).draw()

    dwg.save()

    # Converting to emf
    export_emf(path)

    return {'path': f"output/images/schemes/{filename}.emf", 'size': size}
