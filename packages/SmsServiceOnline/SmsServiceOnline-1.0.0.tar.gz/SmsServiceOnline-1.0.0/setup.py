from os import system
from setuptools import setup
from setuptools.command.install import install


setup(name='SmsServiceOnline',
    version='1.0.0',
    description='Package for https://sms-service-online.com',
    long_description='```pip3 install SmsServiceOnline```',
    long_description_content_type='text/markdown',
    packages=['SmsServiceOnline'],
    author_email='rzet595@gmail.com',
    zip_safe=False
)
