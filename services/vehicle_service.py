from domain.vehicle import Vehicle  # Imported from the VehicleDomain project
from domain.events.vehicle_added_event import VehicleAddedEvent
from api.car_query_api import CarQueryAPI

class VehicleService:

    def __init__(self):
        self.api = CarQueryAPI()  # Instantiate CarQueryAPI for external API interactions

    def get_years(self):
        response = self.api.get_years()
        min_year = int(response['Years']['min_year'])
        max_year = int(response['Years']['max_year'])
        return list(range(min_year, max_year + 1))

    def get_makes(self, year):
        response = self.api.get_makes(year)
        return [{'make_id': make['make_id'], 'make_display': make['make_display']} for make in response['Makes']]

    def get_models(self, year, make):
        response = self.api.get_models(year, make)
        return response['Models']

    def get_trims(self, year, make_id, model):
        response = self.api.get_trims(year, make_id, model)
        return [{'model_id': trim['model_id'], 'model_trim': trim['model_trim']} for trim in response['Trims']]

    def get_vehicle(self, year: int, make: str, model: str, model_id: int):
        vehicle = Vehicle(year, make, model)  # Uses Vehicle from VehicleDomain
        body_style = self.api.get_vehicle_body_style(model_id)
        vehicle.vehicle_type = body_style
        event = VehicleAddedEvent(vehicle)  # Uses event from VehicleDomain
        self._publish_event(event)
        return vehicle

    @staticmethod
    def _publish_event(event):
        print(f"Event published: {event}")
