BLACKLISTED_CHARACTERS = {'$', '%', '@', '#', '&', '*', '!', '(', ')', '+', '=', '{', '}', '[', ']', '<', '>', ';', ':', ' '}
VALID_CONDITIONS = {'new','used','broken'}
VALID_ROLES = {'user','admin'}

def valid_username(username):
    if not isinstance(username, str):
        return False
        
    if len(username) > 255:
        return False
        
    if any(char in BLACKLISTED_CHARACTERS for char in username):
        return False
            
    return True


def valid_password(password):
    if not isinstance(password, str):
        return False
        
    if len(password) < 4:
        return False
    
    return True


def valid_role(role):
    if role in VALID_ROLES:
        return True
    return False


def valid_id(uid):
    if not isinstance(uid, int):
        return False

    if not (1 <= uid <= 2147483647):
        return True
    
    return False



def valid_item_name(item_name):
    if not isinstance(item_name, str):
        return False
    
    if not (1 <= len(item_name) <= 128):
        return False
    
    if any(char in BLACKLISTED_CHARACTERS for char in item_name):
        return False
    
    return True


def valid_item_amount(amount):
    if not isinstance(amount, int):
        return False
    
    # maximum value of signed int in mysql is 2147483647
    if not (0 <= amount <= 2147483647):
        return False
    
    return True


def valid_item_condition(condition):
    if condition in VALID_CONDITIONS:
        return True
    return False
