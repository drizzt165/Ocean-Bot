# Ocean-Bot
Discord bot for my server and as a learning experience in python


## Discord Bot Token
Change the name of ".env_sample" to ".env" and fill in your data for each field.

MUST have a bot TOKEN to operate. You can create a bot and find this using the discord developer portal.

## Setting up environment

### Setup script
Run the `./scripts/Setup.bat` or `./scripts/Setup.py` files. This will create a virutal environment under the same directory.

### Manually
Run `python -m venv OceanBot_env` to create a virtual environment if you wish in a desired directory.
Then run `python -m pip install -r requirements.txt` from Ocean-Bot/requirements.txt to download all modules.
If using a virtual environment, then make sure to select the desired interpreter.

### When installing new modules for development:
Run `python -m pip install pipreqs` to install pipreqs. Then run `pipreqs ./ --ignore ./OceanBot_env --force` to update the requirements.txt
