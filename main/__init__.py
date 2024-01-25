from .app import *
import uvicorn, sys

def main():
    # read --host and --port from command line, e.g. `python main.py --host 127.0.0.1 --port 8000`
    host: str = sys.argv[sys.argv.index("--host") + 1] if "--host" in sys.argv else "127.0.0.1"
    port: str = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else "8000"
    uvicorn.run(app, host=host, port=int(port))