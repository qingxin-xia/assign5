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
        return sorted(self.user_profiles.values(), key=lambda p: p.get_age(), reverse=True)
    
    def sort_profiles_by_name(self):
        return sorted(self.user_profiles.values(), key=lambda p: p.name)
    
    def sort_profiles_by_email(self):
        return sorted(self.user_profiles.values(), key=lambda p: p.email)
    
    def sort_profiles_by_location(self):
        return sorted(self.user_profiles.values(), key=lambda p: (p.location.country, p.location.state, p.location.city))
    
    def save_profiles_to_json(self, json_file: str):
        profile_list = []
        for user_profile in self.user_profiles.values():
            profile_list.append({
                'name': user_profile.name,
                'email': user_profile.email,
                'password': user_profile.password,
                'dob': user_profile.dob,
                'location': {
                    'city': user_profile.location.city,
                    'state': user_profile.location.state,
                    'country': user_profile.location.country
                }
            })
        with open(json_file, 'w') as f:
            json.dump(profile_list, f, indent=4)
    
    def load_profiles_from_json(self, json_file: str):
        with open(json_file, 'r') as f:
            json_data = json.load(f)
        if isinstance(json_data, dict):
            profile_items = [json_data]
        elif isinstance(json_data, list):
            profile_items = json_data
        else:
            print(f"ERROR: JSON file must contain a dictionary or list")
            return
        for item_data in profile_items:
            try:
                user_profile = UserProfile(
                    name=item_data['name'],
                    email=item_data['email'],
                    password=item_data['password'],
                    dob=item_data['dob'],
                    location=Location(**item_data['location'])
                )
                try:
                    self.add_profile(user_profile)
                except ValueError:
                    pass
            except KeyError as e:
                print(f"error loading profile: missing field {e}")
            except Exception as e:
                print(f"error loading profile: {e}")