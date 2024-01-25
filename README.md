# FastAPI-simple-example

A simple example of FastAPI.

In this example, we will create a service of a online store.

Users can register, login, and see the information of the items.

Sellers can do all the things that users can do, and also can add, update, and delete items.

Admins can do all the things that sellers can do, and also can add, update, and delete users.

## Requirements

- Python >= 3.10
- Install requirements using PDM, or pip from requirements.txt

## Run

```bash
uvicorn main:app --reload
```

Or, you might try the start script (NOT FULLY TESTED):

```bash
source ./start.sh
```

powershell:

```powershell
.\start.ps1
```
