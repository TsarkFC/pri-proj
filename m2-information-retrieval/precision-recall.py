import matplotlib.pyplot as plt
import matplotlib

aterragem_marte_no_custom_schema_no_weights = [1, 1, 1, 1, 1, 0, 1, 0, 1, 1]
microsoft_teams_no_custom_schema_no_weights = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
aterragem_marte_with_custom_schema_no_weights = [0, 1, 1, 0, 1, 1, 1, 1, 0, 1]
microsoft_teams_with_custom_schema_no_weights = [1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
aterragem_marte_with_custom_schema_and_weights = [1, 1, 1, 0, 1, 1, 1, 0, 1, 0]
microsoft_teams_with_custom_schema_and_weights = [0, 1, 1, 0, 0, 0, 0, 0, 0, 0]

def calculate_precision_recall(query_results):
    precision = []
    recall = []

    # recall relevantes / total relevantes
    # precision relevantes / total

    current_relevant_sum = 0
    current_total = 0
    total_relevants = sum(query_results)

    for relevant in query_results:
        current_relevant_sum += relevant
        current_total += 1
        precision.append(current_relevant_sum / current_total)
        recall.append(current_relevant_sum / total_relevants)

    return precision, recall

precision, recall = calculate_precision_recall(aterragem_marte_no_custom_schema_no_weights)

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
