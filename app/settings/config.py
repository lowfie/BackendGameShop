import environs

env = environs.Env()
env.read_env()

# database connect
USER_POSTGRES = env.str('USER_POSTGRES')
PASSWORD_POSTGRES = env.str('PASSWORD_POSTGRES')
HOST_POSTGRES = env.str('HOST_POSTGRES')
PORT_POSTGRES = env.str('PORT_POSTGRES')
DATABASE_POSTGRES = env.str('DATABASE_POSTGRES')

# gmail smtp ssl profile
SMTP_HOST = env.str('SMTP_HOST')
SMTP_PORT = env.str('SMTP_PORT')
SMTP_MAIL = env.str('SMTP_MAIL')
SMTP_PASSWORD = env.str('SMTP_PASSWORD')

# redis connection data
HOST_REDIS = env.str('HOST_REDIS')
PORT_REDIS = env.str('PORT_REDIS')

# fastapiauth secret key
SECRET = env.str('SECRET')

UVICORN_RELOAD = True
