from hashlib import sha1


# Password Check Helper Functions 

def password_setup(password):
    passwd = password.password.encode()
    hashed_pass_obj = sha1(passwd)
    hashed_pass = hashed_pass_obj.hexdigest()

    first_part = hashed_pass[:5]
    second_part = hashed_pass[5:].upper()

    return [first_part, second_part]