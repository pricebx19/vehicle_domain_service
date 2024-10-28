import pytest
from unittest.mock import patch, MagicMock
from api.car_query_api import CarQueryAPI


class TestCarQueryAPI:

    def setup_method(self):
        self.api = CarQueryAPI()

    # 1. Test _build_url correctly constructs the URL
    def test_build_url(self):
        url = self.api._build_url("getYears")
        expected_url = "https://www.carqueryapi.com/api/0.3/?callback=?&cmd=getYears"
        assert url == expected_url

    # 2. Test _build_url with parameters
    def test_build_url_with_params(self):
        url = self.api._build_url("getModels", year=2017, make="Ford")
        expected_url = "https://www.carqueryapi.com/api/0.3/?callback=?&cmd=getModels&year=2017&make=Ford"
        assert url == expected_url

    # 3. Test successful _make_api_call with valid response
    @patch("api.car_query_api.requests.get")
    def test_make_api_call_success(self, mock_get):
        # Simulate a successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '?({"Years": {"min_year": "2000", "max_year": "2020"}});'
        mock_get.return_value = mock_response

        url = self.api._build_url("getYears")
        response = self.api._make_api_call(url)

        # Assert that the response is cleaned and parsed correctly
        assert response == {"Years": {"min_year": "2000", "max_year": "2020"}}
        mock_get.assert_called_once_with(url, headers={'User-Agent': 'PostmanRuntime/7.39.0'})

    # 4. Test _make_api_call with an HTTP error
    @patch("api.car_query_api.requests.get")
    def test_make_api_call_http_error(self, mock_get):
        # Simulate a failed API response (500)
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = Exception("HTTP Error")
        mock_get.return_value = mock_response

        url = self.api._build_url("getYears")

        with pytest.raises(Exception, match="HTTP Error"):
            self.api._make_api_call(url)

        mock_get.assert_called_once_with(url, headers={'User-Agent': 'PostmanRuntime/7.39.0'})

    # 5. Test _make_api_call with invalid JSON response
    @patch("api.car_query_api.requests.get")
    def test_make_api_call_invalid_json(self, mock_get):
        # Simulate an API response with invalid JSON
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '?invalid_json);'
        mock_get.return_value = mock_response

        url = self.api._build_url("getYears")
        response = self.api._make_api_call(url)

        # Assert that the invalid JSON is handled gracefully
        assert response == {}
        mock_get.assert_called_once_with(url, headers={'User-Agent': 'PostmanRuntime/7.39.0'})

    # 6. Test get_years using mocked API response
    @patch("api.car_query_api.CarQueryAPI._make_api_call")
    def test_get_years(self, mock_make_api_call):
        # Simulate the return value from the API
        mock_make_api_call.return_value = {"Years": {"min_year": "2000", "max_year": "2020"}}

        response = self.api.get_years()

        assert response == {"Years": {"min_year": "2000", "max_year": "2020"}}
        mock_make_api_call.assert_called_once()

    # 7. Test get_makes using mocked API response
    @patch("api.car_query_api.CarQueryAPI._make_api_call")
    def test_get_makes(self, mock_make_api_call):
        # Simulate the return value from the API
        mock_make_api_call.return_value = {"Makes": [{"make_id": "ford", "make_display": "Ford"}]}

        response = self.api.get_makes(2017)

        assert response == {"Makes": [{"make_id": "ford", "make_display": "Ford"}]}
        mock_make_api_call.assert_called_once()

    # 8. Test get_models using mocked API response
    @patch("api.car_query_api.CarQueryAPI._make_api_call")
    def test_get_models(self, mock_make_api_call):
        # Simulate the return value from the API
        mock_make_api_call.return_value = {"Models": [{"model_id": "mustang", "model_name": "Mustang"}]}

        response = self.api.get_models(2017, "Ford")

        assert response == {"Models": [{"model_id": "mustang", "model_name": "Mustang"}]}
        mock_make_api_call.assert_called_once()

    # 9. Test get_trims using mocked API response
    @patch("api.car_query_api.CarQueryAPI._make_api_call")
    def test_get_trims(self, mock_make_api_call):
        # Simulate the return value from the API
        mock_make_api_call.return_value = {"Trims": [{"model_id": "mustang_eco", "model_trim": "EcoBoost"}]}

        response = self.api.get_trims(2017, "Ford", "Mustang")

        assert response == {"Trims": [{"model_id": "mustang_eco", "model_trim": "EcoBoost"}]}
        mock_make_api_call.assert_called_once()

    # 10. Test get_vehicle_body_style using mocked API response
    @patch("api.car_query_api.CarQueryAPI._make_api_call")
    def test_get_vehicle_body_style(self, mock_make_api_call):
        # Simulate the return value from the API
        mock_make_api_call.return_value = {"model_body": "Sedan"}

        body_style = self.api.get_vehicle_body_style(68830)

        assert body_style == "Sedan"
        mock_make_api_call.assert_called_once()
