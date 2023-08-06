from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='famog',
    version='0.1',
    description='A package for Facts API',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='https://elian-1.gitbook.io/facts-api/',
    author='Elian Galdamez',
    author_email='elian.galdamez510@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='API',
    packages=find_packages('famog'),
    install_requires=['requests']
)