from django.shortcuts import render

def index(request):
    return render(request, 'effMobApp/index.html')

def error(request):
    return render(request, 'effMobApp/error.html')

def external_api_demo(request):
    return render(request, 'effMobApp/externalApi.html')

