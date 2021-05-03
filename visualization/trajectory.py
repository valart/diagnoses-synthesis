import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import csv
import ast

years = mdates.YearLocator()
years_fmt = mdates.DateFormatter('%Y')
fig, ax = plt.subplots(figsize=(20, 10))
# format the ticks
ax.xaxis.set_major_locator(years)
ax.xaxis.set_major_formatter(years_fmt)

with open("../output/diagnoses.csv", encoding="utf8") as file:

    read = csv.reader(file, delimiter="\t")
    date = []
    t_date = []
    num = []
    t_num = []
    txt = []
    t_txt = []
    for row in read:
        if row[0] == '9457':
            for i in list(ast.literal_eval(row[7])):
                if len(i) == 3:
                    t_date.append(datetime.strptime(i[1], '%Y-%m-%d').date())
                    t_txt.append(i[0])
                    t_num.append(1)
                else:
                    date.append(datetime.strptime(i[1], '%Y-%m-%d').date())
                    txt.append(i[0])
                    num.append(1)

ax.plot(date, num, 'go')
ax.set_xlim(date[0], date[-1])
ax.grid(True)

ax.plot(t_date, t_num, 'ro')


for i, t in enumerate(txt):
    ax.annotate(t, (date[i], 1.01), rotation=90)

for i, t in enumerate(t_txt):
    ax.annotate(t, (t_date[i], 0.99), rotation=90)

fig.autofmt_xdate()
plt.show()
