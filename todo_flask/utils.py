from jinja2 import Environment, FileSystemLoader
import os.path
import time
import json


def log(*args, **kwargs):
    # time.time() 返回 unix time
    formats = '%H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(formats, value)
    with open('app-log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)
