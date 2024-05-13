# Set environment variables
export FLASK_APP=app.py
export FLASK_DEBUG=true

# Check if venv is installed
echo "Updating dependencies"
sudo apt-get update > /dev/null
sudo apt-get install -y python3 python3-pip python3-venv > /dev/null

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
pip install Flask-Migrate > /dev/null

echo "Starting app server now"
flask run