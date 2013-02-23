# Create your views here.

from django.http import HttpResponse

def home(request):
    st = "Site...see /admin or /gigapans or something"
    return HttpResponse(st)
