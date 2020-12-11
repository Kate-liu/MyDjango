# -*- coding: utf-8 -*-
import logging
import time

logger = logging.getLogger(__name__)


def performance_logger_middleware(get_response):
    def middleware(request):
        start_time = time.time()

        response = get_response(request)

        duration = time.time() - start_time
        response["X-page-Duration-ms"] = int(duration * 1000)

        logger.info("%s %s %s", duration, request.path, request.GET.dict())
        return response

    return middleware