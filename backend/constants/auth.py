import config  # Load environment configuration

SECRET_KEY = config.JWT_SECRET_KEY
ALGORITHM = config.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = 480  # 8 hours to expire
