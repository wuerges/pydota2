from distutils.core import setup

setup(
    name='pydota2',
    version='0.01',
    description='Dota2 match history python wrapper for the Steam Web API',
    url='http://github.com/jephdo/pydota2/',
    author='Jeph Do',
    author_email='jephdo@gmail.com',
    packages=[
        'dota2',
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ]
)