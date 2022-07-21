import requests

API_KEY = os.environ.get('API_KEY')


# Home Page

def simple_check(email):
    return requests.get(f'https://haveibeenpwned.com/api/v3/breachedaccount/{email}',
        headers={
            'hibp-api-key': API_KEY
        }
    )


# User Email Page

def email_check(email):
    resp = requests.get(f'https://haveibeenpwned.com/api/v3/breachedaccount/{email}', 
        params={
            'truncateResponse':'false'
        },
        headers={
            'hibp-api-key':API_KEY
        }
    )
    if resp.status_code == 200:
        data = resp.json()
    else:
        data = 'safe'

    return [data, resp.status_code]

# Password Checks
def password_check(first, second):
    resp = requests.get(f'https://api.pwnedpasswords.com/range/{first}')

    data = resp.text
    data = data.splitlines()

    for d in data: 
        [hash, count] = d.split(':')
        if str(second) == hash: 
            return count

    return False