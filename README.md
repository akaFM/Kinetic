# Kinetic
Task managing fullstack app

### Installation for macOS/Linux
```bash
git clone https://github.com/akaFM/Kinetic.git
cd Kinetic
sh ./setup.sh
echo "DEBUG=True" > taskFlow/taskFlow/.env # for dev only
python taskFlow/manage.py migrate
