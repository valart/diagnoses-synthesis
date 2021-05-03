import yaml
from models.model import Model
from models.states.stateName import StateName
from models.states.state import State
from models.states.trajectory_state import TrajectoryState
from models.trajectory import Trajectory
import os
import utils.utils as utils

DATA_PATH = "data/input"
TRAJECTORY_PATH = "data/trajectories/"

'''
:param filename: filename of ICD-10 diagnosis
:param stateName: statename of state object
:return: fully decorated state object
'''
def get_state(filename, stateName):
    with open(filename) as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
        next = data['next'] if 'next' in data else None
        once = data['once']
        chronic = data['chronic']
        if next is not None:
            keys = [key for key in next]
            values = [value for value in next.values()]
            scaled = utils.scale_down(values)
            for index, value in enumerate(keys):
                next[value] = scaled[index]
        return State(data['code'], data['age'], stateName, next, once, chronic)


# Existing only 4 levels of ICD-10 codes
# |-chapter
#   |-subchapter
#       |-section
#           |-subsection
def get_model(path=""):
    model = Model()
    # Adding chapters
    for chapterFile in os.listdir(path + DATA_PATH + '/chapter/'):
        chapter = get_state(path + DATA_PATH + '/chapter/' + chapterFile, StateName.chapter)
        model.add_edge('INITIAL', chapter)
        model.add_state(StateName.chapter, chapter)

        # Adding subchapters
        if not os.path.exists(path + DATA_PATH + '/subchapter/' + chapterFile[:-4]):
            continue
        subchapters = []
        for subchapterFile in os.listdir(path + DATA_PATH + '/subchapter/' + chapterFile[:-4]):
            subchapter = get_state(path + DATA_PATH + '/subchapter/' + chapterFile[:-4] + '/' + subchapterFile, StateName.sub_chapter)
            subchapters.append(subchapter)

            # Adding sections
            if not os.path.exists(path + DATA_PATH + '/section/' + subchapterFile[:-4]):
                continue
            sections = []
            for sectionFile in os.listdir(path + DATA_PATH + '/section/' + subchapterFile[:-4]):
                section = get_state(path + DATA_PATH + '/section/' + subchapterFile[:-4] + '/' + sectionFile, StateName.section)
                sections.append(section)

                # Adding subsections
                if not os.path.exists(path + DATA_PATH + '/subsection/' + sectionFile[:-4]):
                    continue
                subsections = []
                for subsectionFile in os.listdir(path + DATA_PATH + '/subsection/' + sectionFile[:-4]):
                    subsection = get_state(path + DATA_PATH + '/subsection/' + sectionFile[:-4] + '/' + subsectionFile, StateName.sub_section)
                    subsections.append(subsection)

                for subsection in subsections:
                    model.add_edge(section.code, subsection)
                    model.add_state(StateName.sub_section, subsection)
            for section in sections:
                model.add_edge(subchapter.code, section)
                model.add_state(StateName.section, section)
        for subchapter in subchapters:
            model.add_edge(chapter.code, subchapter)
            model.add_state(StateName.sub_chapter, subchapter)

    return model


def get_trajectories():
    trajectories = dict()
    for directory in os.listdir(TRAJECTORY_PATH):
        trajectory = Trajectory()
        for filename in os.listdir(TRAJECTORY_PATH + directory):
            with open(TRAJECTORY_PATH + directory + '/' + filename) as file:
                data = yaml.load(file, Loader=yaml.FullLoader)
                start_edge = data['code']
                for code, value in data['transaction'].items():
                    end_edge = TrajectoryState(code, value['period'], value['probability'])
                    trajectory.add_edge(start_edge, end_edge)
        # trajectories.append(trajectory)
        trajectories[directory] = trajectory
    return trajectories
