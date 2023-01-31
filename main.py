import uvicorn
from app.settings.config import UVICORN_RELOAD

if __name__ == '__main__':
    uvicorn.run(app='app.core.logic.router:app', host='0.0.0.0', port=8000, reload=UVICORN_RELOAD)
