import json


def save(data, path):
    """
    data 是 dict 或者 list
    path 是保存文件的路径
    """
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        f.write(s)


def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        return json.loads(s)


# Model 是一个 ORM（object relation mapper）
# 好处就是不需要关心存储数据的细节，直接使用即可
class Model(object):
    """
    Model 是所有 model 的基类
    """

    @classmethod
    def db_path(cls):
        class_name = cls.__name__
        path = 'data/{}.txt'.format(class_name)
        return path

    @classmethod
    def new(cls, form):
        """
        创建并保存一个 model 并且返回它
            比如对于 Todo 而言,创建的方式如下
            Todo.new({'title': '吃饭'})
        C create
        """
        m = cls(form)
        m.save()
        return m

    @classmethod
    def _new_from_dict(cls, d):
        # 因为子元素的 __init__ 需要一个 form 参数
        # 所以这个给一个空字典
        m = cls({})
        for k, v in d.items():
            # setattr 是一个特殊的函数
            # 假设 k v 分别是 'name'  'yoo'
            # 它相当于 m.name = 'yoo'
            setattr(m, k, v)
        return m

    @classmethod
    def all(cls):
        """
        all 方法使用 load 函数得到所有的 models
        R read
        """
        path = cls.db_path()
        models = load(path)
        # 这里用了列表推导生成一个包含所有 实例 的 list
        # 因为这里是从 存储的数据文件 中加载所有的数据
        # 所以用 _new_from_dict 这个特殊的函数来初始化一个数据
        ms = [cls._new_from_dict(m) for m in models]
        return ms

    @classmethod
    def find_all(cls, **kwargs):
        """
        kwargs 是只有一个元素的 dict
        找到 所有 与关键字相符的model,用法如下
        u = User.find_all(username='yoo')
        """
        ms = []
        k, v = '', ''
        for key, value in kwargs.items():
            k, v = key, value
        models = cls.all()
        for m in models:
            # 也可以用 getattr(m, k) 取值
            if v == m.__dict__[k]:
                ms.append(m)
        return ms

    @classmethod
    def find_by(cls, **kwargs):
        """
        kwargs 是只有一个元素的 dict
        找到 一个 与关键字相符的model,用法如下
        u = User.find_by(username='yoo')
        """
        k, v = '', ''
        for key, value in kwargs.items():
            k, v = key, value
        models = cls.all()
        for m in models:
            # 也可以用 getattr(m, k) 取值
            if v == m.__dict__[k]:
                return m
        return None

    @classmethod
    def find(cls, id):
        return cls.find_by(id=id)

    @classmethod
    def delete(cls, id):
        """
        D delete
        """
        models = cls.all()
        index = -1
        for i, e in enumerate(models):
            if e.id == id:
                index = i
                break
        # 判断是否找到了这个 id 的数据
        if index == -1:
            # 没找到
            pass
        else:
            # 找到了 删除这个数据
            obj = models.pop(index)
            # 然后将剩下的数据保存
            li = [m.__dict__ for m in models]
            path = cls.db_path()
            save(li, path)
            # 返回被删除的元素
            return obj

    def __repr__(self):
        class_name = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} \n>\n'.format(class_name, s)

    def json(self):
        """
        返回当前 model 的字典表示
        """
        # copy 会复制一份新数据并返回
        d = self.__dict__.copy()
        return d

    def save(self):
        """
        用 all 方法读取文件中的所有 model 并生成一个 list
        把 self 添加进去并且保存进文件
        """
        models = self.all()
        if self.id is None:
            # 设置 self.id
            # 先看看是否是空 list
            if len(models) == 0:
                # 我们让第一个元素的 id 为 1（当然也可以为 0）
                self.id = 1
            else:
                m = models[-1]
                self.id = m.id + 1
            models.append(self)
        else:
            index = -1
            for i, m in enumerate(models):
                if m.id == self.id:
                    index = i
                    break
            models[index] = self
        li = [m.__dict__ for m in models]
        path = self.db_path()
        save(li, path)
