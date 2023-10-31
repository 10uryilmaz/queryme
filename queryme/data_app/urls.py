from django.urls import path
from .views import upload_data_view, query_data_view, FileQueryAPI

urlpatterns = [
    path('upload/', upload_data_view, name='upload_data_view'),
    path('query/', query_data_view, name='query_data_view'),
    path('file-query/', FileQueryAPI.as_view(), name='file_query'),
]
