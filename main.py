import uvicorn
from app.settings.config import RELOAD

if __name__ == '__main__':
    uvicorn.run(app='app.core.logic.router:app', reload=RELOAD)
