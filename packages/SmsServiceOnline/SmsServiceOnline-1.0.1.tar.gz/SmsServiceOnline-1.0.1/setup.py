from setuptools import setup

with open("readme.md") as readme:
    description = readme.read()
    readme.close()

setup(name='SmsServiceOnline',
    version='1.0.1',
    description='Package for https://sms-service-online.com',
    long_description=description,
    long_description_content_type='text/markdown',
    packages=['SmsServiceOnline'],
    install_requires=[
        'requests',
    ],
    url="https://github.com/fxcvd/SmsServiceOnline",
    author_email='rzet595@gmail.com',
    zip_safe=False
)
