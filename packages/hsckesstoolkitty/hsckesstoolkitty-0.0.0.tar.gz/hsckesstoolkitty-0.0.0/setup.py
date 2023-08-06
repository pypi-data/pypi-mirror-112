from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='hsckesstoolkitty',
    version='',
    description='A toolkit for cyber security',
    long_description='',
    url='',
    author='Ian Moffett',
    author_email='teaqllabs@gmail.com',
    license='',
    classifiers=classifiers,
    keywords='toolkit',
    packages=find_packages(),
    install_requires=['requests']
)