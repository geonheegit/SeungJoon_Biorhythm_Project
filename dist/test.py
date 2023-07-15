import matplotlib.pyplot as plt

plt.rcParams['axes.unicode_minus'] = False
fig = plt.figure(figsize=(8, 8))
fig.set_facecolor('white')
ax = fig.add_subplot()

ax.plot([-1, -2, -3, -4, -5], [3, 5, 6, 3, 6])
plt.show()