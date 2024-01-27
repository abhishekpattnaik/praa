from django.shortcuts import render
from rest_framework import viewsets # , permissions

from data_pull.models import Record
from data_pull.serializers import RecordSerializer
from data_pull.helpers import fetch_new_records
from common.logging_helper import api_logging


class RecordAPIView(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Record.objects.all().order_by('-updated_at')
    serializer_class = RecordSerializer
    permission_classes = []
    
def show_records(request):
    try:
        api_logging.logger.info("API hit for show records %s", str(request))
        template_data = fetch_new_records(request)

        return render(
            request, 
            'show_records.html', 
            template_data
        )
    except Exception as e:
        api_logging.logger.exception(e)
        return render(
            request,
            "internal_error.html"
        )
