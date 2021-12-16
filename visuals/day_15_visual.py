from PIL import Image, ImageFilter

import day_15
import helpers


def create_image(grid, save=False):
    # img = Image.fromarray(grid, 'RGB')
    img = Image.new("RGB", (500, 500))
    for k, v in grid.items():
        if v == 25:
            rgb = (255, 255, 255)

        elif v >= 8:
            rgb = (25, 25, 255)
        elif v >= 5:
            rgb = (90, 90, 255)
        elif v >= 2:
            rgb = (180, 180, 255)
        else:
            rgb = (200, 200, 255)
        img.putpixel(k, rgb)
    new_img = img.filter(ImageFilter.GaussianBlur(1))
    for k, v in grid.items():
        if v == 25:
            rgb = (255, 255, 180)
            new_img.putpixel(k, rgb)
        elif v == 1:
            rgb = (200, 200, 255)
            new_img.putpixel(k, rgb)
    new_img.show()

    if save:
        new_img.save("day_15.png")


def get_day_15_data(lines):
    lut = day_15.LUT().load(lines)
    lut.update_multi(5)
    risk, node = day_15.search(lut, (0, 0), lut.end_pos())
    return lut, node


def prepare_data_for_visualization(lut, node):
    path = []
    while node.parent is not None:
        path.append(node.state)
        node = node.parent
    path.append(node.state)

    grid = lut.get_grid()
    for p in path:
        grid[p] = 25

    return grid

def main():
    lines = helpers.get_lines(r"./../data/day_15.txt")
    lut, node = get_day_15_data(lines)
    grid = prepare_data_for_visualization(lut, node)
    create_image(grid, save=False)


if __name__ == "__main__":
    main()