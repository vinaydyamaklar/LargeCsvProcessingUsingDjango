from django.views.generic import View
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseForbidden, HttpResponse
import os
import json
from datetime import datetime
from main.settings.settings import BASE_DIR
from .tasks import process_csv_to_persist, generate_file
from .models import CsvFile, CsvRecords
from celery.result import AsyncResult

# Create your views here.


class UploadView(View):

    def get(self, request, *args, **kwargs):
        # some logic
        context = {}
        return render(request, 'upload.html', context)

    def post(self, request, *args, **kwargs):
        try:
            upload_dir_name = BASE_DIR+'/media/csv_files/'+request.POST['uploadId']
            if not os.path.exists(upload_dir_name):
                os.makedirs(upload_dir_name)
            filename = upload_dir_name + '/' + 'file.csv'
            with open(filename, 'ab+') as destination:
                for chunk in request.FILES['file'].chunks():
                    destination.write(chunk)

            # calling worker if the last chunk is uploaded successfully
            if json.loads(request.POST['isLastChunk']):
                csf = CsvFile.objects.create(status='processing')
                process_csv_to_persist.delay(upload_dir_name, csf.pk)
                job_id = "JOB-"+str(csf.pk)
                return JsonResponse({"message": "finished", "job": job_id, "status": "OK"})
            return JsonResponse({"message": "not_finished", "status": "OK"})
        except Exception as e:
            return JsonResponse({"message": "failed, try again later", "status": "ERROR"})


class JobsView(View):

    def get(self, request, *args, **kwargs):
        if request.GET.get("taskId", None):
            task_id = request.GET.get("taskId")
            # filename = request.GET.get("filename")

            result = generate_file.AsyncResult(task_id)
            if result.ready():
                return JsonResponse({"message": 'ready', "status": "OK"})
            return JsonResponse({"message": 'not ready', "status": "OK"})

        # if not ajax request just render the file
        context = {}
        jobs_created = CsvFile.objects.all()
        context['jobs'] = jobs_created
        return render(request, 'jobs.html', context)

    def post(self, request, *args, **kwargs):
        try:
            range_from = request.POST.get('rangeFrom', None)
            range_to = request.POST.get('rangeTo', None)
            job_id = request.POST.get('jobId', None)
            if not range_from or not range_to or not job_id:
                return JsonResponse({"message": 'Missing data', "status": "error"})

            csf = CsvFile.objects.filter(pk=int(job_id)).first()
            if not csf:
                return JsonResponse({"message": 'Invalid Job ID', "status": "error"})

            if csf and csf.status != 'finished':
                return JsonResponse({"message": 'Job is not yet finished or there may be some error.',
                                     "status": "error"})

            temp_dir = BASE_DIR + '/media/csv_files/'
            filename = temp_dir + 'JOB-' + str(csf.pk) + '-' + str(datetime.now().timestamp()) + '.csv'

            task = generate_file.delay(job_id, temp_dir, filename, range_from, range_to)
            return JsonResponse({"task_id": str(task.task_id), "filename": filename, "status": "OK"})
        except Exception:
            return JsonResponse({"message": "Unable to download", "status": "ERROR"})

