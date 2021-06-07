from django.shortcuts import render

def showMainPage(request):
    return render(request, 'mainpage.html')