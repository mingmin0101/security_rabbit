from data.models import Computer, ScanningRecord, FileInfo
from data.serializers import ComputerSerializer, ScanningRecordSerializer,FileInfoSerializer, FileNameSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


# API endpoint that allows users to be viewed or edited.
@api_view(['POST'])
def ComputerView(request):
    """
    Show the computer controlled by the current user.
    https://www.django-rest-framework.org/api-guide/filtering/
    """
    try:
        computer = Computer.objects.filter(administrator = request.user)
        serializer = ComputerSerializer(computer, many=True)
        return Response(serializer.data)

    except Computer.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def ScanningRecordView(request):
    """
    Show the selected computer(by primary key of Computer Model) controlled by the current user.
    Show the Scanning Records of the selected computer.
    """
    try:
        computerID = request.query_params['computerID']
        computer = Computer.objects.filter(administrator=request.user).filter(id=computerID)
        querylist = (
            ComputerSerializer(computer, many=True).data,
            ScanningRecordSerializer(ScanningRecord.objects.filter(computer = computerID), many=True).data,
        )
        return Response(querylist)

    except Computer.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def ScanningDetailsView(request):
    '''
    Show ScanningDetails by id.
    '''
    try:
        scanID = request.query_params['scanID']

        querylist = (
            ComputerSerializer(Computer.objects.filter(administrator = request.user).filter(id = ScanningRecord.objects.get(scan_id=scanID).computer.id), many=True).data,
            ScanningRecordSerializer(ScanningRecord.objects.filter(scan_id=scanID), many=True).data,
            FileNameSerializer(FileInfo.objects.filter(scanningRecord_id=scanID), many=True).data,
        )
        return Response(querylist)

    except Computer.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def FileInfoView(request):

    try:
        fileID = request.query_params['fileID']
        file = FileInfo.objects.filter(id = fileID)
        file_get = FileInfo.objects.get(id = fileID)
        sc = ScanningRecord.objects.filter(scan_id = file_get.scanningRecord_id.scan_id)
        sc_get = ScanningRecord.objects.get(scan_id = file_get.scanningRecord_id.scan_id)
        querylist = (
            ComputerSerializer(Computer.objects.filter(administrator = request.user).filter(id = sc_get.computer.id), many=True).data,
            ScanningRecordSerializer(sc, many=True).data,
            FileInfoSerializer(file, many=True).data,
        )
        return Response(querylist)
        
    except Computer.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)


###############################
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Documents
from django.conf import settings
from django.core.files import File
from .forms import DocumentForm
import os

def uploadxml(request):
    if (request.POST):
        form = DocumentForm(request.POST,request.FILES)
        if form.is_valid:
            new_doc = Documents(file = request.FILES['docfile'])
            new_doc.save()
    else:
        form = DocumentForm()
    return render(request,'uploadxml.html',{'form':form})

def downloadpy(request,filename):
    file_path = os.path.join(settings.MEDIA_ROOT,'exefiles',filename+'.py')
    with open(file_path,'rb') as f:
        file = File (f)
        response = HttpResponse(file.chunks(),content_type='APPLICATION/OCTET-STREAM')
        response['Content-Disposition'] = 'attachment; filename=' + filename+'.py'
        response['Content-Length'] = os.path.getsize(file_path)
    return response

def downloadexe(request,filename):
    file_path = os.path.join(settings.MEDIA_ROOT,'exefiles',filename+'.exe')
    with open(file_path,'rb') as f:
        file = File (f)
        response = HttpResponse(file.chunks(),content_type='APPLICATION/OCTET-STREAM')
        response['Content-Disposition'] = 'attachment; filename=' + filename+'.exe'
        response['Content-Length'] = os.path.getsize(file_path)
    return response

def downloadtxt(request,filename):
    file_path = os.path.join(settings.MEDIA_ROOT,'exefiles',filename+'.txt')
    with open(file_path,'rb') as f:
        file = File (f)
        response = HttpResponse(file.chunks(),content_type='APPLICATION/OCTET-STREAM')
        response['Content-Disposition'] = 'attachment; filename=' + filename+'.txt'
        response['Content-Length'] = os.path.getsize(file_path)
    return response