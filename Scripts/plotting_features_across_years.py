import json
import matplotlib.pyplot as plt
from collections import defaultdict

with open('complexity_analysis_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

years = sorted(int(y) for y in data.keys())
metric_group = 'per_sentence'
features_to_plot = ['subordination', 'passive', 'nominalization']

# group by decade: 1943 → 1940, 1957 → 1950, etc.
decade_data = defaultdict(lambda: defaultdict(list))

for y in years:
    decade = (y // 10) * 10   # e.g. 1943 -> 1940
    y_str = str(y)
    for feature in features_to_plot:
        value = data[y_str][metric_group][feature]
        decade_data[decade][feature].append(value)

# compute average per decade
decades = sorted(decade_data.keys())

plt.figure(figsize=(10, 6))

for feature in features_to_plot:
    decade_values = []
    for d in decades:
        vals = decade_data[d][feature]
        decade_values.append(sum(vals) / len(vals))
    plt.plot(decades, decade_values, marker='o', label=feature.replace('_', ' ').title())

plt.xlabel('Decade')
plt.ylabel('Average occurrences per sentence')
plt.title('Diachronic evolution of grammatical complexity (by decade)')
plt.xticks(decades)  # one tick per decade
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()