from django.db import models


class CsvFile(models.Model):
    class Meta:
        db_table = 'csv_file'

    status = models.CharField(default='processing', max_length=20)
    total_records = models.IntegerField(default=0)
    processed_records = models.IntegerField(default=0)
    failed_records = models.IntegerField(default=0)


class CsvRecords(models.Model):
    u_id = models.CharField(null=False, max_length=100)
    record_str = models.CharField(max_length=10000)
    range = models.IntegerField(null=False, default=0)
    file = models.ForeignKey(CsvFile, on_delete=models.ProtectedError)

    class Meta:
        db_table = 'csv_record'
        unique_together = ('u_id', 'file')
