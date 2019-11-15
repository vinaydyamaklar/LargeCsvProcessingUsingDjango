from celery import shared_task
import csv


@shared_task
def process_csv_to_persist(dir_name):
    print("******************inside celery")
    file_name = dir_name + '/file.csv'
    fields = []
    rows = []

    # Reading csv file
    with open(file_name, 'r') as csv_file:
        # Creating a csv reader object
        csv_reader = csv.reader(csv_file)

        # extracting field name
        fields = next(csv_reader)

        # extracting each data row one by one
        for row in csv_reader:
            if len(fields) == len(row.split(',')):
                rows.append(row)