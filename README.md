# Social Team Builder
Social Team Builder - Teamtreehouse

## Prerequisites
 - Python 3
  
## To Run
  1. Open a command-line or terminal window.
  2. `cd` into the project directory
  3. We must install the project dependencies:
     `pip install -r requirements.txt`
  
  4. Migrate
    `python manage.py migrate`
    
  5. Load Initial Data
    `python manage.py loaddata initial_data.json`
   
    
  6. Start the server
    `python manage.py runserver`
    
     or
     
    `python manage.py runserver 0.0.0.0:8000`
  7. Open browser to that address.


## Default Account Info
If you ran Step 5 from above, you should be able to use
> Note without Step 5, no skills will be loaded.
> You will have to add them manually through your profile.

Email: `admin@example.com`
Password: `p4ssw0rd`

or create your own using the SignUp Form.
