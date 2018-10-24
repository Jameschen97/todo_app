import random

from models.user import User
from routes.session import session

from utils import (
    template,
    http_response,
    redirect,
    log,
)


def random_str():
    seed = 'abcdefghsdkqwcsbjahbsj24549edfvs2g4yguyg'
    s = ''
    for i in range(16):
        random_index = random.randint(0, len(seed) - 1)
        s += seed[random_index]
    return s


def route_login(request):
    """
    登录页面的路由函数
    """
    headers = {
        'Content-Type': 'text/html',
    }
    log('login-cookies', request.cookies)

    if request.method == 'POST':
        form = request.form()
        u = User(form)
        if u.validate_login():
            user = User.find_by(username=u.username)
            # 设置 session
            session_id = random_str()
            session[session_id] = user.id
            headers['Set-Cookie'] = 'user={}'.format(session_id)
            log('headers response', headers)
            # 登录后重定向到 /
            return redirect('/', headers)
    # 显示登录页面
    body = template('login.html')
    return http_response(body)


def route_register(request):
    """
    注册页面的路由函数
    """
    if request.method == 'POST':
        form = request.form()
        u = User(form)
        if u.validate_register() is not None:
            print('注册成功', u)
            # 注册成功后 重定向到 登录 页面
            return redirect('/login')
        else:
            # 注册失败 重定向到 注册 页面
            return redirect('/register')
    # 显示注册页面
    body = template('register.html')
    return http_response(body)


def current_user(request):
    session_id = request.cookies.get('user', '')
    user_id = session.get(session_id, -1)
    if user_id == -1:
        return -1
    return user_id


def index(request):
    uid = current_user(request)
    u = User.find_by(id=uid)
    if u is None:
        username = "请登录!"
    else:
        username = u.username
    body = template('index.html')
    body = body.replace('{{ username }}', username)
    return http_response(body)


def login_required(route_function):
    def f(request):
        uid = current_user(request)
        u = User.find_by(id=uid)
        if u is None:
            return redirect('/login')
        return route_function(request)

    return f


# 路由字典
route_dict = {
    '/': index,
    '/login': route_login,
    '/register': route_register,
}
