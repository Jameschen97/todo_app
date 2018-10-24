import time
from models import Model

# 针对我们的数据 TODO
# 我们要做 4 件事情
"""
C create 创建数据
R read 读取数据
U update 更新数据
D delete 删除数据

Todo.new() 来创建一个 todo
"""


class Todo(Model):
    def __init__(self, form, user_id=-1):
        self.id = form.get('id', None)
        self.task = form.get('task', '')
        self.completed = False
        # self.deleted = False
        # 和别的数据关联的方式, 用 user_id 表明拥有它的 user 实例
        self.user_id = int(form.get('user_id', user_id))
        # 添加创建和修改时间
        self.ct = form.get('created_time', None)
        self.ut = form.get('updated_time', None)
        if self.ct is None:
            self.ct = int(time.time())
            self.ut = self.ct

    def is_owner(self, id):
        return self.user_id == id

    def ct(self):
        formats = '%H:%M:%S'
        value = time.localtime(self.ct)
        dt = time.strftime(formats, value)
        return dt

    @classmethod
    def update(cls, id, form):
        t = cls.find(id)
        valid_names = [
            'task',
            'completed',
            'deleted',
        ]
        for key in form:
            # 这里只应该更新我们想要更新的东西
            if key in valid_names:
                setattr(t, key, form[key])
        # 修改更新时间
        t.ut = int(time.time())
        t.save()

    @classmethod
    def complete(cls, id, completed):
        """
        用法很方便 也可用于 deleted 字段(逻辑删除)
        Todo.complete(1, True)
        Todo.complete(2, False)
        """
        t = cls.find(id)
        t.completed = completed
        t.save()
        return t

    @classmethod
    def new(cls, form, user_id=-1):
        """
        创建并保存一个 todo 并且返回它
        Todo.new({'task': '吃饭'})
        :param form: 一个字典 包含了 todo 的数据
        :param user_id: 一个int 包含了 user_id 的数据
        :return: 创建的 todo 实例
        """
        # 下面一行相当于 t = Todo(form)
        t = cls(form, user_id)
        t.save()
        return t
