import pyramid.config
import pyramid.response
import pyramid.view


# @pyramid.view.view_config(route_name='yo', renderer='json')
# def yo(request):
#     return 'yo'

@pyramid.view.view_config(route_name='yo', renderer='json')
class CouchView:
    def __init__(self, request):
        self.request = request

    @pyramid.view.view_config(request_method='GET')
    def get(self):
        return 'yo'
