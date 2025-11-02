import re
class Location:
    def __init__(self, city: str, state: str, country: str):
        self.city = city
        self.state = state
        self.country = country
        
    def valid_location(self) -> bool:
        regex = r"^(?P<city>[a-zA-Z]+), (?P<state>[A-Z]{2}), (?P<country>[A-Z]{2})$"
        self.location = f"{self.city}, {self.state}, {self.country}"
        return re.match(regex, self.location) is not None