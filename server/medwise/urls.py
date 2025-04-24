"""
URL configuration for medwise project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from main.rawsearch.views import SearchItemView
from main.views import TopInteractionsView


urlpatterns = [
    path('admin/', admin.site.urls),
    # path("db_retrieve/", include("db_retrieve.urls")),
    path("search/", SearchItemView.as_view(), name = "cui_search"),
    path("api/top-interactions-by-prr", TopInteractionsView.as_view(), name="top_interactions"), # <-- Add new URL pattern
]
