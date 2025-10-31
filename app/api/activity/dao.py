from app.database.dao import BaseDAO
from app.database.models import Activity
from app.database.database import asyncSessionMaker
from sqlalchemy.future import select
from sqlalchemy.orm import aliased
from sqlalchemy.sql.expression import literal

class ActivityDAO(BaseDAO):
    model = Activity

    @classmethod
    async def getItAndAllDescendansIdCte(cls, id: int, maxDepth: int = 3):
        """
        Генератор запроса: Активность по id и все её потомки до maxDepth уровня
        """
        # Рекурсивный CTE для получения всех дочерних активностей
        ActivityHierarchy = aliased(Activity, name="activity_hierarchy")
        
        # Базовый случай - начальная активность
        base_case = select(
            ActivityHierarchy.id,
            ActivityHierarchy.parent_id,
            literal(0).label('level')  # Уровень вложенности
        ).where(ActivityHierarchy.id == id).cte(
            name="activity_tree", 
            recursive=True
        )
        
        # Рекурсивный случай - дочерние активности
        recursive_case = select(
            ActivityHierarchy.id,
            ActivityHierarchy.parent_id,
            (base_case.c.level + 1).label('level')
        ).join(
                base_case, 
                ActivityHierarchy.parent_id == base_case.c.id
        ).where(
            base_case.c.level < maxDepth - 1  # Ограничение глубины
        )
        
        # Объединяем базовый и рекурсивный случаи
        activity_tree_cte = base_case.union_all(recursive_case)

        return activity_tree_cte
    
    @classmethod
    async def getItAndAllDescendans(cls, id: int, maxDepth: int = 3):
        cte = await cls.getItAndAllDescendansIdCte(id, maxDepth)
        query = select(Activity).join(cte,cte.c.id == Activity.id)

        async with asyncSessionMaker() as session:
            result = await session.execute(query)
            result = result.scalars().all()

        return result