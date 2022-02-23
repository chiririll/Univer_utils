from PIL import Image
from . import utils


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
        card_path = f"src/CARDS/" + ("BACK" if c['TAG'] else f"SUIT_{str(c['SUIT'])}/{c['RANK']:X}") + ".png"
        card = Image.open(card_path)
        img.paste(card, (offset[0] * i, offset[1] * i))

    img.save(path)
    return {'path': path, 'size': (size[0] * scale, size[1] * scale), 'align': "left", 'first_line': 0}


if __name__ == "__main__":
    pass
