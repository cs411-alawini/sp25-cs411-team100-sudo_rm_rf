from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse
#from django.views import generic
#from django.template import loader
from django.views.generic.list import ListView
from django.db.models import Q

from .models import Rxnconso
from .forms import getRxaui

def index(request):
    return HttpResponse("testing")


def searchbox(request):
    query = request.GET.get("drug_id_input")
    #return redirect("result/", aui=query)
    #return redirect(result, aui = query)
    return render(request, "db_retrieve/search.html")

def search(request):
    return render(request, "db_retrieve/search.html")
    #vectors = Rxnconso.objects.all()
    #result = Rxnconso.objects.filter(Q(rxaui__icontains = query))
    #return result(request, query)

def result(request):
    query = request.GET.get("searched_aui")
    result = Rxnconso.objects.get(rxaui = str(query))
    return render(request, "db_retrieve/results.html", {"result" : result})
    """
    else:
        id = get_object_or_404(Rxnconso, pk = aui)
        return render(request, "db_retrieve/results.html", {"str" : id})
    """

"""
def searchresult(request, aui):
    drug_instance = get_object_or_404(Rxnconso, pk = aui)

    return render(request, "db_retrieve/results.html", {"Drug name": rxnconso})
"""
