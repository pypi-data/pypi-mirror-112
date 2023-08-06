from setuptools import setup, find_packages

setup(
    name="YXKJapi",
    version="0.0.2",
    author="bmd",
    author_email="1790523836@qq.com",
    description="遥相科技api测试产品",
    python_requires=">=3.6",
    package_dir={'': 'src'},
    packages=find_packages('src')
)


