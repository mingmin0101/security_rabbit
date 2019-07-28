from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.conf import settings
from django.core.files import File
from .models import computerList, scanningHistory, scanningDetails, fileInfo, Documents
from .forms import DocumentForm
from .serializers import computerListSerializer, scanningHistorySerializer
from rest_framework import generics
import os

# Create your views here.
def userPage(request):
    lists = computerList.objects.all()
    return render(request,'user.html',locals()) 

def showDetail(request,computerName):
    try:
        lists = computerList.objects.get(computerName=computerName)
        scanning_lists = scanningHistory.objects.filter(computer__computerName=computerName)
        print(scanning_lists)
        if lists != None:
            return render(request, 'computer.html', locals())
    except:
        return redirect('/user')
def showScanningDetail(request,computerName,sequence):
        try:
            lists = computerList.objects.get(computerName=computerName)
            scanning_lists = scanningHistory.objects.filter(computer__computerName=computerName)
            scanning_histories = scanningDetails.objects.filter(scanning_history_id__scan_sequence=sequence)
            if scanning_histories != None:
                    return render(request, 'scanningDetail.html',locals())
        except:
            return redirect('/user')

def showFileDetail(request,computerName,fileName):
        try:
           return render(request,'fileInfo.html',locals())
        except:
           return redirect('/user')


class computerListCreate(generics.ListCreateAPIView):
        queryset = computerList.objects.all()
        serializer_class = computerListSerializer

class scanningHistoryListCreate(generics.ListCreateAPIView):
        queryset = scanningHistory.objects.all()
        serializer_class = scanningHistorySerializer

# def example(request):
#     lists = computer_list.objects.all()
#     return render(request,'user.html',locals()) 

def uploadxml(request):
    if (request.POST):
        form = DocumentForm(request.POST,request.FILES)
        if form.is_valid:
            new_doc = Documents(file = request.FILES['docfile'])
            new_doc.save()
    else:
        form = DocumentForm()
    return render(request,'uploadxml.html',{'form':form})

def downloadexe(request,filename):
    file_path = os.path.join(settings.MEDIA_ROOT,'exefiles',filename+'.exe')
    with open(file_path,'rb') as f:
        file = File (f)
        response = HttpResponse(file.chunks(),content_type='APPLICATION/OCTET-STREAM')
        response['Content-Disposition'] = 'attachment; filename=' + filename + '.exe'
        response['Content-Length'] = os.path.getsize(file_path)
    return response