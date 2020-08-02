# Ocean-Bot
Discord bot for my server and as a learning experience in python


### Discord Bot Token
Change the name of ".env_sample" to ".env" and fill in your data for each field.

MUST have a bot TOKEN and PREFIX for bot to operate.

### Setting up environment
Run `python -m venv OceanBot_env` to create a virtual environment if you wish in a desired directory.
Then run `python -m pip install -r requirements.txt` from Ocean-Bot/requirements.txt to download all modules.
If using a virtual environment, the make sure to select the desired interpreter.

#### Same Virtual Environment on multiple devices
Under `OceanBot_env/pyvenv.cfg`, change the `home` variable to the root of your python install.

###### When installing new modules for development:
Run `python -m pip freeze > requirements.txt` to update the module requirements.
