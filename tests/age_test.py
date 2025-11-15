import pytest
import json
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parent.parent))


from src import UserProfile


class TestAgeCalculation:
   def test_valid_dob(self):
       assert UserProfile.valid_dob("10/10/2006") == True # valid date form mdy
       assert UserProfile.valid_dob("2006-10-15") == True # valid date form ymd


       assert UserProfile.valid_dob("0000-10-15") == False # ymd bad year
       assert UserProfile.valid_dob("2024-13-15") == False # ymd bad month
       assert UserProfile.valid_dob("2024-00-15") == False # ymd bad month 2
       assert UserProfile.valid_dob("2024-01-00") == False # ymd bad day
       assert UserProfile.valid_dob("2024-10-32") == False # ymd bad day 2


       assert UserProfile.valid_dob("10/10/0000") == False # mdy bad year
       assert UserProfile.valid_dob("13/10/2006") == False # mdy bad month
       assert UserProfile.valid_dob("00/10/2006") == False # mdy bad month 2
       assert UserProfile.valid_dob("10/00/2006") == False # mdy bad day
       assert UserProfile.valid_dob("10/32/2006") == False # mdy bad day 2


   def test_correct_age(self):
       user = UserProfile(name="Qingxin Xia", email="qingxinxia@ucla.edu", password="Password123!",
       dob="10/10/2006",
       location={
           "city": "LosAngeles",
           "state": "CA",
           "country": "US"
       })
       assert user.get_age() == 19 # no reason to assume this would fail


       user = UserProfile(name="Qingxin Xia", email="qingxinxia@ucla.edu", password="Password123!",
       dob="10/20/2026",
       location={
           "city": "LosAngeles",
           "state": "CA",
           "country": "US"
       })
       assert user.get_age() == -1 # future date


       user = UserProfile(name="Qingxin Xia", email="qingxinxia@ucla.edu", password="Password123!",
       dob="11/12/2025",
       location={
           "city": "LosAngeles",
           "state": "CA",
           "country": "US"
       })
       #assert user.get_age() == 0 # yesterday's date (same month)


       # same tests but with alternate date format
       user = UserProfile(name="Qingxin Xia", email="qingxinxia@ucla.edu", password="Password123!",
       dob="2006-10-10",
       location={
           "city": "LosAngeles",
           "state": "CA",
           "country": "US"
       })
       assert user.get_age() == 19 # no reason to assume this would fail


       user = UserProfile(name="Qingxin Xia", email="qingxinxia@ucla.edu", password="Password123!",
       dob="2026-10-20",
       location={
           "city": "LosAngeles",
           "state": "CA",
           "country": "US"
       })
       assert user.get_age() == -1 # future date


       user = UserProfile(name="Qingxin Xia", email="qingxinxia@ucla.edu", password="Password123!",
       dob="2025-11-12",
       location={
           "city": "LosAngeles",
           "state": "CA",
           "country": "US"
       })
       assert user.get_age() == 0 # yesterday's date (same month)
  
if __name__ == "__main__":
   pytest.main([__file__, "-v"])