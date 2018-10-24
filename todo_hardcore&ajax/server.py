import socket
import urllib.parse
import _thread

from routes import route_static
from routes.routes_user import route_dict as user_routes
from routes.routes_todo import route_dict as todo_routes
from routes.routes_ajax import route_dict as ajax_routes
from routes.api_todo import route_dict as api_routes

from utils import log


# 定义一个 class 用于保存请求的数据
class Request(object):
    def __init__(self):
        self.method = 'GET'
        self.path = {}
        self.query = {}
        self.body = ''
        self.headers = {}
        self.cookies = {}

    def add_cookies(self):
        """
        user=yoo; xx=xx
        """
        cookies = self.headers.get('Cookie', '')
        kvs = cookies.split('; ')
        for kv in kvs:
            if '=' in kv:
                # 这里只切一次,避免报错,这是一个简化程序的做法
                k, v = kv.split('=', 1)
                self.cookies[k] = v

    def add_headers(self, header):
        """
        [
            'Accept-Language: zh-CN,zh;q=0.8'
            'Cookie: user=yoo; xx=xx'
        ]
        """
        # 清空 headers
        self.headers = {}
        lines = header
        for line in lines:
            k, v = line.split(': ', 1)
            self.headers[k] = v
        # 清除 cookies
        self.cookies = {}
        self.add_cookies()

    def form(self):
        """
        用于存储表单数据
        """
        body = urllib.parse.unquote(self.body)
        args = body.split('&')
        f = {}
        print('form debug', args, len(args))
        for arg in args:
            k, v = arg.split('=', 1)
            f[k] = v
        return f

    def json(self):
        """
        把 body 中的 json 格式字符串解析成 dict 或者 list 并返回
        """
        import json
        return json.loads(self.body)


def error(code=404):
    """
    根据 code 返回不同的错误响应
    """
    e = {
        404: b'HTTP/1.x 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
        500: b'HTTP/1.x 500 Internal Server Error\r\n\r\n<h1>Internal Server Error</h1>',
        502: b'HTTP/1.x 502 Bad Gateway\r\n\r\n<h1>Bad Gateway</h1>',
    }
    return e.get(code, b'')


def parsed_path(path):
    """
    message=hello&user=yoo
    {
        'message': 'hello',
        'user': 'yoo',
    }
    """
    index = path.find('?')
    if index == -1:
        return path, {}
    else:
        path, query_str = path.split('?', 1)
        args = query_str.split('&')
        query = {}
        for arg in args:
            k, v = arg.split('=')
            query[k] = v
        return path, query


def response_for_path(path, request):
    path, query = parsed_path(path)
    request.path = path
    request.query = query
    r = {
        '/static': route_static,
    }
    """
    注册路由
    """
    r.update(user_routes)
    r.update(todo_routes)
    # ajax路由
    r.update(api_routes)
    r.update(ajax_routes)
    # 根据 path 调用相应的处理函数
    # 没有处理的 path 会返回 404
    response = r.get(path, error)
    return response(request)


def process_request(connection):
    r = b''
    while True:
        rq = connection.recv(1024)
        r += rq
        if len(rq) < 1024:
            break
    r = r.decode('utf-8')
    log('完整请求:')
    log('request***', r)
    log('请求结束')
    # 因为 chrome 会发送空请求导致 split 得到空 list
    # 所以这里判断一下防止程序崩溃
    if len(r.split()) < 2:
        connection.close()
    path = r.split()[1]
    # 创建一个新的 request 并设置
    request = Request()
    request.method = r.split()[0]
    request.add_headers(r.split('\r\n\r\n', 1)[0].split('\r\n')[1:])
    # 把 body 放入 request 中
    request.body = r.split('\r\n\r\n', 1)[1]
    # 用 response_for_path 函数来得到 path 对应的响应内容
    response = response_for_path(path, request)
    # 把响应发送给客户端
    connection.sendall(response)
    log('完整响应:')
    try:
        log('response***', response.decode('utf-8').replace('\r\n', '\n'))
        log('*******')
    except Exception as e:
        print('异常', e)
    # 处理完请求, 关闭连接
    connection.close()
    print('关闭')


def run(host='', port=3000):
    """
    启动服务器
    """
    # 初始化 socket 套路
    # 使用 with 可以保证程序中断的时候正确关闭 socket 释放占用的端口
    print('start at', '{}:{}'.format(host, port))
    with socket.socket() as s:
        # 绑定 主机地址 和 端口
        s.bind((host, port))
        # 监听 接受 读取请求数据 解码成字符串
        s.listen(5)
        # 无限循环来处理请求
        while True:
            connection, address = s.accept()
            print('连接成功, 使用多线程处理请求', address)
            # 开一个新的线程来处理请求, 第二个参数是传给新函数的参数列表, 必须是 tuple
            _thread.start_new_thread(process_request, (connection,))
            # process_request(connection)


if __name__ == '__main__':
    # 生成配置并且运行程序
    config = dict(
        host='',
        port=3000,
    )
    run(**config)
