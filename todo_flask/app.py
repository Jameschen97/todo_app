from flask import (
    Flask,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    Blueprint,
)

from routes.todo import main as todo_routes

app = Flask(__name__)
# 设置 secret_key 来使用 flask 自带的 session
# 这个字符串随便设置什么内容都可以
app.secret_key = 'random string'

# 注册蓝图
# 用 url_prefix 来给蓝图中的每个路由加一个前缀
app.register_blueprint(todo_routes, url_prefix='/todo')

# 程序入口
if __name__ == '__main__':
    # debug 模式可以自动加载你对代码的变动, 因此不用重启程序
    # host 参数指定为 '0.0.0.0' 可以让别的机器访问你的代码
    config = dict(
        debug=False,
        host='0.0.0.0',
        port=2000,
    )
    app.run(**config)
