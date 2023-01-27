from sqlalchemy import select

from app.core.database.models import *
from app.core.database.init import async_session


class GamesMixin:
    @staticmethod
    async def get_user_created_games(user_id: int):
        async with async_session() as session:
            user_games = (await session.execute(
                select(Game.id)
                .join(User)
                .where(Game.user_id.__eq__(user_id))
            )).all()
            user_games = [item['id'] for item in user_games]
            return user_games
