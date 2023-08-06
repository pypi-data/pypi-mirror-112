from setuptools import setup, find_packages

setup(
    name='pdsystem',
    py_modules=['pdsystem'],
    version='1.0.0',
    description='判断系统',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    install_requires=[],    # install_requires字段可以列出依赖的包信息，用户使用pip或easy_install安装时会自动下载依赖的包
    author='神秘人',
    url='https://github.com',
    author_email='3046479366@qq.com',
    license='MIT',
    packages=find_packages(),   # 需要处理哪里packages，当然也可以手动填，例如['pip_setup', 'pip_setup.ext']
    include_package_data=False,
    zip_safe=True,
)