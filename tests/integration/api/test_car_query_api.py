import pytest
import requests
from api.car_query_api import CarQueryAPI


class TestCarQueryAPI:

    def setup_method(self):
        self.api = CarQueryAPI()

    def test_get_years_valid(self):
        # Test fetching valid years from the CarQueryAPI
        response = self.api.get_years()

        assert "Years" in response
        assert int(response["Years"]["min_year"]) > 1900
        assert int(response["Years"]["max_year"]) >= int(response["Years"]["min_year"])

    def test_get_makes_valid(self):
        # Test fetching valid makes for a specific year
        response = self.api.get_makes(2017)

        assert "Makes" in response
        assert len(response["Makes"]) > 0  # Ensure that we get at least one make
        assert "make_id" in response["Makes"][0]
        assert "make_display" in response["Makes"][0]

    def test_get_models_valid(self):
        # Test fetching valid models for a specific make and year
        response = self.api.get_models(2017, "Ford")

        assert "Models" in response
        assert len(response["Models"]) > 0  # Ensure that we get at least one model
        assert "model_make_id" in response["Models"][0]
        assert "model_name" in response["Models"][0]

    def test_get_trims_valid(self):
        # Test fetching valid trims for a specific make, model, and year
        response = self.api.get_trims(2017, "Ford", "Mustang")

        assert "Trims" in response
        assert len(response["Trims"]) > 0  # Ensure that we get at least one trim
        assert "model_id" in response["Trims"][0]
        assert "model_trim" in response["Trims"][0]

    def test_get_vehicle_body_style_valid(self):
        # Test fetching vehicle body style for a valid model_id
        body_style = self.api.get_vehicle_body_style(68830)  # Replace with a valid model_id if necessary
        assert body_style is not None
        assert isinstance(body_style, str)

    def test_get_years_invalid_url(self):
        # Test with an invalid URL (we can monkeypatch _build_url to return an invalid one)
        with pytest.raises(requests.exceptions.ConnectionError):
            self.api._build_url = lambda *args, **kwargs: "https://invalid-url.com"
            self.api.get_years()

    def test_get_vehicle_body_style_unknown(self):
        body_style = self.api.get_vehicle_body_style(999999999999)
        assert body_style == "Unknown"
