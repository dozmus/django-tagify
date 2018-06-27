import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

setup(
    name='django-tagify',
    version='0.17',
    packages=['django_tagify'],
    description='django tag input field',
    long_description=README,
    author='PureCS',
    author_email='purecs@hotmail.com',
    url='https://github.com/purecs/django-tagify/',
    license='MIT',
    install_requires=[
        'Django>=2.0.0',
    ],
    include_package_data=True,
    package_data={
        'django_tagify': [
            'templates/*.html',
            'static/js/*.js',
            'static/css/*.css',
        ]
    },
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
