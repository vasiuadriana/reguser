import re, shortuuid

def generate_username(email):
    """
    Generates a unique Django username from the user's e-mail address 
    by appending a short uuid at the end of the username. 
    """
    leading_part_of_email = email.rsplit('@',1)[0]
    leading_part_of_email = re.sub(r'[^a-zA-Z0-9+]', '',
                                   leading_part_of_email)
    return leading_part_of_email[:7] + '.' + shortuuid.uuid()

