from django.shortcuts import render

def showStreamPage(request):
    return render(request, 'stream.html')