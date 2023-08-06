Envvars
=======

Helper function to read the environment variables in the development machine and on the production machine (only for heroku.com)

What is the purpose of this library
-----------------------------------

This Library will help you read the environment variables needed to run your software

- An example of the environment variables would be:
    - database_login = datamaster
    - database_password = asdlf@#$kkLK!@)("")
    - DATABASE_URL = postgres://dsdsfd:asdfasgsdfgjjkdty.compute-1.amazonaws.com:532/jj4566ls

You are likely to have the variable stored differently in your development and production environment:

- In your development/local machine:
    - these files are stored in a local text file (usually called .env)
    - your code will open the file, parse the text and read the variable
- If your production environment is heroku.com
    - you can get the variables by `os.environ()`

As you can see, the code to read the env variable is different in the development machine and the production machine

Envars a function that will read it transparently from the development or production machine using the same code


How to use this library
-----------------------

Usage::

    import envars.envars as envars
    e_dct = envars.getenvars()

The environment variables are now in e_dct. Assuming you are running on a local machine and have a .env file that looks like this::

    a=1
    b=2

You can look at the values in e_dct::

    >> print e_dct
    defaultdict(<function <lambda> at 0x10cddbd70>, {'a': '1', 'b': '1'})

    >> print e_dct['a'] 
    '1'

If you are on the production machine at heroku.com, make sure you have the following variable in the heroku environment::

    ENV_NOW=production

Envars uses this as a sign that you are on the production environment and will read it correctly. Now, on the production environment, you code will do the following::

    >> print e_dct
    defaultdict(<function <lambda> at 0x10cddbd70>, {"ENV_NOW":"production", 'a': '1', 'b': '1'})

    >> print e_dct['a'] 
    '1'

    >> print e_dct['ENV_NOW'] 
    'production'



Limitations of this library
---------------------------

Designed only for Heroku.com as production environment 

