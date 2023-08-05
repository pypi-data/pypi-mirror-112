from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'Programming Language :: Python'
]

setup(
    name='basic_lib',
    version='0.0.1',
    description='A simple library for python',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    author='JeysDv',
    author_email='Jeys.Dev.contact@gmail.com',
    url='',
    license='MIT',
    classifiers = classifiers,
    packages=find_packages(),
    install_requires=['']
)