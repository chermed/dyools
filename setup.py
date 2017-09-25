from setuptools import setup
import os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

version = '0.2.1'

setup(
    name='dyools',
    version=version,
    description="dyools",
    long_description=README,
    classifiers=[],
    keywords='dyools',
    author='me',
    author_email='me@example.org',
    url='https://example.org',
    license='LGPL v3',
    zip_safe=True,
    py_modules=['dyools'],
    include_package_data=True,
    package_dir={},
    install_requires=[
        'click',
    ],

)
