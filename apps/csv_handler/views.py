from django.views.generic import View
from django.shortcuts import render, HttpResponseRedirect, reverse
from django.http import JsonResponse
import os
import json
from main.settings.settings import BASE_DIR
from .tasks import process_csv_to_persist, generate_file
from .models import CsvFile, CsvRecords

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
                process_csv_to_persist(upload_dir_name, csf)
                job_id = "JOB-"+str(csf.pk)
                return JsonResponse({"message": "finished", "job": job_id, "status": "OK"})
            return JsonResponse({"message": "not_finished", "status": "OK"})
        except Exception:
            return JsonResponse({"message": "failed, try again later", "status": "ERROR"})


class JobsView(View):

    def get(self, request, *args, **kwargs):
        # some logic
        context = {}
        jobs_created = CsvFile.objects.all()
        context['jobs'] = jobs_created
        return render(request, 'jobs.html', context)

    def post(self, request, *args, **kwargs):
        try:
            range_from = request.POST['rangeFrom']
            range_to = request.POST['rangeTo']
            job_id = request.POST['jobId']

            task = generate_file.delay(job_id, range_from, range_to)
            return JsonResponse({"download_id": task.task_id, "status": "OK"})
        except:
            return JsonResponse({"message": "failed to download try again later", "status": "ERROR"})
