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
import main.views #import TopInteractionsView, TopDrugsByConditionCountView, DrugInteractingPartnersView, UserRegistrationView, UserLoginView
from main.views import TopInteractionsView, TopDrugsByConditionCountView, DrugInteractingPartnersView, UserRegistrationView, UserLoginView, DrugConditionsView, UserDrugsView, PasswordChangeView


urlpatterns = [
    path('admin/', admin.site.urls),
    # path("db_retrieve/", include("db_retrieve.urls")),
    path("search/", SearchItemView.as_view(), name = "cui_search"),
    path("api/top-interactions-by-prr", TopInteractionsView.as_view(), name="top_interactions"),
    path("api/top-drugs-by-conditions", TopDrugsByConditionCountView.as_view(), name="top_drugs_by_conditions"),
    path("api/interacting-drugs/<str:target_rxcui>", DrugInteractingPartnersView.as_view(), name="interacting_drugs"),
    path("api/users", UserRegistrationView.as_view(), name="user_registration"),
    path("api/login", UserLoginView.as_view(), name="user_login"),
    path("api/conditions", DrugConditionsView.as_view(), name="drug_conditions"),

    path("api/user-add-drugs", main.views.AddMedication.as_view(), name="add_user_drugs"),
    path("api/user-delete-drugs", main.views.DeleteMedication.as_view(), name="delete_user_drugs"),
    path("api/result-sets", main.views.GetResultIds.as_view(), name="get_result_ids"),
    path("api/medication-search", main.views.GetID.as_view(), name="get_name_id"),
    path("api/create-result-set", main.views.CreateResultID.as_view(), name="create_resid"),

    path("api/user-drugs", UserDrugsView.as_view(), name="user_drugs"),
    path("api/password", PasswordChangeView.as_view(), name="password change"),
    
]
