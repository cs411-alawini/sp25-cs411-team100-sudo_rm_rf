from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.template import loader

from .models import Rxnconso
from .forms import getRxaui

def index(request):
    return HttpResponse("testing")

def searchbox(request):
    template = loader.get_template("db_retrieve/search.html")
    return HttpResponse(template.render(request))

def result(request, aui):
    id = get_object_or_404(Rxnconso, pk = aui)
    return render(request, "db_retrieve/results.html", {"str" : id})

def searchresult(request, aui):
    drug_instance = get_object_or_404(Rxconsno, pk = aui)

    return render(request, "db_retrieve/results.html", {"Drug name": rxnconso})

