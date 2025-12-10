from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import aliased
from sqlalchemy.sql.expression import literal

from app.database.dao import BaseDAO
from app.database.models import Activity


class ActivityDAO(BaseDAO):
    model = Activity

    @classmethod
    async def getItAndAllDescendans(
        cls, session: AsyncSession, id: int, maxDepth: int = 3
    ):
        cte = await cls._getItAndAllDescendans(id, maxDepth)
        query = select(Activity).join(cte, cte.c.id == Activity.id)

        descendans = await session.execute(query.where(Activity.id != id))
        descendans = descendans.scalars().all()
        root = await session.execute(query.where(Activity.id == id))
        root = root.scalars().one_or_none()

        result = {}
        if root:
            result = root.toDict()
            result["descendans"] = descendans

        return result

    @classmethod
    async def _getItAndAllDescendans(cls, id: int, maxDepth: int = 3):
        """
        Генератор запроса: Активность по id и все её потомки до maxDepth уровня
        """
        # Рекурсивный CTE для получения всех дочерних активностей
        ActivityHierarchy = aliased(Activity, name="activity_hierarchy")

        # Базовый случай - начальная активность
        base_case = (
            select(
                ActivityHierarchy.id,
                ActivityHierarchy.parent_id,
                literal(0).label("level"),  # Уровень вложенности
            )
            .where(ActivityHierarchy.id == id)
            .cte(name="activity_tree", recursive=True)
        )

        # Рекурсивный случай - дочерние активности
        recursive_case = (
            select(
                ActivityHierarchy.id,
                ActivityHierarchy.parent_id,
                (base_case.c.level + 1).label("level"),
            )
            .join(base_case, ActivityHierarchy.parent_id == base_case.c.id)
            .where(base_case.c.level < maxDepth - 1)  # Ограничение глубины
        )

        # Объединяем базовый и рекурсивный случаи
        activity_tree_cte = base_case.union_all(recursive_case)

        return activity_tree_cte
