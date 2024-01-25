# Warn: This is just an example script,
#       check and adapt it to your needs in production instead of using it as is.
# ==============================================================================
# check if in venv
if ($env:VIRTUAL_ENV -eq $null) {
    echo "Not in venv, activating..."
    # check if venv exists
    if (Test-Path .venv) {
        echo "venv exists, activating..."
    } else {
        echo "venv does not exist, creating..."
        # create venv
        python -m venv .venv

        # activate venv
        echo "venv created, activating..."
        . .venv/Scripts/activate

    }
        # activate venv
        . .venv/Scripts/activate
        
}
# check if requirements are installed properly
        if (Compare-Object -ReferenceObject (pip freeze | Out-String) -DifferenceObject (Get-Content -Path requirements.txt | Out-String) -IncludeEqual) {
            echo "requirements.txt installed"
        } else {
            echo "requirements.txt not installed, installing..."
            # install requirements
            pip install -r requirements.txt
        }
echo "Starting uvicorn server on localhost, default port 8000:"

uvicorn main:app --reload
