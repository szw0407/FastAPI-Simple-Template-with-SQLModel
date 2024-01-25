# Warn: This is just an example script,
#       check and adapt it to your needs in production instead of using it as is.
# ===============================================================================
# check if in venv
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "In virtualenv: $VIRTUAL_ENV"
else
    # check if .venv exists
    if [[ -d .venv ]]; then
        echo "Found .venv"
    else
        echo "Creating .venv"
        python3 -m venv .venv
    fi
    echo "Activating .venv"
    source .venv/bin/activate
fi
# check if requirements are installed
if [[pip freeze | grep -F -x -q -f requirements.txt ]]; then
    echo "Requirements installed"
else
    echo "Installing requirements"
    pip install -r requirements.txt
fi

# start the app
echo "Starting uvicorn server on localhost, default port 8000:"
uvicorn main:app --reload
