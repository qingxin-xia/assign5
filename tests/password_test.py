import pytest
import json
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parent.parent))


from src import UserProfile


# I looked at the valid passwords and noticed they all start with capital letters,
# a section of all letters, a section of all numbers, and a section with all special
# characters exactly in that order even though it's not required
class TestAgeCalculation:
   def test_valid_password(self):
       assert UserProfile.valid_password("12%Huadkfj") == True # random keyboard smashing with added requirements
       assert UserProfile.valid_password("lol9J$fad") == True
       assert UserProfile.valid_password("123$fivE") == True
       assert UserProfile.valid_password("Password23!") == True # in the password form for valid data json
       assert UserProfile.valid_password("akdshfk87*dHK") == True # lowercase in front
       assert UserProfile.valid_password("123HelloKitty!") == True # number in front
       assert UserProfile.valid_password("$$$34heLlO") == True # special character in front
       assert UserProfile.valid_password("PasswordH@123") == True # capital letter and letters first, special char, and then number
       assert UserProfile.valid_password("eighT8!!") == True # exactly 8 characters
       assert UserProfile.valid_password("***@$*&3Fd") == True # mostly special characters
       assert UserProfile.valid_password("11111!aA") == True # bare minimum requirements




   def test_invalid_password(self):
       assert UserProfile.valid_password("wE1$d") == False  # not enough characters
       assert UserProfile.valid_password("") == False  # empty string
       assert UserProfile.valid_password("hello4%what") == False  # no uppercase
       assert UserProfile.valid_password("HELLOWORLD54#") == False  # no lowercase
       assert UserProfile.valid_password("adfhk23452") == False  # no special char
       assert UserProfile.valid_password("what'sup??") == False  # no digit
       assert UserProfile.valid_password("oneTw0#") == False  # 7 characters
       assert UserProfile.valid_password("HELLOWORLD") == False  # all uppercase
       assert UserProfile.valid_password("whatareyoudoing") == False  # all lowercase
       assert UserProfile.valid_password("(^%&(*%($)))") == False  # all special char
       assert UserProfile.valid_password("12345678") == False  # all digit


if __name__ == "__main__":
   pytest.main([__file__, "-v"])