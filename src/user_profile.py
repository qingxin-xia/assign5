from __future__ import annotations

import re
import json
from datetime import datetime
from .location import Location

class UserProfile:
    def __init__(self, name: str, email: str, password: str, dob: str, location: Location):
        self.name = name
        self.email = email
        self.password = password
        self.dob = dob
        self.location = location
        
    @staticmethod
    def valid_name(name: str) -> bool:
        parts = name.strip().split()
        if 2 <= len(parts) <= 3:
            for part in parts:
                regex = r"^[A-Z][a-z]*$"
                if re.fullmatch(regex, part) is None:
                    return False
            return True
        return False
    
    @staticmethod
    def valid_email(email: str) -> bool:
        regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(regex, email) is not None
    
    @staticmethod
    def valid_password(password: str) -> bool:
        regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        return re.match(regex, password) is not None
    
    @staticmethod
    def valid_dob(dob: str) -> bool:
        try:
            datetime.strptime(dob, "%Y-%m-%d")
            return True
        except ValueError:
            try:
                datetime.strptime(dob, "%m/%d/%Y")
                return True
            except ValueError:
                return False
            
    @staticmethod
    def valid_location(location: Location) -> bool:
        return location.valid_location()

    def validate(self) -> bool:
        validation_errors = {}
        if not self.valid_name(self.name):
            validation_errors["name"] = ["Invalid name format"]
        if not self.valid_email(self.email):
            validation_errors["email"] = ["Invalid email format"]
        if not self.valid_password(self.password):
            validation_errors["password"] = ["Invalid password format"]
        if not self.valid_dob(self.dob):
            validation_errors["dob"] = ["Invalid date of birth format"]
        if not self.valid_location(self.location):
            validation_errors["location"] = ["Invalid location format"]
        if validation_errors:
            print(f"validation failed for {', '.join(validation_errors.keys())}")
            return False
        return True
    
    def extract_date(self, date_str: str) -> datetime:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            try:
                return datetime.strptime(date_str, "%m/%d/%Y")
            except ValueError:
                raise ValueError(f"Invalid date format: {date_str}")
    
    def get_age(self, reference_date: datetime | None = None) -> int:
        if reference_date is None:
            reference_date = datetime.today()
        birth_date = self.extract_date(self.dob)
        calculated_age = reference_date.year - birth_date.year
        if reference_date.month < birth_date.month or (reference_date.month == birth_date.month and reference_date.day < birth_date.day):
            calculated_age -= 1
        return calculated_age
    
    @classmethod
    def from_json(cls, json_file: str) -> 'UserProfile':
        with open(json_file, 'r') as f:
            file_data = json.load(f)
        return cls(
            name=file_data['name'],
            email=file_data['email'],
            password=file_data['password'],
            dob=file_data['dob'],
            location=Location(**file_data['location'])
        )
        
    def to_json(self, json_file: str) -> None:
        with open(json_file, 'w') as f:
            json.dump(self.to_dict(), f, indent=4)

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'dob': self.dob,
            'location': {
                'city': self.location.city,
                'state': self.location.state,
                'country': self.location.country
            }
        }