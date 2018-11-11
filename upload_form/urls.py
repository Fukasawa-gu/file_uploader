from django.conf.urls import url
from django.urls import include, path
from upload_form import views

app_name = 'upload_form'# これ大事namespaceとかで必要

urlpatterns = [
    url(r'^$', views.form, name = 'form'),
    url(r'^complete/', views.complete, name = 'complete'),
]
