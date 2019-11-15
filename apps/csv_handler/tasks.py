from celery import shared_task
import csv, os
from apps.csv_handler.models import CsvFile, CsvRecords


@shared_task
def process_csv_to_persist(dir_name, csf):
    file_name = dir_name + '/file.csv'
    row_count = 0
    fields = []
    rows = []

    while True:
        is_done, fields, rows, row_count = read_csv(file_name, fields, rows, row_count)
        if is_done:
            break
        else:
            row_count += 1

    # status = 'finished' if is_done else 'error'

    input_file = open(file_name, "r+")
    reader_file = csv.reader(input_file)
    total_records = sum(1 for row in reader_file) - 1
    failed_records = row_count - total_records

    csv_records = []
    for row in rows:
        u_id = row[0]
        csv_records.append(CsvRecords(u_id=u_id, record_str=str(row), file=csf))
    CsvRecords.objects.bulk_create(csv_records)
    csf.total_records = total_records
    csf.failed_records = failed_records
    csf.status = 'finished'
    csf.save()

    # deleting the directory now
    if os.path.exists(file_name):
        os.remove(file_name)
    os.rmdir(dir_name)


def read_csv(file_name, fields, rows, row_count):
    try:
        # Reading csv file
        with open(file_name, 'r') as csv_file:
            # creating a csv reader object
            csv_reader = csv.reader(csv_file)

            # extracting each data row one by one
            i = 0
            for row in csv_reader:
                if i == row_count:
                    rows.append(row)
                    row_count += 1
                i += 1

        return True, fields, rows, row_count
    except:
        return False, fields, rows, row_count
