import time
import json
# import os.path

# from jinja2 import Environment, FileSystemLoader

# __file__ 就是本文件的名字
# 得到用于加载模板的目录
# path = '{}/templates/'.format(os.path.dirname(__file__))
# # 创建一个加载器, jinja2 会从这个目录中加载模板
# loader = FileSystemLoader(path)
# # 用加载器创建一个环境, 有了它才能读取模板文件
# env = Environment(loader=loader)


# jinja2模板
# def template(name, **kwargs):
#     """
#     本函数接受一个路径和一系列参数
#     读取模板并渲染返回
#     """
#     t = env.get_template(name)
#     return t.render(**kwargs)


# 简单模板
def template(name):
    """
    根据名字读取 templates 文件夹里的一个文件并返回
    """
    path = 'templates/' + name
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def http_response(body, headers=None, status_code=200):
    """
    headers 是可选的字典格式的 HTTP 头
    """
    header = 'HTTP/1.1 {} OK\r\nContent-Type: text/html\r\n'.format(status_code)
    if headers is not None:
        header += ''.join(['{}: {}\r\n'.format(k, v)
                           for k, v in headers.items()])
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def json_response(data):
    """
    本函数返回 json 格式的 body 数据
    前端的 ajax 函数就可以用 JSON.parse 解析出格式化的数据
    """
    # 注意, content-type 现在是 application/json 而不是 text/html
    # 这个不是很要紧, 因为客户端可以忽略这个
    header = 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n'
    # json.dumps 用于把 list 或者 dict 转化为 json 格式的字符串
    # ensure_ascii=False 可以正确处理中文
    # indent=2 表示格式化缩进, 方便好看用的
    body = json.dumps(data, ensure_ascii=False, indent=2)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def redirect(location, headers=None):
    if headers is None:
        headers = {
            'Content-Type': 'text/html',
        }
    headers['Location'] = location
    # 302 为临时重定向, 将重定向的地址写入 Location
    return http_response('', headers, 302)


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


def log(*args, **kwargs):
    # time.time() 返回 unix time
    # 然后把 unix time 转换为普通人可以看懂的格式
    formats = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(formats, value)
    with open('app-log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)
