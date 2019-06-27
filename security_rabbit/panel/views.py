from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import computerList, scanningHistory, scanningDetails, fileInfo

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


# def example(request):
#     lists = computer_list.objects.all()
#     return render(request,'user.html',locals()) 