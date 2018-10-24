from models import Model


class User(Model):
    def __init__(self, form):
        self.id = form.get('id', None)
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.role = int(form.get('role', 10))

    def is_admin(self):
        return self.role == 1

    @staticmethod
    def salted_password(pwd, salt='$!@><?>HUI&DWQa`'):
        """$!@><?>HUI&DWQa`"""
        import hashlib

        def sha256(ascii_str):
            return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()

        hash1 = sha256(pwd)
        hash2 = sha256(hash1 + salt)
        return hash2

    @staticmethod
    def hashed_password(pwd):
        import hashlib
        # 用 ascii 编码转换成 bytes 对象
        p = pwd.encode('ascii')
        s = hashlib.sha256(p)
        # 返回摘要字符串
        return s.hexdigest()

    def validate_register(self):
        pwd = self.password
        self.password = self.salted_password(pwd)

        u = User.find_by(username=self.username)
        if u is None:
            self.save()
            return self
        else:
            return None

    def validate_login(self):
        u = User.find_by(username=self.username)
        if u is not None:
            return u.password == self.salted_password(self.password)
        return False
