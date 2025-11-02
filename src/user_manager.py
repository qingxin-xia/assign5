from __future__ import annotations

import json
from .user_profile import UserProfile
from .location import Location

class UserProfileManager:
    def __init__(self):
        self.user_profiles = {}
        
    def add_profile(self, profile: UserProfile) -> None:
        if profile.validate():
            if profile.email in self.user_profiles:
                raise ValueError(f"Profile with email {profile.email} already exists")
            self.user_profiles[profile.email] = profile
            return
        raise ValueError(f"Failed to add profile for '{profile.email}'")
    
    def get_profile(self, email: str) -> UserProfile | None:
        return self.user_profiles.get(email, None)
    
    def remove_profile(self, email: str) -> None:
        if email in self.user_profiles:
            del self.user_profiles[email]
            return
        raise ValueError(f"Failed to remove profile for '{email}'")
    
    def sort_profiles_by_age(self):
        return sorted(self.user_profiles.values(), key=lambda x: x.get_age(), reverse=True)
    
    def sort_profiles_by_name(self):
        return sorted(self.user_profiles.values(), key=lambda x: x.name)
    
    def sort_profiles_by_email(self):
        return sorted(self.user_profiles.values(), key=lambda x: x.email)
    
    def sort_profiles_by_location(self):
        return sorted(self.user_profiles.values(), key=lambda x: (x.location.country, x.location.state, x.location.city))
    
    def save_profiles_to_json(self, json_file: str):
        data = []
        for profile in self.user_profiles.values():
            data.append({
                'name': profile.name,
                'email': profile.email,
                'password': profile.password,
                'dob': profile.dob,
                'location': {
                    'city': profile.location.city,
                    'state': profile.location.state,
                    'country': profile.location.country
                }
            })
        with open(json_file, 'w') as f:
            json.dump(data, f, indent=4)
    
    def load_profiles_from_json(self, json_file: str):
        with open(json_file, 'r') as f:
            data = json.load(f)
        if isinstance(data, dict):
            profile_items = [data]
        elif isinstance(data, list):
            profile_items = data
        else:
            print(f"Error: JSON file must contain a dictionary or list")
            return
        for profile_data in profile_items:
            try:
                profile = UserProfile(
                    name=profile_data['name'],
                    email=profile_data['email'],
                    password=profile_data['password'],
                    dob=profile_data['dob'],
                    location=Location(**profile_data['location'])
                )
                try:
                    self.add_profile(profile)
                except ValueError:
                    pass
            except KeyError as e:
                print(f"Error loading profile: missing field {e}")
            except Exception as e:
                print(f"Error loading profile: {e}")