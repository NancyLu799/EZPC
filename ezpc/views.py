from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from ezpc.models import UploadForm,Upload
from django.core.urlresolvers import reverse
from django.conf import settings
import os
import subprocess
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
    
<<<<<<< HEAD
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
    
    afile = request.FILES['minFile']
    minFileName = settings.MEDIA_ROOT + '/files/' + str(afile)
    minFileName = minFileName.replace('\\','/')
    print('minFile:' + minFileName)
    instance = Upload(files = afile)
    instance.save()
    
    afile = request.FILES['maxFile']
    maxFileName = settings.MEDIA_ROOT + '/files/' + str(afile)
    maxFileName = maxFileName.replace('\\','/')
    print('maxFile:' + maxFileName)
    instance = Upload(files = afile)
    instance.save()
=======
        ezpcfile = os.path.abspath("ezpc/ezpc.pl")
        ezpcfile = ezpcfile.replace('\\','/')
        
        solutionfileName = settings.MEDIA_ROOT + '/files/' + 'solution.txt'
        solutionfileName = solutionfileName.replace('\\', '/')
        print (solutionfileName)
        
        #call perl program
        pipe = subprocess.Popen(["perl", ezpcfile, featureFileName, ccFileName, rcFileName, gcFileName, minFileName, maxFileName, solutionfileName], stdout=subprocess.PIPE, shell=True)
        print("subprocess completed.")        
        
        return HttpResponseRedirect(reverse('fileupload'))
    else:
        file=UploadForm()
        
    files=Upload.objects.all()
    #return("abc")
    return render(request,'ezpc/home.html',{'form':file,'files':file})
>>>>>>> ea4cb294479a79adde6d54ffa792ae02afcd048b

    ezpcfile = os.path.abspath("ezpc/ezpc.pl")
    ezpcfile = ezpcfile.replace('\\','/')
    
    solutionfileName = settings.MEDIA_ROOT + '/files/' + 'solution.txt'
    solutionfileName = solutionfileName.replace('\\', '/')
    print (solutionfileName)
    
    #call perl program
    pipe = subprocess.Popen(["perl", ezpcfile, featureFileName, ccFileName, rcFileName, gcFileName, minFileName, maxFileName, solutionfileName], stdout=subprocess.PIPE, shell=True)
    pipe = subprocess.Popen(["perl", "C:/Users/NancyLu/Desktop/VyasSekar/EZ-PC/extract_solution.pl", 'C:/Users/NancyLu/Desktop/VyasSekar/EZ-PC/solution.txt'], stdout = subprocess.PIPE)
    print("subprocess completed.")
    
    time.sleep(2)
    return HttpResponseRedirect("/media/files/solution.txt")
# Create your views here.
