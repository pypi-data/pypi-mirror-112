import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

setup(
    name='django-bluexpress',
    version='1.0.0',
    packages=['bluexpress'],
    description='Django Bluexpress Integration',
    long_description=README,
    long_description_content_type="text/markdown",
    author='Linets Development Team',
    author_email='dteam@linets.cl',
    url='https://gitlab.com/linets/ecommerce/oms/integrations/oms-bluexpress/',
    license='MIT',
    python_requires=">=3.7",
    install_requires=[
        'Django>=3',
        'zeep>=4.0.0',
        'xmltodict==0.12.0'
    ]
)
