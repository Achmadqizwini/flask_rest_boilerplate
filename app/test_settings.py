from environs import Env

env = Env()
env.read_env()

db_host = env.str("DB_HOST")
db_user = env.str("DB_USER")
db_password = env.str("DB_PASSWORD")
db_port = env.str("DB_PORT")
db_name = env.str("TEST_DB")
debug_mode = env.str("DEBUG")


def get_db_uri(db_user, db_password):
    return f"mysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


DATABASE_URI = get_db_uri(db_user, db_password)
DATABASE_URI = get_db_uri(db_user=db_user, db_password=db_password)
TESTING = True
SQLALCHEMY_DATABASE_URI = DATABASE_URI
BCRYPT_LOG_ROUNDS = 4
DEBUG_TB_ENABLED = False

# Redis settings
redis_cache_config = {
    "CACHE_TYPE": "simple",
    "CACHE_REDIS_URL": None
}

REDIS_HOST = env.str("REDIS_HOST")
REDIS_PORT = env.int("REDIS_PORT")
REDIS_PASSWORD = env.str("REDIS_PASSWORD")

if REDIS_HOST and REDIS_PORT:
    redis_cache_config["CACHE_TYPE"] = "redis"
    redis_cache_config["CACHE_REDIS_URL"] = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"

if REDIS_PASSWORD:
    redis_cache_config["CACHE_REDIS_URL"] = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0"