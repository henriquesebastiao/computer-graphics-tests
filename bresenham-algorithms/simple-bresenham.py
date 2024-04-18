import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set()

x0 = int(input('Enter x1: '))
y0 = int(input('Enter y1: '))
x1 = int(input('Enter x2: '))
y1 = int(input('Enter y2: '))

x, y = x0, y0

dx = x1 - x0
dy = y1 - y0

print(f'\ndx: {dx}')
print(f'dy: {dy}')

m = dy / dx

print(f'm: {m}')

e = m - 0.5
print(f'e: {e}\n')

# display list points
x_point = []
y_point = []
x_ = []
y_ = []
e_ = []

for i in range(dx):
    x_point.append(x)
    y_point.append(y)
    while e > 0:
        y = y + 1
        e = e - 1
    y_.append(y)
    x = x + 1
    x_.append(x)
    e = e + m
    e_.append(e)

print(
    pd.DataFrame(
        {'X point': x_point, 'Y point': y_point, 'e': e_, 'X': x_, 'Y': y_}
    )
)

plt.scatter(x_point, y_point, color='red')
plt.plot(x_point, y_point)
plt.show()
