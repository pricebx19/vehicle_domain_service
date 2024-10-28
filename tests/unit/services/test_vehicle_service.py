import pytest
from unittest.mock import patch, MagicMock
from domain.vehicle import Vehicle
from services.vehicle_service import VehicleService


class TestVehicleService:
    def setup_method(self):
        self.vehicle_service = VehicleService()

    # 1. Test get_years with valid response
    @patch("services.vehicle_service.CarQueryAPI.get_years")
    def test_get_years(self, mock_get_years):
        mock_get_years.return_value = {'Years': {'min_year': '2000', 'max_year': '2020'}}

        years = self.vehicle_service.get_years()

        assert years == list(range(2000, 2021))
        mock_get_years.assert_called_once()

    # 2. Test get_years with invalid response (missing keys)
    @patch("services.vehicle_service.CarQueryAPI.get_years")
    def test_get_years_invalid(self, mock_get_years):
        # API returns unexpected structure
        mock_get_years.return_value = {}

        with pytest.raises(KeyError):
            self.vehicle_service.get_years()

        mock_get_years.assert_called_once()

    # 3. Test get_makes with valid response
    @patch("services.vehicle_service.CarQueryAPI.get_makes")
    def test_get_makes(self, mock_get_makes):
        mock_get_makes.return_value = {'Makes': [{'make_id': 'ford', 'make_display': 'Ford'}]}

        makes = self.vehicle_service.get_makes(2017)

        assert makes == [{'make_id': 'ford', 'make_display': 'Ford'}]
        mock_get_makes.assert_called_once_with(2017)

    # 4. Test get_makes with invalid response (empty makes list)
    @patch("services.vehicle_service.CarQueryAPI.get_makes")
    def test_get_makes_invalid(self, mock_get_makes):
        mock_get_makes.return_value = {'Makes': []}

        makes = self.vehicle_service.get_makes(2017)

        assert makes == []
        mock_get_makes.assert_called_once_with(2017)

    # 5. Test get_models with valid response
    @patch("services.vehicle_service.CarQueryAPI.get_models")
    def test_get_models(self, mock_get_models):
        mock_get_models.return_value = {'Models': [{'model_id': 'mustang', 'model_name': 'Mustang'}]}

        models = self.vehicle_service.get_models(2017, 'Ford')

        assert models == [{'model_id': 'mustang', 'model_name': 'Mustang'}]
        mock_get_models.assert_called_once_with(2017, 'Ford')

    # 6. Test get_models with invalid response (empty models list)
    @patch("services.vehicle_service.CarQueryAPI.get_models")
    def test_get_models_invalid(self, mock_get_models):
        mock_get_models.return_value = {'Models': []}

        models = self.vehicle_service.get_models(2017, 'Ford')

        assert models == []
        mock_get_models.assert_called_once_with(2017, 'Ford')

    # 7. Test get_trims with valid response
    @patch("services.vehicle_service.CarQueryAPI.get_trims")
    def test_get_trims(self, mock_get_trims):
        mock_get_trims.return_value = {'Trims': [{'model_id': 'mustang_eco', 'model_trim': 'EcoBoost'}]}

        trims = self.vehicle_service.get_trims(2017, 'ford', 'mustang')

        assert trims == [{'model_id': 'mustang_eco', 'model_trim': 'EcoBoost'}]
        mock_get_trims.assert_called_once_with(2017, 'ford', 'mustang')

    # 8. Test get_trims with invalid response (empty trims list)
    @patch("services.vehicle_service.CarQueryAPI.get_trims")
    def test_get_trims_invalid(self, mock_get_trims):
        mock_get_trims.return_value = {'Trims': []}

        trims = self.vehicle_service.get_trims(2017, 'ford', 'mustang')

        assert trims == []
        mock_get_trims.assert_called_once_with(2017, 'ford', 'mustang')

    # 9. Test get_vehicle with valid response
    @patch("services.vehicle_service.CarQueryAPI.get_vehicle_body_style")
    @patch("services.vehicle_service.VehicleAddedEvent")
    def test_get_vehicle(self, mock_event, mock_get_vehicle_body_style):
        mock_get_vehicle_body_style.return_value = "Sedan"
        mock_event_instance = mock_event.return_value

        vehicle = self.vehicle_service.get_vehicle(2017, "Ford", "Mustang", 68830)

        assert isinstance(vehicle, Vehicle)
        assert vehicle.year == 2017
        assert vehicle.make == "Ford"
        assert vehicle.model == "Mustang"
        assert vehicle.vehicle_type == "Sedan"

        mock_event.assert_called_once_with(vehicle)
        mock_get_vehicle_body_style.assert_called_once_with(68830)
        assert mock_event_instance is not None

    # 10. Test get_vehicle with invalid model ID
    @patch("services.vehicle_service.CarQueryAPI.get_vehicle_body_style")
    def test_get_vehicle_invalid_model_id(self, mock_get_vehicle_body_style):
        # Simulate a failure for the body style lookup
        mock_get_vehicle_body_style.return_value = "Unknown"

        with pytest.raises(ValueError):
            self.vehicle_service.get_vehicle(2017, "Ford", "Mustang", 7453975397)

        mock_get_vehicle_body_style.assert_called_once_with(7453975397)

