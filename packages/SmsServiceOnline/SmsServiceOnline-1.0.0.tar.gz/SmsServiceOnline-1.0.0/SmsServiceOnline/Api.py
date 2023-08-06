#by @fxcvd
#python 3.6^

from requests import Session


API_URL = "https://sms-service-online.com/stubs/handler_api"


class Api(object):
    def __init__(self, api_key, lang, welcome_message=True):
        self.key = api_key
        self.lang = lang
        self.session = self._create_session()

        if welcome_message:
            print("Package for -> https://sms-service-online.com\nApi docs -> https://sms-service-online.com/ru/api-sms-activate\n\nby @fxcvd\n\nset welcome_message=False for hide this message")

    def _create_session(self):
        return Session()

    def get_balance(self):
        data = self.session.request(
            method="GET",
            url=f"{API_URL}?api_key={self.key}&action=getBalance&lang={self.lang}"
        ).text

        return {"balance": data}

    def get_country_and_operators(self):
        return self.session.request(
            method="GET",
            url=f"{API_URL}?api_key={self.key}&action=getCountryAndOperators&lang={self.lang}"
        ).json()

    def get_services_and_cost(self, country, operator):
        return self.session.request(
            method="GET",
            url=f"{API_URL}?api_key={self.key}&action=getServicesAndCost&country={country}&operator={operator}&lang={self.lang}"
        ).json()

    def get_number(self, country, operator, service):
        data = self.session.request(
            method="GET",
            url=f"{API_URL}?api_key={self.key}&action=getNumber&service={service}&operator={operator}&country={country}&lang={self.lang}"
        ).text.split(":")

        return {"id": data[1], "number": data[2]}

    def set_status(self, id, status):
        data = self.session.request(
            method="GET",
            url=f"{API_URL}?api_key={self.key}&action=setStatus&id={id}&status={status}&lang={self.lang}"
        ).text

        return {"status": data}

    def get_status(self, id):
        data = self.session.request(
            method="GET",
            url=f"{API_URL}?api_key={self.key}&action=getStatus&id={id}&lang={self.lang}"
        ).text

        if ":" in data:
            return {"code": data.split(":")[1]}

        return {"status": data}