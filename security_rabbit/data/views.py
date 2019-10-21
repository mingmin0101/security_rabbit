from data.models import Computer, ScanningRecord, FileInfo
from users.models import User
from data.serializers import ComputerSerializer, ScanningRecordSerializer,FileInfoSerializer, FileNameSerializer
from users.serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.conf import settings
from django.core.files import File
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Documents
from .forms import DocumentForm
import os
import zipfile

from data.tasks import calculate_score
def process_uploaded_file(request):
    pass

# API endpoint that allows users to be viewed or edited.
@api_view(['GET'])
def ComputerView(request):
    """
    Show the computer controlled by the current user.
    https://www.django-rest-framework.org/api-guide/filtering/
    """
    try:
        querylist = (
            UserSerializer(User.objects.filter(id = request.user.id), many=True).data,
            ComputerSerializer(Computer.objects.filter(administrator = request.user), many=True).data,
        )

        return Response(querylist)

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

def download_scanfile(request):  # , userid
    file_path = os.path.join(settings.MEDIA_ROOT,"exefiles","solfege.exe")
    with open(file_path,'rb') as f:
        file = File (f)
        response = HttpResponse(file.chunks(), content_type='APPLICATION/OCTET-STREAM')
        response['Content-Disposition'] = 'attachment; filename=solfege.exe'
        response['Content-Length'] = os.path.getsize(file_path)
    return response

###############################

def uploadxml(request):
    if (request.POST):
        form = DocumentForm(request.POST,request.FILES)
        if form.is_valid:
            new_doc = Documents(file = request.FILES['docfile'])
            new_doc.save()
    else:
        form = DocumentForm()
    return render(request,'uploadxml.html',{'form':form})


def downloadzip(request,filename):
    sigcheck_name = 'sigcheck64.exe'
    main_name = '__main__.exe'
    userdb_name = 'userdb_filter.txt'
    sigcheck_path = os.path.join(settings.MEDIA_ROOT,'exefiles','sigcheck64.exe')
    main_path = os.path.join(settings.MEDIA_ROOT,'exefiles','__main__.exe')
    userdb_path = os.path.join(settings.MEDIA_ROOT,'exefiles','userdb_filter.txt')
    srzip_name = 'srcore.zip'
    with zipfile.ZipFile(srzip_name,'w') as z_file:
        z_file.write(sigcheck_path, 'sigcheck64.exe')
        z_file.write(main_path, '__main__.exe')
        z_file.write(userdb_path, 'userdb_filter.txt')
    
    with open(srzip_name, 'rb') as z_file:
        data = z_file.read()
        response = HttpResponse(data, content_type='application/zip')
        response['Content-Disposition'] = 'attachment;filename='+ srzip_name

    return response
