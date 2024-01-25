# FastAPI-simple-Template-with-SQLmodel

A simple example of FastAPI.

In this example, we will create a service of a online store.

Users can register, login, and see the information of the items.

Sellers can do all the things that users can do, and also can add, update, and delete items.

Admins can do all the things that sellers can do, and also can add, update, and delete users.

## Requirements

- Python >= 3.10
- Install requirements using PDM, or pip from requirements.txt

## Run

### Recommended

If you have installed PDM, you can run the following command to start the service:

```powershell
pdm start <args>
```

### Other ways

If installed properly, you can run the following command to start the service:

```bash
start-server
```

Or, you can run the following command to start the service:

```bash
uvicorn main:app --reload
```

You might try the start script (NOT FULLY TESTED) too:

```bash
source ./start.sh
```

powershell:

```powershell
.\start.ps1
```

## Arguments

All arguments are the same as `uvicorn`'s arguments. Below are some of the mostly used arguments:

- `--host`: The host to listen on. (default: `127.0.0.1`)
- `--port`: The port to listen on. (default: `8000`, which is also the same as `python -m http.server`'s default)
- `--reload`: Enable auto-reload.

## API

Visit the SwaggerUI at `/docs` or the Redoc at `/redoc` to see the API.

## License

Currently, this project is licensed under the MIT License. See [LICENSE](./LICENSE) for more information.

## TODO

Since this is just a simple example, there are still many things to do, including but not limited to:

- [ ] Add tests templates
- [ ] Add CI/CD templates
- [ ] Add Dockerfile

I shall appreciate it if you can help me with these things.

Moreover, I am considering making a frontend for this project. Perhaps I will use Vue.js, but when I will do it is still unknown.
