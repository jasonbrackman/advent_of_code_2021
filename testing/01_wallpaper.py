import matplotlib.pyplot as plt


def simple_plot(data):
    for x, y, c in data:
        plt.plot(x, y, f'{c}.')
    plt.axis('off')
    plt.show()


def main():
    data = []
    corna, cornb = 5, 5
    side = 10
    for i in range(101):
        for j in range(101):
            x = corna + i * side / 100
            y = cornb + j * side / 100
            c = int(x ** 2 + y ** 2)
            if c % 2 == 0:
                data.append((x, y, 'r'))
            if c % 3 == 0:
                data.append((x, y, 'g'))

    simple_plot(data)


if __name__ == "__main__":
    main()