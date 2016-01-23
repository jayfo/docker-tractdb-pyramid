import pyramid.config
import pyramid.response
import pyramid.view


@pyramid.view.view_defaults(route_name='yo', renderer='json')
class YoView:
    def __init__(self, request):
        self.request = request

    @pyramid.view.view_config(request_method='GET')
    def get(self):
        return 'yo'
