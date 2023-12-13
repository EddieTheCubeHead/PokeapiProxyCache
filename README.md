# PokeapiProxyCache
A caching proxy server that hosts a two layer (db+ram) key-value cache of pokeapi requests.

Written to not stress pokeapi servers with requests while testing pokeapi for a school project.

## Running

### Create venv and install requirements

If you are not using a tool like PyCharm that creates a venv for you automatically
you need to manually create or move to the virtual environment

Creating the virtual environment is done with python's venv module:
`python -m venv .\venv`

Depending on the tool you are using this might not open the virtual environment.
The virtual environment is open, if the command line feed starts with `(venv)`.

If you have already created the venv but have closed the session after the 
creation of the venv or the venv has not opened, you need to open the venv with
a command. Assuming a ps terminal, this can be done with the following command (make 
sure powershell has the right to run scripts):

`.\venv\Scripts\Activate.ps1`

Other terminals should use the activate script in the folder that corresponds with the terminal type.

After your terminal has `(venv)` on the left side of the line, you can install the requirements with

`pip install -r requirements.txt`

### Run the server

After installing requirements, you can run the server with

`uvicorn src.app:app`
