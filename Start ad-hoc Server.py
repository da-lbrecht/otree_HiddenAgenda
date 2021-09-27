# Execute the following commands in terminal

#  Activate virtual environment
python3 -m venv venv_otree

# Reset database on the server
pip3 install -r requirements.txt
otree resetdb

sudo -E env "PATH=$PATH" "DATABASE_URL = 'postgres://postgres@localhost/hiddenagenda_db'" "OTREE_PRODUCTION=1" otree prodserver 80

export DATABASE_URL = 'postgres://postgres@localhost/hiddenagenda_db'
export ADMIN_PASSWORD=my_password
export OTREE_PRODUCTION=1
export OTREE_AUTH_LEVEL=DEMO