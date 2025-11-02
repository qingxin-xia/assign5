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
                if not re.match(regex, part):
                    return False
            return True
        return False
    
    @staticmethod
    def valid_email(email: str) -> bool:
        regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.fullmatch(regex, email) is not None
    
    @staticmethod
    def valid_password(password: str) -> bool:
        regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        return re.fullmatch(regex, password) is not None
    
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
        errors = {}
        if not self.valid_name(self.name):
            errors["name"] = ["Invalid name format"]
        if not self.valid_email(self.email):
            errors["email"] = ["Invalid email format"]
        if not self.valid_password(self.password):
            errors["password"] = ["Invalid password format"]
        if not self.valid_dob(self.dob):
            errors["dob"] = ["Invalid date of birth format"]
        if not self.valid_location(self.location):
            errors["location"] = ["Invalid location format"]
        if errors:
            print(f"Validation failed for {', '.join(errors.keys())}")
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
        dob_date = self.extract_date(self.dob)
        age = reference_date.year - dob_date.year
        if reference_date.month < dob_date.month or (reference_date.month == dob_date.month and reference_date.day < dob_date.day):
            age -= 1
        return age
    
    @classmethod
    def from_json(cls, json_file: str) -> 'UserProfile':
        with open(json_file, 'r') as f:
            data = json.load(f)
        return cls(
            name=data['name'],
            email=data['email'],
            password=data['password'],
            dob=data['dob'],
            location=Location(**data['location'])
        )
        
    def to_json(self, json_file: str) -> None:
        data = {
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
        with open(json_file, 'w') as f:
            json.dump(data, f, indent=4)    
            
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