from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect 
from ezpc.models import UploadForm,Upload
from django.core.urlresolvers import reverse
from django.conf import settings
import os, shutil, time, random, subprocess
from subprocess import Popen


def home(request):
    if request.session.session_key:
        request.session.modified = True #Generates new session ID     
    request.session.save()
    sessionkey = request.session.session_key
    sessionkey = sessionkey.replace(':', '_')
    print ('sessionid:' + sessionkey)
    return render(request,'ezpc/home.html')


def input(request):
    file=UploadForm()
    files=Upload.objects.all()
    return render(request,'ezpc/input.html',{'form':file,'files':file})
   
    
def submit(request):
    sessionkey = request.session.session_key
    sessionkey = sessionkey.replace(':', '_')
    print ('sessionid:' + sessionkey)
    
    newpath = settings.MEDIA_ROOT + '/files/' + sessionkey + '/'
    if os.path.exists(newpath):
        shutil.rmtree(newpath)       
    os.makedirs(newpath)        
          
    if 'featureFile' in request.FILES:
        afile = request.FILES['featureFile']
        feature = settings.MEDIA_ROOT + '/files/' + str(afile)
        feature = feature.replace('\\','/')
        instance = Upload(files = afile)
        instance.save()
        ffNew = settings.MEDIA_ROOT + '/files/' + sessionkey + '/' + str(afile)
        os.rename(feature, ffNew) 
    else:
        return HttpResponse('You are missing at least one file. Please upload a Column Constraints File')
    
    if 'ccFile' in request.FILES:    
        afile = request.FILES['ccFile']
        ccFileName = settings.MEDIA_ROOT + '/files/' + str(afile)
        ccFileName = ccFileName.replace('\\','/')       
        instance = Upload(files = afile)
        instance.save()
        ccNew = settings.MEDIA_ROOT + '/files/' + sessionkey + '/' + str(afile)
        os.rename(ccFileName, ccNew) 
        print('ccFile:' + ccNew)
    else:
        return HttpResponse('You are missing at least one file. Please upload a Column Constraints File')
    
    if 'rcFile' in request.FILES:       
        afile = request.FILES['rcFile']
        rcFileName = settings.MEDIA_ROOT + '/files/' + str(afile)
        rcFileName = rcFileName.replace('\\','/')  
        instance = Upload(files = afile)
        instance.save()
        rcNew = settings.MEDIA_ROOT + '/files/' + sessionkey + '/' + str(afile)
        rcNew = rcNew.replace('\\', '/')
        os.rename(rcFileName, rcNew) #rename file w/ userkey
        print('rcFile:' + rcNew)
    else:
        return HttpResponse('You are missing at least one file. Please upload a Candidate Availability File')
    
    if 'gcFile' in request.FILES:      
        afile = request.FILES['gcFile']
        gcFileName = settings.MEDIA_ROOT + '/files/' + str(afile)
        gcFileName = gcFileName.replace('\\','/')     
        instance = Upload(files = afile)
        instance.save()
        gcNew = settings.MEDIA_ROOT + '/files/' + sessionkey + '/' + str(afile)
        os.rename(gcFileName, gcNew) #rename file w/ userkey
        print('gcFile:' + gcNew)
    else:
        return HttpResponse('You are missing at least one file. Please upload a Group Constraints File')
    
    min = request.POST.get("min")      
    max = request.POST.get("max") 

    ezpcfile   = os.path.abspath("ezpc/ezpc.pl")
    ezpcfile   = ezpcfile.replace('\\','/')
    parser     = os.path.abspath("ezpc/extract_solution.pl")
    parser     = parser.replace('\\', '/')
    csvToTable = os.path.abspath("ezpc/csvToTable.py")
    csvToTable = csvToTable.replace('\\','/')
    
    solutionfileName = settings.MEDIA_ROOT + '/files/' + sessionkey + '/' +'solution.txt'
    solutionfileName = solutionfileName.replace('\\', '/')
    parsedsolution = settings.MEDIA_ROOT + '/files/' + sessionkey + '/' + 'parsed.txt'
    parsedsolution = parsedsolution.replace('\\', '/')
    table = settings.MEDIA_ROOT + '/files/' + sessionkey + '/' + 'table.html'
    table = table.replace('\\', '/')
    finaltable = "/media/files/" + sessionkey + '/' + 'table.html'
      
    pipe = subprocess.Popen(["perl", ezpcfile, ffNew, ccNew, rcNew, gcNew, min, max, solutionfileName])
    print("subprocess 1 completed.")
    time.sleep(0.5)
    pipe = subprocess.Popen(["perl", parser, solutionfileName, parsedsolution])
    print("subprocess 2 completed") 
    time.sleep(1)
    pipe = subprocess.Popen(["python", csvToTable, ffNew, table, parsedsolution]) 
    time.sleep(1)
    return HttpResponseRedirect(finaltable)



