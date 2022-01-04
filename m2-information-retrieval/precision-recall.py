import matplotlib.pyplot as plt
import numpy as np

aterragem_marte_no_custom_schema_no_weights = [1, 1, 1, 1, 1, 0, 1, 0, 1, 1]
microsoft_teams_no_custom_schema_no_weights = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
aterragem_marte_with_custom_schema_no_weights = [0, 1, 1, 0, 1, 1, 1, 1, 0, 1]
microsoft_teams_with_custom_schema_no_weights = [1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
aterragem_marte_with_custom_schema_and_weights = [1, 1, 1, 0, 1, 1, 1, 0, 1, 0]
microsoft_teams_with_custom_schema_and_weights = [0, 1, 1, 0, 0, 0, 0, 0, 0, 0]
slides = [1,0,1,0,0,1,0,0,1,1]
slides_2 = [0,1,0,0,1,0,1,0,0,0]

queries = [
    ("aterragem_marte_no_custom_schema_no_weights", [1, 1, 1, 1, 1, 0, 1, 0, 1, 1]),
    ("microsoft_teams_no_custom_schema_no_weights", [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]),
    ("aterragem_marte_with_custom_schema_no_weights", [0, 1, 1, 0, 1, 1, 1, 1, 0, 1]),
    ("microsoft_teams_with_custom_schema_no_weights", [1, 1, 0, 0, 0, 0, 0, 0, 0, 0]),
    ("aterragem_marte_with_custom_schema_and_weights", [1, 1, 1, 0, 1, 1, 1, 0, 1, 0]),
    ("microsoft_teams_with_custom_schema_and_weights", [0, 1, 1, 0, 0, 0, 0, 0, 0, 0]),
    ("slides", [1,0,1,0,0,1,0,0,1,1]),
    ("slides_2", [0,1,0,0,1,0,1,0,0,0])
]

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

    print("----\n", precision, "\n", recall)

    return precision, recall

for (name, data) in queries:
    precision, recall = calculate_precision_recall(data)

    ticks = [0, 0.2, 0.4, 0.6, 0.8, 1]

    plt.rcParams.update({'font.size': 19})
    figures, axis = plt.subplots(1, 2, sharey=True, sharex=True)

    axis[0].plot(recall, precision)

    # decreasing_max_precision = np.maximum.accumulate(precision[::-1])[::-1]

    # Uncomment for interpolated graphic
    last_recall = -1
    for i in range(len(precision)):
        precision[i] = max(precision[i:])
        if recall[i] == 1: 
            precision[i:] =  [precision[i] for _ in precision[i:]]
            break

    recall.insert(0, 0)
    precision.insert(0, precision[0])

    # axis[1].step(recall, decreasing_max_precision, '-r')
    axis[1].plot(recall, precision)

    axis[0].set_xlabel("Recall")
    axis[1].set_xlabel("Recall")
    axis[0].set_ylabel("Precision")
    axis[0].set_title("Precision-Recall Curve")
    axis[1].set_title("Precision-Recall Curve Interpolated")
    plt.xticks(ticks)
    plt.yticks(ticks)

    plt.subplots_adjust(left=0.061, right=0.973, bottom=0.07, top=0.938, hspace=0.2, wspace=0.089)
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()

    plt.show()
    # plt.savefig("graphs/" + name + ".pdf")
