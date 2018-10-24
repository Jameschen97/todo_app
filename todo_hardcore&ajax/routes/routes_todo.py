from routes.routes_user import (
    current_user,
    login_required,
)
from utils import (
    template,
    http_response,
    redirect,
)
from models.todo import Todo
from models.user import User


def index(request):
    """
    todo 首页 的路由函数
    """
    # 找到当前登录的用户, 如果没登录, 就 redirect 到 /login
    uid = current_user(request)
    todo_list = Todo.find_all(user_id=uid)
    todo_html = ''
    if todo_list is not None:
        # 下面生成一个 html 字符串
        todos = []
        for t in todo_list:
            edit_link = '<a href="/todo/edit?id={}">编辑</a>'.format(t.id)
            delete_link = '<a href="/todo/delete?id={}">删除</a>'.format(t.id)
            s = '<h3>{} : {} {} {}</h3>'.format(t.id, t.task, edit_link, delete_link)
            todos.append(s)
        todo_html = ''.join(todos)
    # 替换模板文件中的标记字符串
    body = template('todo_index.html')
    body = body.replace('{{ todos }}', todo_html)
    return http_response(body)


def add(request):
    """
    接受浏览器发过来的 添加todo 请求
    添加数据并发一个 302 定向给浏览器
    浏览器就会去请求 /todo 从而回到主页
    """
    # 得到浏览器发送的表单
    form = request.form()
    uid = current_user(request)
    # 创建一个 todo
    Todo.new(form, uid)
    # 让浏览器刷新页面到主页去
    return redirect('/todo')


def edit(request):
    """
    todo edit 的路由函数
    """
    # 得到当前编辑的 todo的 id
    todo_id = int(request.query.get('id', -1))
    t = Todo.find_by(id=todo_id)

    uid = current_user(request)
    u = User.find_by(id=uid)
    # 验证用户id是否相同
    if t.user_id != u.id:
        return redirect('/login')
    # 替换模板文件中的标记字符串
    body = template('todo_edit.html')
    body = body.replace('{{ todo_id }}', str(t.id))
    body = body.replace('{{ todo_task }}', str(t.task))
    return http_response(body)


def update(request):
    """
    todo update 的路由函数
    """
    if request.method == 'POST':
        # 修改并保存 todo
        form = request.form()
        todo_id = int(form.get('id', -1))
        t = Todo.find_by(id=todo_id)
        t.task = form.get('task', t.task)
        t.save()
    # 浏览器发送数据过来被处理后, 重定向到首页
    # 浏览器在请求新首页的时候, 就能看到新增的数据了
    return redirect('/todo')


def delete_todo(request):
    """
    todo delete 的路由函数
    """
    # 得到当前编辑的 todo的 id
    todo_id = int(request.query.get('id', -1))
    t = Todo.find_by(id=todo_id)

    uid = current_user(request)
    u = User.find_by(id=uid)
    # 验证用户id是否相同
    if t.user_id != u.id:
        return redirect('/login')

    if t is not None:
        # 删除 todo
        t.remove()
    return redirect('/todo')


# 路由字典
route_dict = {
    # GET 请求, 显示页面
    '/todo': login_required(index),
    '/todo/edit': login_required(edit),
    # POST 请求, 处理数据
    '/todo/add': login_required(add),
    '/todo/update': login_required(update),
    '/todo/delete': login_required(delete_todo),

}
