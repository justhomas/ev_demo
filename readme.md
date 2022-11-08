# Installation
1. Clone the repository

2. Create and activate a virtual environment
```sh
python3 -m venv .venv  #create 
source .venv/bin/activate #activate venv 
```

3. Install the required libraries
```sh
pip install -r requirements.txt
```

4. Run the project
```sh
uvicorn main:app --reload
```

The swagger documentation is available at `<host_name>/docs` and the address API are available at `<host_name>/addresses`