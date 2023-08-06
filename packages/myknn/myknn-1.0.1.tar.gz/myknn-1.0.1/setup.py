from setuptools import setup

setup(
    name='myknn',# 需要打包的名字,即本模块要发布的名字
    version='v1.0.1',#版本
    description='A  module  myself knn', # 简要描述
    py_modules=['myknn'],   #  需要打包的模块
    author='xiaoli', # 作者名
    author_email='ljl_python@163.com',   # 作者邮件
    url='https://github.com/lijiulin163LJL/myknn.git', # 项目地址,一般是代码托管的网站
    requires=["numpy",'math','collections'], # 依赖包,如果没有,可以不要
    license='MIT'
)