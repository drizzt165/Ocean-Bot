# Ocean-Bot
Discord bot for my server and as a learning experience in python

## Setting up .env
Change the name of ".env_sample" to ".env" and fill in your data for each field.

### Setting up database
Change the SQLUser, SQLPass, SQLHost, and DATABASE variables to represent your DB connection.

#### Example for ClearDB MySQL using Heroku:

##### Example URL:
mysql://`<dbUser>`:`<dbPass>`@`<dbHost>`/`<dbSchema>`?reconnect=true

##### Changes in .env file
SQLUser = `'dbUser'`  
SQLPass = `'dbPass'`  
SQLHost = `'dbHost'`   
DATABASE = `'dbSchema'`  

### Discord Bot Token
Fill out the TOKEN variable with the bot token from discord development site.

### PREFIX
Change PREFIX variable to the prefix you want to use for each command.

## Setting up environment
Run `python -m venv OceanBot_env` to create a virtual environment if you wish in a desired directory.
Then run `python -m pip install -r requirements.txt` from Ocean-Bot/requirements.txt to download all modules.
If using a virtual environment, the make sure to select the desired interpreter.

### When installing new modules for development:
Run `python -m pip freeze > requirements.txt` to update the module requirements.

### Same Virtual Environment on multiple devices
Under `OceanBot_env/pyvenv.cfg`, change the `home` variable to the root of your python install.
