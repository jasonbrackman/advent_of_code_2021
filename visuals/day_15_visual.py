import helpers
import day_15
import matplotlib.pyplot as plt
from PIL import Image, ImageFilter


def simple_plot(data):
    for x, y, c, s in data:
        plt.plot(x, y, f"{c}{s}", markersize=0.25)
    plt.axis("off")

    # Ensure origin is upper left corner instead of default lower left
    ax = plt.gca()  # get the axis
    ax.set_ylim(ax.get_ylim()[::-1])  # invert the axis
    ax.xaxis.tick_top()  # and move the X-Axis
    ax.yaxis.tick_left()  # remove right y-Ticks
    plt.show()


def visualize(points):
    colours = {0: "k", 1: "g", 2: "g", 3: "y", 4: "r", 5: "r", 6: "r", 7: "r", 8: "r", 9: "r"}
    data = []
    for (x, y), v in points.items():
        data.append([x, y, colours[v], '.'])
    simple_plot(data)


if __name__ == "__main__":
    lines = helpers.get_lines(r"./../data/day_15.txt")

    lut = day_15.LUT().load(lines)
    lut.update_multi(5)
    risk, node = day_15.search(lut, (0, 0), lut.end_pos())

    path = []
    while node.parent is not None:
        path.append(node.state)
        node = node.parent
    path.append(node.state)

    grid = lut.get_grid()

    for p in path:
        grid[p] = 25

    # img = Image.fromarray(grid, 'RGB')
    img = Image.new('RGB', (500, 500))
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
            rgb = (255, 255, 200)
            new_img.putpixel(k, rgb)
        elif v == 1:
            rgb = (200, 200, 255)
            new_img.putpixel(k, rgb)
    new_img.show()
    new_img.save('day_15.png')


