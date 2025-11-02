from __future__ import annotations

import json
import re
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
        """Validate that name has 2-3 parts, each starting with uppercase letter.
        
        Args:
            name: The name string to validate
            
        Returns:
            True if name is valid, False otherwise
        """
        name_parts = name.strip().split()
        if 2 <= len(name_parts) <= 3:
            for name_part in name_parts:
                name_pattern = r"^[A-Z][a-z]*$"
                if re.fullmatch(name_pattern, name_part) is None:
                    return False
            return True
        return False
    
    @staticmethod
    def valid_email(email: str) -> bool:
        """Validate email format using regex pattern.
        
        Args:
            email: The email string to validate
            
        Returns:
            True if email format is valid, False otherwise
        """
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(email_pattern, email) is not None
    
    @staticmethod
    def valid_password(password: str) -> bool:
        """Validate password meets security requirements.
        
        Password must contain: uppercase, lowercase, digit, special char, min 8 chars.
        
        Args:
            password: The password string to validate
            
        Returns:
            True if password meets requirements, False otherwise
        """
        regex = r'^(?=^[A-Z])(?=.*[a-z]?)(?=.*\d)(?=.*[@$!%*?&])[A-z\d@$!%*?&]{8,}$'
        return re.match(regex, password) is not None
    
    @staticmethod
    def valid_dob(dob: str) -> bool:
        """Validate date of birth format (YYYY-MM-DD or MM/DD/YYYY).
        
        Args:
            dob: The date of birth string to validate
            
        Returns:
            True if date format is valid, False otherwise
        """
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

    # Validate all profile fields
    def validate(self) -> bool:
        validation_errors = {}
        # Check date of birth validity
        if not self.valid_dob(self.dob):
            validation_errors["dob"] = ["Invalid date of birth format"]
        # Check location validity
        if not self.valid_location(self.location):
            validation_errors["location"] = ["Invalid location format"]
        # Check name validity
        if not self.valid_name(self.name):
            validation_errors["name"] = ["Invalid name format"]
        # Check email validity
        if not self.valid_email(self.email):
            validation_errors["email"] = ["Invalid email format"]
        # Check password validity
        if not self.valid_password(self.password):
            validation_errors["password"] = ["Invalid password format"]
        if validation_errors:
            print(f"validation failed for {', '.join(validation_errors.keys())}")
            return False
        return True

    # Extract date from string in multiple formats
    def extract_date(self, date_str: str) -> datetime:
        # Try YYYY-MM-DD format first
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            # Try MM/DD/YYYY format
            try:
                return datetime.strptime(date_str, "%m/%d/%Y")
            except ValueError:
                raise ValueError(f"Invalid date format: {date_str}")

    def get_age(self, reference_date: datetime | None = None) -> int:
        if reference_date is None:
            reference_date = datetime.today()
        dob_date = self.extract_date(self.dob)
        age_result = reference_date.year - dob_date.year
        if reference_date.month < dob_date.month or (reference_date.month == dob_date.month and reference_date.day < dob_date.day):
            age_result -= 1
        return age_result
    
    @classmethod
    def from_json(cls, json_file: str) -> 'UserProfile':
        with open(json_file, mode='r') as file_handle:
            json_content = json.load(file_handle)
        return cls(
            name=json_content["name"],
            email=json_content["email"],
            password=json_content["password"],
            dob=json_content["dob"],
            location=Location(**json_content["location"])
        )
        
    def to_json(self, json_file: str) -> None:
        with open(json_file, mode='w') as output_file:
            json.dump(self.to_dict(), output_file, indent=4)

    def to_dict(self) -> dict:
        profile_dict = {
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "dob": self.dob,
            "location": {
                "city": self.location.city,
                "state": self.location.state,
                "country": self.location.country
            }
        }
        return profile_dict