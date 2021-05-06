import sqlite3
import csv
from datetime import datetime
import ast
import sys

DATA_FILE = 'db.sqlite'


def get_icd10_to_omop(filename):
    code = dict()
    with open(filename) as file:
        row = csv.reader(file, delimiter="\t")
        next(row)  # Skipping first line
        for i in row:
            code[i[0]] = i
    return code


def insert_conceptions(conn, filename):
    with open(filename) as file:
        row = csv.reader(file, delimiter="\t")
        next(row)  # Skipping first line
        for i in row:
            conn.execute(
                "INSERT INTO CONCEPT(concept_id, concept_name, domain_id, vocabulary_id, concept_class_id, standard_concept, concept_code, valid_start_date, valid_end_date, invalid_reason) "
                "VALUES(?,?,?,?,?,?,?,?,?,?)",
                (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9]))


def create_person(conn, person):
    conn.execute(
        "INSERT INTO PERSON(person_id, gender_source_value, gender_concept_id, birth_datetime, year_of_birth, month_of_birth, day_of_birth, race_concept_id, ethnicity_concept_id) "
        "VALUES(?,?,?,?,?,?,?,?,?);", person)


def create_observation_period(conn, period):
    conn.execute(
        "INSERT INTO OBSERVATION_PERIOD(observation_period_id, person_id, observation_period_start_date, observation_period_end_date, period_type_concept_id) "
        "VALUES(?,?,?,?,?);", period)


def create_condition_occurrence(conn, occurrence):
    conn.execute(
        "INSERT INTO CONDITION_OCCURRENCE(condition_occurrence_id, person_id, condition_concept_id, condition_start_date, condition_type_concept_id, condition_source_concept_id, condition_source_value) "
        "VALUES(?,?,?,?,?,?,?);", occurrence)


def create_procedure_occurrence(conn, occurrence):
    conn.execute(
        "INSERT INTO PROCEDURE_OCCURRENCE(procedure_occurrence_id, person_id, procedure_concept_id, procedure_date, procedure_type_concept_id, procedure_source_concept_id, procedure_source_value) "
        "VALUES(?,?,?,?,?,?,?);", occurrence)


def create_observation(conn, observation):
    conn.execute(
        "INSERT INTO OBSERVATION(observation_id, person_id, observation_concept_id, observation_date, observation_type_concept_id, observation_source_concept_id, observation_source_value) "
        "VALUES(?,?,?,?,?,?,?);", observation)

try:
    codes = get_icd10_to_omop('../data/ICD10/icd10_to_omop.tsv')  # Path to the file icd10_to_omop.tsv file
except:
    print("Andmebaasi lisamiseks vajalik fail 'icd10_to_omop.tsv' puudub. Võtke ühendust autoriga")
    sys.exit(1)

try:
    print("Trying to connect ...")

    connection = sqlite3.connect(DATA_FILE)

    print("Connected")

    person_id = 0
    condition_occurrence_id = 0
    observation_id = 0
    procedure_occurrence_id = 0
    observation_period_id = 0

    connection.execute("DELETE FROM PERSON;")
    connection.execute("DELETE FROM OBSERVATION_PERIOD;")
    connection.execute("DELETE FROM CONDITION_OCCURRENCE;")
    connection.execute("DELETE FROM PROCEDURE_OCCURRENCE;")
    connection.execute("DELETE FROM OBSERVATION;")

    connection.execute("DELETE FROM DRUG_EXPOSURE;")
    connection.execute("DELETE FROM DRUG_ERA;")
    connection.execute("DELETE FROM COST;")
    connection.execute("DELETE FROM MEASUREMENT;")
    connection.execute("DELETE FROM VISIT_DETAIL;")
    connection.execute("DELETE FROM PAYER_PLAN_PERIOD;")
    connection.execute("DELETE FROM VISIT_OCCURRENCE;")
    connection.execute("DELETE FROM DEVICE_EXPOSURE;")
    connection.execute("DELETE FROM SPECIMEN;")
    connection.execute("DELETE FROM NOTE_NLP;")
    connection.execute("DELETE FROM NOTE;")
    connection.execute("DELETE FROM PROVIDER;")
    connection.execute("DELETE FROM DRUG_STRENGTH;")
    connection.execute("DELETE FROM CONCEPT;")
    connection.execute("DELETE FROM SOURCE_TO_CONCEPT_MAP;")
    connection.execute("DELETE FROM LOCATION;")
    connection.execute("DELETE FROM METADATA;")
    connection.execute("DELETE FROM DEATH;")
    connection.execute("DELETE FROM COHORT_ATTRIBUTE;")
    connection.execute("DELETE FROM DOSE_ERA;")
    connection.execute("DELETE FROM CARE_SITE;")
    connection.execute("DELETE FROM CONDITION_ERA;")
    connection.execute("DELETE FROM FACT_RELATIONSHIP;")
    connection.execute("DELETE FROM CONCEPT_ANCESTOR;")
    connection.execute("DELETE FROM COHORT;")
    connection.execute("DELETE FROM CONCEPT_CLASS;")
    connection.execute("DELETE FROM CDM_SOURCE;")
    connection.execute("DELETE FROM CONCEPT_SYNONYM;")
    connection.execute("DELETE FROM RELATIONSHIP;")
    connection.execute("DELETE FROM CONCEPT_RELATIONSHIP;")

    insert_conceptions(connection, "../data/ICD10/concept.tsv")

    print("Inserting data to database")

    with open("../output/diagnoses.csv", encoding="utf8") as file:
        read = csv.reader(file, delimiter="\t")
        next(read)
        for row in read:
            if len(list(ast.literal_eval(row[7]))) == 0:
                continue
            # Create person
            person_id += 1
            create_person(connection, (
                person_id,
                row[1],
                8507 if row[1] == "M" else 8532,
                datetime.strptime(row[2], '%Y-%m-%d'),
                datetime.strptime(row[2], '%Y-%m-%d').year,
                datetime.strptime(row[2], '%Y-%m-%d').month,
                datetime.strptime(row[2], '%Y-%m-%d').day,
                0, 1))
            # Insert observation period
            observation_period_id += 1
            create_observation_period(connection, (
                observation_period_id,
                person_id,
                datetime.timestamp(datetime.strptime(list(ast.literal_eval(row[7]))[0][1], '%Y-%m-%d')),
                datetime.timestamp(datetime.strptime(list(ast.literal_eval(row[7]))[-1][1], '%Y-%m-%d')),
                44814724
            ))
            # Insert persons' diagnoses
            diagnoses = list(ast.literal_eval(row[7])) if len(list(ast.literal_eval(row[8]))) == 0 else list(
                ast.literal_eval(row[8]))
            for diagnosis in diagnoses:
                if codes[diagnosis[0]][3] == 'Condition':
                    condition_occurrence_id += 1
                    create_condition_occurrence(connection, (
                        condition_occurrence_id,
                        person_id,
                        codes[diagnosis[0]][2],
                        datetime.timestamp(datetime.strptime(diagnosis[1], '%Y-%m-%d')),
                        32020,
                        codes[diagnosis[0]][1],
                        diagnosis[0]
                    ))
                elif codes[diagnosis[0]][3] == 'Procedure':
                    procedure_occurrence_id += 1
                    create_procedure_occurrence(connection, (
                        procedure_occurrence_id,
                        person_id,
                        codes[diagnosis[0]][2],
                        datetime.timestamp(datetime.strptime(diagnosis[1], '%Y-%m-%d')),
                        38000275,
                        codes[diagnosis[0]][1],
                        diagnosis[0]
                    ))
                elif codes[diagnosis[0]][3] == 'Observation':
                    observation_id += 1
                    create_observation(connection, (
                        observation_id,
                        person_id,
                        codes[diagnosis[0]][2],
                        datetime.timestamp(datetime.strptime(diagnosis[1], '%Y-%m-%d')),
                        38000276,
                        codes[diagnosis[0]][1],
                        diagnosis[0]
                    ))

    connection.commit()
    print("Finished inserting")
    connection.close()

except:
    print('Connection refused! Check diagnoses.csv and db.sqlite files existence')
