from setuptools import setup, find_packages

version = '0.1.0'

setup(
    name='django-teams',
    version=version,
    description=("A simple application for Django providing a hierarchical team structure."),
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python",
        "Environment :: Web Environment",
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    keywords='groups,teams,django',
    author='Matthew Scott',
    author_email='matt@11craft.com',
    url='http://github.com/11craft/django-teams/',
    license='Apache 2.0',
    packages=find_packages(),
    zip_safe=False,
    package_data = {
        'teams': [
            'media/*.css',
            'templates/*/*.html',
        ],
    }
)
