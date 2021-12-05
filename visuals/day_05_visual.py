import matplotlib.pyplot as plt

import day_05
import helpers


def simple_plot(data):
    for x, y, c, s in data:
        plt.plot(x, y, f"{c}{s}", markersize=0.25)
    plt.axis("off")
    plt.show()


def visualize(points):
    colours = {1: "k", 2: "g", 3: "y", 4: "r", 5: "r", 6: "r"}
    shapes = {1: ".", 2: ".", 3: ".", 4: ".", 5: ".", 6: "."}
    data = []
    for point, value in sorted(points.items(), key=lambda item: item[1]):
        data.append([point[0], point[1], colours[value], shapes[value]])
    simple_plot(data)


if __name__ == "__main__":
    path = r"../data/day_05.txt"
    lines = helpers.get_lines(path)
    data = day_05.process_data(lines)
    points = day_05.process_lines(data, verticals=True)
    visualize(points)
