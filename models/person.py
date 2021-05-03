from utils import utils
from .states.stateName import StateName
import random


class Person:

    def __init__(self, code, sex, birthday):
        self.code = code
        self.sex = sex
        self.chapter = []
        self.subchapter = []
        self.section = []
        self.subsection = []
        self.chronic = set()
        self.birthday = birthday
        self.today = birthday
        self.alive = True
        self.new_date = True
        self.chronic_count = set()
        self.diagnosis_count = set()

    def live(self, model):
        model.generate(self)

    def add_diagnosis(self, state):
        if state.chronic:
            self.chronic.add(state)
        if self.new_date:
            self.today = utils.get_random_date(self.today)
            self.new_date = False
        self.diagnosis_count.add(state)
        if state.state_name == StateName.chapter:
            self.chapter.append((state.code, str(self.today)))
        elif state.state_name == StateName.sub_chapter:
            self.subchapter.append((state.code, str(self.today)))
        elif state.state_name == StateName.section:
            self.section.append((state.code, str(self.today)))
        elif state.state_name == StateName.sub_section:
            self.subsection.append((state.code, str(self.today)))

    # Returning if given diagnosis exists in EHR
    def get_diagnosis(self, state):
        if state.state_name == StateName.chapter:
            for i in self.chapter:
                if i[0] == state.code:
                    return True
        elif state.state_name == StateName.sub_chapter:
            for i in self.subchapter:
                if i[0] == state.code:
                    return True
        elif state.state_name == StateName.section:
            for i in self.section:
                if i[0] == state.code:
                    return True
        elif state.state_name == StateName.sub_section:
            for i in self.subsection:
                if i[0] == state.code:
                    return True

    def die(self):
        # http://andmebaas.stat.ee/Index.aspx?DataSetCode=RV56#
        age = self.today.year - self.birthday.year
        rand = random.uniform(0, 1)
        if age // 5 == 0:
            return rand <= 31/71235
        if age // 5 == 1:
            return rand <= 12/74176
        if age // 5 == 2:
            return rand <= 7/72512
        if age // 5 == 3:
            return rand <= 22/61227
        if age // 5 == 4:
            return rand <= 29/64692
        if age // 5 == 5:
            return rand <= 63/88133
        if age // 5 == 6:
            return rand <= 92/99574
        if age // 5 == 7:
            return rand <= 106/92945
        if age // 5 == 8:
            return rand <= 185/90701
        if age // 5 == 9:
            return rand <= 290/91347
        if age // 5 == 10:
            return rand <= 434/83105
        if age // 5 == 11:
            return rand <= 679/88719
        if age // 5 == 12:
            return rand <= 980/85106
        if age // 5 == 13:
            return rand <= 1381/77344
        if age // 5 == 14:
            return rand <= 1556/58104
        if age // 5 == 15:
            return rand <= 1951/51683
        if age // 5 == 16:
            return rand <= 2564/40544
        if age // 5 == 17:
            return rand <= 2623/23198
        if age // 5 == 18:
            return rand <= 1793/9170
        return True

    def get_age_range(self):
        return utils.AGES[(self.today.year - self.birthday.year) // 5]
