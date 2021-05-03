import matplotlib.pyplot as plt
import csv
import ast
from utils import utils
from datetime import datetime
from scipy.ndimage.filters import gaussian_filter1d


def show_categories(category):
    if category == "chapter":
        categories = [category for category in utils.categories]
    else:
        categories = list(utils.categories[category].keys())

    rng = [[0] * 100 for _ in range(len(categories))]
    years = [i for i in range(100)]

    with open("output/diagnoses.csv", encoding="utf8") as file:
        read = csv.reader(file, delimiter="\t")
        next(read)
        for row in read:
            rowVal = row[5] if category == "chapter" else row[6]
            for cat in list(ast.literal_eval(rowVal)):
                if cat[0] in categories:
                    catIndex = categories.index(cat[0])
                    age = datetime.strptime(cat[1], '%Y-%m-%d').year - datetime.strptime(row[2], '%Y-%m-%d').year
                    rng[catIndex][age] += 1

    fig, ax = plt.subplots(figsize=(20, 5))
    for i in range(len(categories)):
        rng[i] = gaussian_filter1d(rng[i], sigma=2)

    categories[:] = [utils.names[i] for i in categories]
    colors = utils.colors

    rng.reverse()
    categories.reverse()

    ax.stackplot(years, rng, labels=categories, colors=colors[:len(categories)])
    ax.set_title('Peatükkid' if category == "chapter" else utils.names[category])
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    ax.set_ylabel('Total patients')
    fig.tight_layout()
    plt.show()
    # plt.savefig("F00-F99.png") # plt.show()

