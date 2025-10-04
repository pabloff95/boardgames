from django.http import HttpResponse

def index(request):
    return  HttpResponse("<h1>Game index</h1>")