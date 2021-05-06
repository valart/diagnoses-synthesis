import random
import datetime
from dateutil.relativedelta import relativedelta


class Trajectory:

    def __init__(self):
        self.graph = dict()
        self.percent_of_patients = 0

    '''
    @:param start_edge: diagnosis ICD-10 code
    @:param end_edge: trajectories state object
    '''
    def set_percent_of_patients(self, percent_of_patients):
        self.percent_of_patients = percent_of_patients

    '''
    @:param start_edge: diagnosis ICD-10 code
    @:param end_edge: trajectories state object
    '''

    def add_edge(self, start_edge, end_edge):
        if start_edge not in self.graph:
            self.graph[start_edge] = [end_edge]
        else:
            self.graph[start_edge].append(end_edge)

    def insert_trajectory(self, person, code):
        random_date = self.get_random_date(person.birthday, person.today)
        self.insert_diagnosis(code, random_date, person.section)
        self.get_trajectory(code, random_date, person.section, person.today)

    '''
    @:param diagnosis: current diagnosis code
    @:param time: current date in user life
    @:param diagnoses_list: list of diagnosis that may appear
    @:param deathdate: date, when person died
    '''

    def get_trajectory(self, diagnosis, time, diagnoses_list, deathdate):
        if diagnosis in self.graph:
            # Get all child and shuffle them
            child = self.graph[diagnosis]
            random.shuffle(child)
            sorted(child, key=lambda x: x.probability)

            previous = 0
            power = random.random()
            for state in child:
                if power <= state.probability + previous:
                    if state.name == 'None' or time == deathdate:
                        return
                    date = time + relativedelta(months=state.period)
                    date = date if date < deathdate else deathdate
                    time = self.get_random_date(time, date)
                    self.insert_diagnosis(state.name, time, diagnoses_list)
                    return self.get_trajectory(state.name, time, diagnoses_list, deathdate)
                else:
                    previous += state.probability

    def insert_diagnosis(self, name, time, diagnoses_list):
        index = 0
        for diagnosis in diagnoses_list:
            date = datetime.datetime.strptime(diagnosis[1], '%Y-%m-%d').date()
            if time < date:
                diagnoses_list.insert(index, (name.split('_')[0], str(time), 'TRJ'))
                return True
            index += 1
        return False

    def get_random_date(self, start_date, end_date):
        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        return start_date + datetime.timedelta(days=random_number_of_days)
