import matplotlib.pyplot as plt
import matplotlib

# precision = [1, 1, 1, 1, 1, 0.83, 0.86, 0.75, 0.77, 0.8]
# recall = [0.09, 0.18, 0.27, 0.36, 0.45, 0.45, 0.54, 0.54, 0.63, 0.73]

# precision = [0, 0.5, 0.67, 0.5, 0.6, 0.67, 0.71, 0.75, 0.67, 0.7]
# recall = [0, 0.09, 0.18, 0.18, 0.27, 0.36, 0.45, 0.54, 0.54, 0.63]

precision = [1, 1, 1, 0.75, 0.8, 0.83, 0.86, 0.75, 0.77, 0.70]
recall = [0.09, 0.18, 0.27, 0.27, 0.36, 0.45, 0.54, 0.54, 0.63, 0.63]

# precision = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0.1]
# recall = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0.1]

# precision = [1, 1, 0.67, 0.5, 0.4, 0.33, 0.29, 0.25, 0.22, 0.2]
# recall = [0.1, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]

# precision = [0, 0.5, 0.67, 0.5, 0.4, 0.33, 0.29, 0.25, 0.22, 0.2]
# recall = [0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]

ticks = [0, 0.2, 0.4, 0.6, 0.8, 1]

plt.rcParams.update({'font.size': 19})
figures, axis = plt.subplots(1, 2, sharey=True, sharex=True)

axis[0].plot(recall, precision)

# Uncomment for interpolated graphic
for i in range(len(precision)):
    precision[i] = max(precision[i:])

axis[1].plot(recall, precision)

axis[0].set_xlabel("Recall")
axis[1].set_xlabel("Recall")
axis[0].set_ylabel("Precision")
axis[0].set_title("Precision-Recall Curve")
axis[1].set_title("Precision-Recall Curve Interpolated")
plt.xticks(ticks)
plt.yticks(ticks)
plt.subplots_adjust(left=0.061, right=0.973, bottom=0.061, top=0.938, hspace=0.2, wspace=0.089)

plt.show()
