import environs

env = environs.Env()
env.read_env()

# database connect
USER_POSTGRES = env.str('USER_POSTGRES')
PASSWORD_POSTGRES = env.str('PASSWORD_POSTGRES')
HOST_POSTGRES = env.str('HOST_POSTGRES')
PORT_POSTGRES = env.str('PORT_POSTGRES')
DATABASE_POSTGRES = env.str('DATABASE_POSTGRES')

# fastapiauth secret key
SECRET = env.str('SECRET')

UVICORN_RELOAD = True


