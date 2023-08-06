# @Time     : 2021/5/26
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from scripts.build import build_package, requires

name = "f1z1_async_emitter"
version = "0.0.5"
emitter_requires = requires + [
    "f1z1-async-runner>=0.0.6"
]

if __name__ == '__main__':
    build_package(name, version, filename="README.md", install_requires=emitter_requires)
