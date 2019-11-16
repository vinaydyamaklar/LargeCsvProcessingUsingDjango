from celery import shared_task, task
import csv
import os
import codecs
from apps.csv_handler.models import CsvRecords, CsvFile


@task
def generate_file(job_id, start_from, start_to):
    filename = "%s.csv" % generate_file.request.id
    file = CsvFile.objects.get(id=job_id)
    records = CsvRecords.objects.filter(file=file)
    with open("%s%s" % ("/path/to/export/", filename), "w+") as f:
        writer = csv.writer(f, dialect=csv.excel)

        # for i in qs:
        #     writer.writerow([i.foo, i.bar, i.baz, ...])

    return filename


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

    input_file = open(file_name, "r+", encoding="utf8", errors='ignore')
    reader_file = csv.reader(input_file)
    total_records = sum(1 for row in reader_file) - 1
    failed_records = total_records - len(rows)
    processed_records = total_records - failed_records

    csv_records = []
    pos = 0
    for row in rows:
        u_id = row[0] + str(csf.pk)
        pos += 1
        csv_records.append(CsvRecords(u_id=u_id, range=pos, record_str=str(row), file=csf))

    # updating DB
    try:
        CsvRecords.objects.bulk_create(csv_records)
        csf.total_records = total_records
        csf.failed_records = failed_records
        csf.processed_records = processed_records
        csf.status = 'finished'
        csf.save()
    except Exception:
        csf.total_records = total_records
        csf.failed_records = 0
        csf.processed_records = 0
        csf.status = 'error'
        csf.save()
        pass
    finally:
        # deleting the directory now
        if os.path.exists(file_name):
            os.remove(file_name)
        os.rmdir(dir_name)


def read_csv(file_name, fields, rows, row_count):
    try:
        # Reading csv file
        with open(file_name, 'r', encoding="utf8", errors='ignore') as csv_file:
            # creating a csv reader object
            csv_reader = csv.reader(csv_file)

            # extracting field name
            fields = next(csv_reader)

            # extracting each data row one by one
            i = 0
            for row in csv_reader:
                uid = row[0]
                if i == row_count and uid not in [r[0] for r in rows]:
                    rows.append(row)
                    row_count += 1
                i += 1

        return True, fields, rows, row_count
    except Exception:
        return False, fields, rows, row_count
