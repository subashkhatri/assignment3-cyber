# Set environment variables
export FLASK_APP=app.py
export FLASK_DEBUG=true

# Check if venv is installed
if ! which virtualenv &> /dev/null
then
    echo "You don't have python3-venv installed.. Installing now.."
    sudo apt update > /dev/null
    sudo apt install -y python3-venv > /dev/null
fi

# Check if there's a venv
if ! ls $(pwd)/.venv &> /dev/null
then
    echo "Created you a venv"
    python3 -m venv $(pwd)/.venv
fi

echo "Activating venv"
. .venv/bin/activate

echo "Installing Python requirements"

pip install -r requirements.txt > /dev/null

echo "Running Database setup"
flask db init &> /dev/null
flask db migrate &> /dev/null
flask db upgrade &> /dev/null

echo "Starting app server now"
flask run