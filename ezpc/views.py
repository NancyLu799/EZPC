from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from ezpc.models import UploadForm,Upload
from django.core.urlresolvers import reverse
from django.conf import settings
import os
import subprocess
from subprocess import Popen
import time

# Create your views here.

def home(request):
    return render(request,'ezpc/home.html')

def input(request):
    file=UploadForm()
    files=Upload.objects.all()
    return render(request,'ezpc/input.html',{'form':file,'files':file})
    
def submit(request):
    afile = request.FILES['featureFile']
    featureFileName = settings.MEDIA_ROOT + '/files/' + str(afile)
    featureFileName = featureFileName.replace('\\','/')
    print('featureFile:' + featureFileName)
    instance = Upload(files = afile)
    instance.save()
        
    afile = request.FILES['ccFile']
    ccFileName = settings.MEDIA_ROOT + '/files/' + str(afile)
    ccFileName = ccFileName.replace('\\','/')
    print('ccFile:' + ccFileName)
    instance = Upload(files = afile)
    instance.save()
    
    afile = request.FILES['rcFile']
    rcFileName = settings.MEDIA_ROOT + '/files/' + str(afile)
    rcFileName = rcFileName.replace('\\','/')
    print('rcFile:' + rcFileName)
    instance = Upload(files = afile)
    instance.save()
    
    afile = request.FILES['gcFile']
    gcFileName = settings.MEDIA_ROOT + '/files/' + str(afile)
    gcFileName = gcFileName.replace('\\','/')
    print('gcFile:' + gcFileName)
    instance = Upload(files = afile)
    instance.save()
    
    min = request.POST.get("min")
    max = request.POST.get("max")

    ezpcfile = os.path.abspath("ezpc/ezpc.pl")
    ezpcfile = ezpcfile.replace('\\','/')
    
    parsedfile = os.path.abspath("ezpc/extract_solution.pl")
    parsedfile = parsedfile.replace('\\', '/')
    
    solutionfileName = settings.MEDIA_ROOT + '/files/' + 'solution.txt'
    solutionfileName = solutionfileName.replace('\\', '/')
    print (solutionfileName)
    
    tablefileName = settings.MEDIA_ROOT + '/files/' + 'solution.csv'
    tablefileName = tablefileName.replace('\\', '/')
    
    #call perl program
    pipe = subprocess.Popen(["perl", ezpcfile, featureFileName, ccFileName, rcFileName, gcFileName, min, max, solutionfileName], stdout=subprocess.PIPE, shell=True)
    print("subprocess 1 completed.")
    time.sleep(1)
    pipe = subprocess.Popen(["perl", parsedfile, solutionfileName])
    print("subprocess 2 completed")
    
    time.sleep(2)
    return HttpResponseRedirect('/media/files/parsedsolution.txt')

# Create your views here.
