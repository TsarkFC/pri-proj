import matplotlib.pyplot as plt
from numpy.lib.function_base import percentile

precision = [1, 1, 1, 0.75, 0.8, 0.83, 0.86, 0.75, 0.77, 0.70]
recall = [0.09, 0.18, 0.27, 0.27, 0.36, 0.45, 0.54, 0.54, 0.63, 0.63]
ticks = [0, 0.2, 0.4, 0.6, 0.8, 1]

# Uncomment for interpolated graphic
# for i in range(len(precision)):
#     precision[i] = max(precision[i:])


plt.plot(recall, precision)
plt.xticks(ticks)
plt.yticks(ticks)

plt.show()
