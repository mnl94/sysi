BLACKLISTED_CHARACTERS = {'$', '%', '@', '#', '&', '*', '!', '(', ')', '+', '=', '{', '}', '[', ']', '<', '>', ';', ':', ' '}
BLACKLISTED_CHARACTERS_MESSAGE = {'$', '%', '@', '#', '*', '{', '}', '[', ']', '<', '>', ';'}
MIN_PASSW_LEN = 4
MAX_PASSW_LEN = 60
MIN_USERNAME_LEN = 1
MAX_USERNAME_LEN = 255
VALID_CONDITIONS = {'new','used','broken'}
VALID_ROLES = {'user','admin'}
MAX_INT_MYSQL = 2147483647

def valid_username(username):
    if not isinstance(username, str):
        return False
    
    leng = len(username)
    if leng > MAX_USERNAME_LEN or leng < MIN_USERNAME_LEN:
        return False
        
    if any(char in BLACKLISTED_CHARACTERS for char in username):
        return False
            
    return True


def valid_password(password):
    if not isinstance(password, str):
        return False
    
    leng = len(password)
    if leng < MIN_PASSW_LEN or leng > MAX_PASSW_LEN:
        return False
    
    return True


def valid_role(role):
    if role in VALID_ROLES:
        return True
    return False


def valid_id(uid):
    if not isinstance(uid, int):
        return False

    if not (1 <= uid <= MAX_INT_MYSQL):
        return False
    
    return True



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
    
    if not (0 <= amount <= MAX_INT_MYSQL):
        return False
    
    return True


def valid_item_condition(condition):
    if condition in VALID_CONDITIONS:
        return True
    return False


def valid_item_price(price):
    if not isinstance(price, int):
        return False
    
    if not (0 <= price <= MAX_INT_MYSQL):
        return False
    
    return True


def valid_message(message):
    if not isinstance(message, str):
        return False
    
    if not (0 <= len(message) <= 512):
        return False
    
    if any(char in BLACKLISTED_CHARACTERS_MESSAGE for char in message):
        return False
    
    return True


def valid_supplier(supplier):
    if not isinstance(supplier, str):
        return False
    
    if not (1 <= len(supplier) <= 128):
        return False
    
    if any(char in BLACKLISTED_CHARACTERS_MESSAGE for char in supplier):
        return False

    return True
