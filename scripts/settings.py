import os

DATA_DIR = "./stash/"
FETCHED_DIR = os.path.join(DATA_DIR, "fetched")
FETCHED_CANDSUMS_DIR = os.path.join(FETCHED_DIR, 'candsums')
COMPILED_DIR = os.path.join(DATA_DIR, "compiled")

# via data.gov
# https://api.data.gov/signup/
API_KEY = open("./scripts/api.key").read().strip()

def setup_space():
    os.makedirs(FETCHED_CANDSUMS_DIR, exist_ok = True)
    os.makedirs(COMPILED_DIR, exist_ok = True)
