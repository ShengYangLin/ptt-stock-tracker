# Description
```bash
Ptt Stock Tracker tracks posts and "pushes" of certain users from the PTT Stock forum.
You may found some interesting, intrcutive or even profitable information from those messages.
```

# Installation
## Assume MySQL is installed and database is created.
## Run following command to install:
```bash
# for virtual environment
pip install pipenv
# install requirements
pipenv install
```

## Usage
Change .demo_env to .env and set the variables for your needs.
Apply token for Line Notification and set to "LINE_TOKEN" in .env.
```bash
run
# Start the crawling process.
pipenv run python crawler_scheduler.py
# Start the notifying process.
pipenv run python notifer_scheduler.py
```

Several settings can be changed inside config.yaml.