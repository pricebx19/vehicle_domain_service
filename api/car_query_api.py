import requests
import json
from urllib.parse import urlencode


class CarQueryAPI:

    def __init__(self):
        self.base_url = "https://www.carqueryapi.com/api/0.3/?callback=?"
        self.headers = {'User-Agent': 'PostmanRuntime/7.39.0'}

    def get_years(self):
        url = self._build_url("getYears")
        return self._make_api_call(url)

    def get_makes(self, year):
        url = self._build_url("getMakes", year=year)
        return self._make_api_call(url)

    def get_models(self, year, make):
        url = self._build_url("getModels", year=year, make=make)
        return self._make_api_call(url)

    def get_trims(self, year, make, model):
        url = self._build_url("getTrims", year=year, make=make, model=model)
        return self._make_api_call(url)

    def get_vehicle_body_style(self, model_id):
        url = self._build_url("getModel", model=model_id)
        return self._make_api_call(url).get("model_body", "Unknown")

    def _build_url(self, cmd, **kwargs):
        query_string = urlencode(kwargs)
        return f"{self.base_url}&cmd={cmd}&{query_string}" if query_string else f"{self.base_url}&cmd={cmd}"

    def _make_api_call(self, url):
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return self._clean_response(response)

    @staticmethod
    def _clean_response(response):
        json_str = response.text.strip('?([').rstrip(']);')
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return {}