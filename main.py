import uvicorn
from app.settings.config import UVICORN_RELOAD

if __name__ == '__main__':
    uvicorn.run(app='app.core.logic.router:app', reload=UVICORN_RELOAD)
