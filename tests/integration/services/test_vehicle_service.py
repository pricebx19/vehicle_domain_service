import pytest
from domain.vehicle import Vehicle

from services.vehicle_service import VehicleService


class TestVehicleService:
    def setup_method(self):
        self.vehicle_service = VehicleService()

    def test_get_vehicle_valid(self):
        vehicle = self.vehicle_service.get_vehicle(2017, "Ford", "Mustang", 68830)

        assert isinstance(vehicle, Vehicle)
        assert vehicle.year == 2017
        assert vehicle.make == "Ford"
        assert vehicle.model == "Mustang"
        assert vehicle.vehicle_type == "Subcompact Cars"
        assert vehicle.size == "small"

    def test_get_vehicle_invalid(self):
        with pytest.raises(ValueError):
            self.vehicle_service.get_vehicle(2017, "Ford", "Mustang", 7453975397)
