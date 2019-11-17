from celery import shared_task
from celery.task import task
import csv
import os
import json
from apps.csv_handler.models import CsvRecords, CsvFile


@task(name='Generate downloadable csv file')
def generate_file(job_id, filename, start_from, end_at):
    job = CsvFile.objects.filter(pk=int(job_id)).first()

    csv_records = CsvRecords.objects.filter(file=job, range__gte=start_from, range__lte=end_at)
    with open(filename, "w+", encoding="utf8", errors='ignore') as f:
        writer = csv.writer(f, dialect=csv.excel)
        fields = json.loads(job.fields_str)
        writer.writerow(fields)
        for rec in csv_records:
            rec = json.loads(rec.record_str)
            writer.writerow(rec)

    return filename


@shared_task(name='Read uploaded CSV, process & persist')
def process_csv_to_persist(dir_name, csf):
    file_name = dir_name + '/file.csv'
    row_count = 0
    fields = []
    rows = []
    csf = CsvFile.objects.filter(pk=csf).first()
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
        csv_records.append(CsvRecords(u_id=u_id, range=pos, record_str=json.dumps(row), file=csf))

    # updating DB
    try:
        CsvRecords.objects.bulk_create(csv_records)
        csf.total_records = total_records
        csf.failed_records = failed_records
        csf.processed_records = processed_records
        csf.fields_str = json.dumps(fields)
        csf.status = 'finished'
        csf.save()
    except Exception:
        csf.total_records = total_records
        csf.failed_records = 0
        csf.processed_records = 0
        csf.fields_str = json.dumps([])
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
            if row_count == 0:
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


def write_csv(file_name, records):
    try:
        pass
    except Exception:
        pass