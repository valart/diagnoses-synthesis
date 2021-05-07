from parsing import get_model, get_trajectories
from models.person import Person
from datetime import date, timedelta
from visualization import graph, graphics
import os
import csv
import random
import sys


def save_into_file(data, first_time):
    if not os.path.exists('output'):
        os.makedirs('output')
    let = 'w' if first_time else 'a'
    with open('output/diagnoses.csv', let, newline='') as file:
        writer = csv.writer(file, delimiter='\t')
        if first_time:
            writer.writerow(
                ["Code", "Sex", "Birthday", "Died", "Age", "Chapter", "Subchapter", "Section", "Subsection"])
        for person in data:
            # Filtering data between 2010 and 2019
            # person.section = list(filter(lambda x: 2010 <= int(x[1][:4]) <= 2019, person.section))
            writer.writerow(
                [person.code, person.sex, person.birthday, person.today, person.today.year - person.birthday.year,
                 person.chapter, person.subchapter, person.section, person.subsection])


def insert_trajectory(trajectories, data):
    keys = list(trajectories.keys())
    indexes = [i for i in range(len(data))]
    random.shuffle(indexes)
    # Getting random number of people
    indexes = indexes[:int(random.randint(10, 100) / 100 * len(data))]
    for key in keys:
        random.shuffle(indexes)
        for index in indexes[:int(len(indexes) * trajectories[key].percent_of_patients)]:
            trajectories[key].insert_trajectory(data[index], key)


def generate(population=1000):
    print("Genereerin {} inimest".format(population))
    print("Loen andmed sisse ...")
    # Getting diagnosis models
    model = get_model()
    # Getting trajectories models
    trajectories = get_trajectories()
    print("Andmed loetud, hakkan genereerima")

    data = []
    first_time = True
    for i in range(population):

        start_date = date(1970, 1, 1)
        end_date = date(2020, 1, 1)

        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        random_date = start_date + timedelta(days=random_number_of_days)

        person = Person(i + 1, random.choice(['M', 'F']), random_date)
        person.live(model)
        data.append(person)

        print(i + 1)
        if (i + 1) % 100 == 0:
            # Trajectories
            print("Lisan trajektoorid")
            insert_trajectory(trajectories, data)

            # Inserting data to file
            print("Lisan andmed faili")
            save_into_file(data, first_time)
            first_time = False
            data = []

    if len(data) != 0:
        # Trajectories
        print("Lisan trajektoorid")
        insert_trajectory(trajectories, data)

        # Inserting data to file
        print("Lisan andmed faili")
        save_into_file(data, first_time)


def show_model(age, sex):
    graph.show_graph(age, sex)


def show_plot(category):
    graphics.show_categories(category)


if __name__ == '__main__':
    if "-p" in sys.argv:
        generate(int(sys.argv[sys.argv.index("-p") + 1]))
    elif "-model" in sys.argv:
        show_model(int(sys.argv[sys.argv.index("-model") + 1]), sys.argv[sys.argv.index("-model") + 2])
    elif "-plot" in sys.argv:
        show_plot(sys.argv[sys.argv.index("-plot") + 1])
    else:
        generate()
