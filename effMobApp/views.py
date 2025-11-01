from django.shortcuts import render

def index(request):
    if (request.user and request.user.is_authenticated):
        return render(request, 'effMobApp/index.html', {'user_id': request.user.id})
    return render(request, 'effMobApp/index.html')

def error(request):
    return render(request, 'effMobApp/error.html')

def external_api_demo(request):
    return render(request, 'effMobApp/externalApi.html')

