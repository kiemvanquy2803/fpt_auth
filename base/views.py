import time
from django.utils import timezone
import logging

logging.basicConfig(filename='app.log',level=logging.INFO)
request_logger = logging.getLogger('api.request.logger')

# Create your views here.
class LoggingTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)

        duration = time.time() - start_time
        msg = "method=%s path=%s status=%s duration=%s date=%s"
        args = (request.method,
                request.path,
                response.status_code,
                duration,
                timezone.datetime.now()
                )

        request_logger.info(msg, *args)
        return response