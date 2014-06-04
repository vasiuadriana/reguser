from random import randint, choice
import re

def generate_username(email):
    """
    A simple way of generating a unique Django username from the 
    user's e-mail address, with a very low probability of collision. 
    
    >>> generate_username("abc@gmail.com")
    abcabcc933
    >>> generate_username("hey.what.is.up@hotmail.com")
    heysupa.6851
    """
    leading_part_of_email = email.rsplit('@',1)[0]
    leading_part_of_email = re.sub(r'[^a-zA-Z0-9+]', '',
                                   leading_part_of_email)
    truncated_part_of_email = leading_part_of_email[:3] \
                              + leading_part_of_email[-3:]
    salt = choice(leading_part_of_email)
    salt += choice(['', '-', '_', '.', '+']) 
    salt += str(randint(1, 99999))
    return truncated_part_of_email + salt

