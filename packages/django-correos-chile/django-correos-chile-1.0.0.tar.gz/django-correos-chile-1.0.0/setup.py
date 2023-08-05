import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

setup(
    name='django-correos-chile',
    version='1.0.0',
    packages=['correos_chile'],
    description='Django Correos Chile Integration',
    long_description=README,
    long_description_content_type="text/markdown",
    author='Linets Development Team',
    author_email='dteam@linets.cl',
    url='https://gitlab.com/linets/ecommerce/oms/integrations/oms-correos-chile/',
    license='MIT',
    python_requires=">=3.7",
    install_requires=[
        'Django>=3',
        'zeep>=4.0.0'
    ]
)
