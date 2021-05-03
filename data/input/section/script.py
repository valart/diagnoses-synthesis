import utils.utils as utils
import os
import yaml


for i in utils.categories:
    for j in utils.categories[i]:
        if not os.path.exists(j):
            os.makedirs(j)
        for ij in utils.categories[i][j]:
            with open(j + '/' + ij + '.yml', 'w') as file:
                obj = dict()
                obj['code'] = ij
                obj["age"] = dict()
                for age in utils.AGES:
                    obj["age"][age] = dict()
                    obj["age"][age] = dict()
                    obj["age"][age]["M"] = 1
                    obj["age"][age]["W"] = 1
                documents = yaml.dump(obj, file, sort_keys=False)
