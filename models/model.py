from models.states.stateName import StateName
import random
from datetime import date
from utils import utils


class Model:

    def __init__(self):
        self.states = {
            StateName.chapter: [],
            StateName.sub_chapter: [],
            StateName.section: [],
            StateName.sub_section: []
        }
        self.graph = dict()

    '''
    :param start: parent ICD0-10 code
    :param: end: child state object
    '''
    def add_edge(self, start, end):
        if start not in self.graph:
            self.graph[start] = [end]
        else:
            self.graph[start].append(end)

    '''
    :param state_category: category of ICD-10 state
    :param: diagnosis: state object
    '''
    def add_state(self, state_category, diagnosis):
        if diagnosis not in self.states[state_category]:
            self.states[state_category].append(diagnosis)

    '''
    :param code: some ICD0-10 code
    :return: state object that has same codename
    '''
    def get_state(self, code):
        for state in self.states[StateName.chapter]:
            if state.code == code:
                return state
        for state in self.states[StateName.sub_chapter]:
            if state.code == code:
                return state
        for state in self.states[StateName.section]:
            if state.code == code:
                return state
        for state in self.states[StateName.sub_section]:
            if state.code == code:
                return state

    '''
    :param person: person object
    '''
    def check_chronic_diagnoses(self, person):
        # Adding all chronic diagnoses
        for diagnosis in person.chronic:
            if diagnosis not in person.chronic_count and random.random() < 0.1:
                person.chronic_count.add(diagnosis)
                person.add_diagnosis(diagnosis)
        person.new_date = True

    '''
    :param person: person object who has an age and a gender
    :param code: current state(diagnosis) name
    '''
    def add_diagnoses(self, person, code):
        # Getting all possible child objects
        possible_diagnoses = [i for i in self.graph[code]]
        diagnoses = list(filter(lambda d: d.once is False or person.get_diagnosis(d) is False, possible_diagnoses))
        random.shuffle(diagnoses)

        # If we are in INITIAL state, we are going through all chapters
        if code == 'INITIAL':
            for diagnosis in diagnoses:
                self.check_chronic_diagnoses(person)
                probability = diagnosis.age[person.today.year - person.birthday.year][person.sex]
                if random.random() < probability and diagnosis not in person.diagnosis_count:
                    person.add_diagnosis(diagnosis)
                    self.add_diagnoses(person, diagnosis.code)
                    person.new_date = True
        # Otherwise we are going through all state child until we get suitable state
        else:
            found = False
            while found is False:
                for diagnosis in diagnoses:
                    probability = diagnosis.age[person.today.year - person.birthday.year][person.sex]
                    if random.random() < probability and diagnosis not in person.diagnosis_count:
                        person.add_diagnosis(diagnosis)
                        if diagnosis.code in self.graph:
                            self.add_diagnoses(person, diagnosis.code)
                        # If this is final state it may have next depending on it states
                        elif diagnosis.next is not None:
                            for diagnosis_code, prob in diagnosis.next.items():
                                if random.random() < prob:
                                    self.add_diagnoses(person, self.get_state(diagnosis_code))
                        found = True
                        break

    '''
    :param person: person object that is going to have a diagnoses
    '''
    def generate(self, person):
        if not person.alive:
            return
        # Add diagnoses
        self.add_diagnoses(person, 'INITIAL')
        # Start new year
        person.today = date(person.today.year + 1, 1, 1)
        # Check if person die in same age
        if person.die():
            person.today = utils.get_random_date(person.today)
            person.alive = False
        # Repeat
        person.chronic_count = set()
        person.diagnosis_count = set()
        self.generate(person)
