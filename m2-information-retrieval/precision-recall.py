import matplotlib.pyplot as plt
from numpy.lib.function_base import percentile

# precision = [1, 1, 1, 1, 1, 0.83, 0.86, 0.75, 0.77, 0.8]
# recall = [0.09, 0.18, 0.27, 0.36, 0.45, 0.45, 0.54, 0.54, 0.63, 0.73]

# precision = [0, 0.5, 0.67, 0.5, 0.6, 0.67, 0.71, 0.75, 0.67, 0.7]
# recall = [0, 0.09, 0.18, 0.18, 0.27, 0.36, 0.45, 0.54, 0.54, 0.63]

# precision = [1, 1, 1, 0.75, 0.8, 0.83, 0.86, 0.75, 0.77, 0.70]
# recall = [0.09, 0.18, 0.27, 0.27, 0.36, 0.45, 0.54, 0.54, 0.63, 0.63]

# precision = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0.1]
# recall = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0.1]

# precision = [1, 1, 0.67, 0.5, 0.4, 0.33, 0.29, 0.25, 0.22, 0.2]
# recall = [0.1, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]

# precision = [0, 0.5, 0.67, 0.5, 0.4, 0.33, 0.29, 0.25, 0.22, 0.2]
# recall = [0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]

ticks = [0, 0.2, 0.4, 0.6, 0.8, 1]

# Uncomment for interpolated graphic
# for i in range(len(precision)):
#     precision[i] = max(precision[i:])


plt.plot(recall, precision)
plt.xlabel("Recall")
plt.ylabel("Precision")
plt.xticks(ticks)
plt.yticks(ticks)
plt.subplots_adjust(left=0.3, right=0.7, bottom=0.2, top=0.8)

plt.show()
