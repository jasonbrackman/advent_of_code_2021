from helpers import window

x = list('lots of sugar in my tea')
for y in window(x, 2):
    print(y)
