import traceback

from django.shortcuts import render, redirect

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status

from .forms import UploadFileForm  
from .models import UploadedData
from .parsers import ParserFactory
from .serializers import FileQuerySerializer

# ===============================
# BUSINESS LOGIC
# ===============================

def handle_uploaded_file(uploaded_file):
    """Process and store the uploaded data file."""
    file_name = uploaded_file.name.rsplit('.', 1)[0]
    file_type = uploaded_file.name.split('.')[-1].upper()

    parser = ParserFactory.get_parser(file_type)
    parsed_data = parser.parse(uploaded_file.read().decode())

    if UploadedData.objects.exists():
        UploadedData.objects.all().delete()

    for record in parsed_data:
        record['table_name'] = file_name
        UploadedData.objects.create(data=record)

    return True


def execute_query(search_term):
    """Search for the provided term in the stored data."""
    matching_records = UploadedData.objects.filter(data__icontains=search_term).values_list('data', flat=True)
    return list(matching_records)

# ===============================
# INTERFACE LOGIC
# ===============================

# HTML Interfaces

def upload_data_view(request):
    """View for uploading data files via the web interface."""
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                handle_uploaded_file(request.FILES['file'])
                return redirect('query_data_view')
            except ValueError:
                return render(request, 'upload.html', {'form': form, 'error': "Invalid file type."})
            except Exception as e:
                print("Exception occurred. Details:", str(e), "Traceback:", traceback.format_exc())
                return render(request, 'upload.html', {'form': form, 'error': str(e)})
        else:
            return render(request, 'upload.html', {'form': form})
    else:
        form = UploadFileForm()
        return render(request, 'upload.html', {'form': form})

def query_data_view(request):
    """View for querying the uploaded data via the web interface."""
    all_data = UploadedData.objects.all().values_list('data', flat=True)
    if request.method == 'POST':
        query_type = request.POST.get('type')
        try:
            result = execute_query(query_type) 
            return render(request, 'query.html', {'query_result': result, 'data_objects': all_data})
        except Exception as e:
            return render(request, 'query.html', {'error': f"Error processing query: {e}", 'data_objects': all_data})
    else:
        return render(request, 'query.html', {'data_objects': all_data})


# REST API Interfaces

class FileQueryAPI(APIView):
    """API view to accept data file and type and return the type results."""
    parser_classes = [MultiPartParser]

    def post(self, request):
        serializer = FileQuerySerializer(data=request.data)

        if serializer.is_valid():
            uploaded_file = serializer.validated_data['file']

            try:
                handle_uploaded_file(uploaded_file)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            query_type = serializer.validated_data.get('type', None)
            if query_type:
                try:
                    query_result = execute_query(query_type)
                    return Response({"query_result": query_result}, status=status.HTTP_200_OK)
                except Exception as e:
                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            else:
                all_data = UploadedData.objects.all().values_list('data', flat=True)
                return Response({"data": list(all_data)}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
