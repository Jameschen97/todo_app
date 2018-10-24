from utils import (
    http_response,
    template,
)


def index(request):
    body = template('todo_ajax.html')
    return http_response(body)


route_dict = {
    '/todo/ajax': index,
}
