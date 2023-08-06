from setuptools import setup

description = """
# SmsServiceOnline 
`pip3 install SmsServiceOnline==1.0.1`

## Example #1
```python
import SmsServiceOnline

KEY = "<api key here>"
LANG = "ru"
MESSAGE = False


api = SmsServiceOnline.Api(
    api_key=KEY,
    lang=LANG,
    welcome_message=MESSAGE,
)

api.get_balance()
```
```python
>>> 10.2
```

### all methods -> [here](https://sms-service-online.com/ru/api-sms-activate/)  

---
```by @fxcvd with ❤```
"""

setup(name='SmsServiceOnline',
    version='1.0.2',
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
