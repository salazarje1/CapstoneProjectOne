# Capstone Project One

My Application uses the 'haveibeenpwned' API and allows user to checks if their passwords and email have been pwned. 

[Application Link](https://capstone-proj-one.herokuapp.com/)
[HaveIBeenPwned API](https://haveibeenpwned.com/API/v2?ref=apilist.fun)

--- 

## Project Summary

I designed this application with goal of helping online users stay safe by knowing when its time to change passwords. Having an email that has been breached or pwned is important to know and keep you safe. 

With my site you will know when its time to change an email if it will make you feel safer. At the very least you will know when it's time to change your password. When you change you password you can make sure the password is safe to use online.

---

## Function Used 

- User Account 
    - Users can create thier own private account and keep stored passwords and emails private. 
    - Users can edit and change their name, email, and passwords. 
    - User passwords hashed and salted with Bcrypt. 
    - User account can also be deleted when not needed anymore. 

- Emails
  - Each user account can store as many emails as they need. All emails are store by user id and can not be accessed by other users. 
  - Each email can be checked with the API. 
  - Email can be added and deleted. 

- Passwords 
  - Each user can add as many passwords to the users account. 
  - Each password can be check with the API. 
  - Each password is sent to the API hashed 
  - The API only allows passwords to be searched by a certain amount of characters. 
  - The API implement a [k-Anonmity](https://en.wikipedia.org/wiki/K-anonymity).

---

## User Interaction 

- A user can check email breach through the home page but will be informed if its been breached or not. 
- From the home page a user can register/login to an account. 
- Once logged in an email can be added to the account. 
  - If the email checked is breached you will get information from all the breaches your email has been in. 
  - If the email hasn't been breached you will get a safe indicator. 
- Once logged in passwords can be added to accounts also. 
  - If the passwords have been breached the website will let you know how many times its been breached. 
  - If it hasn't been breached you will get a safe indicator. 
- Users can see their account information. 
- Users can change their account information.
- User can delete their accounts. 
- User can logout from accounts. 

---

## Technoloy Stack

- Frontend
  - HTML/Jinja
  - CSS/Bootstrap 4
  - Javascript/Axios

- Backend
  - Python/Flask
  - SQLAlchemy
  - WTForms
  - PostgreSQL
  - unittest

- API
  - [HaveIBeenPwnd API](https://haveibeenpwned.com/API/v2?ref=apilist.fun)


