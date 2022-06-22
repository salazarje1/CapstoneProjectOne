# Capstone Project One

---

## API 

I will be using the "Have I Been Pwned" API 

[HaveIBeenPwned API Link](https://haveibeenpwned.com/API/v2?ref=apilist.fun)


---

## Project Proposal 

1. What goal will your website be designed to achieve? 
   Anyone worried about there email and password can get on and check if they need to make a change to their accounts

2. What kind of users will visit your site? In other words, what is the demographic of your users?
   I think my website can be used by anybody. Everybody has a reason to keep their account safe and secure. 

3. What data do you plan on using? You may have not picked your actual API yet, which is fine, just outline what kind of data you would like it to contain.
   The data that I will be using from the API will mainly be account information from data breaches. 

4. In brief, outline your approach to creating your project (knowing that you may not know everything in advance and that these details might change later). Answer questions like the ones below, but feel free to add more information:
    - What does your database schema look like?
        My database schema will be two different tables, users tables, and an emails table.
            - The users table will have all the account information to login and use the site. 
            - the emails table will have a relation with a user account, will store all the emails a user wants to check against the API.
            
    - What kinds of issues might you run into with your API?
        The limit on API calls that are allowed

    - Is there any sensitive information you need to secure?
        I think that most of the information used on the website will need to be secure 
    
    - What functionality will your app include?
        Login to an account and hold a certain amount of emails and check them with a click of a button see if they been in a breach.
        Have a password generator for login users that can be used as a good password. 

    - What will the user flow look like?
        From the main site you will be able to check an email for breach information. 
        You'll be able to login or register. 
        Once logged in you'll be able to use the other features. 

    - What features make your site more than CRUD? Do you have any stretch goals?
        Being able to store and check emails will be extra
        and the password generator.
