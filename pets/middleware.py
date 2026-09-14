import time

class PerfomanceLoggingMiddleware:
    """замеряет время выполнения запроса"""
    def __init__(self, get_response):
        '''get_response-самаView'''
        self.get_response = get_response

    def __call__(self, request):
        '''До передачи во View'''
        start_time = time.perf_counter()
        # Передаем дальше по цепочке
        response = self.get_response(request)
        # после выполнения View
        duration = time.perf_counter()-start_time
        response['X-Page-Render-Duration'] = f'{duration:.4f} sec'
        return response