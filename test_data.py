import asyncio

from sqlalchemy import text

from app.database.database import asyncSessionMaker
from app.database.models import Activity, Building, Organization, Organization_Activity_Rel, Phone


async def create_test_data():
    async with asyncSessionMaker() as session:

        await session.execute(text("DELETE FROM organization_activity_rels"))
        await session.execute(text("DELETE FROM phones"))
        await session.execute(text("DELETE FROM organizations"))
        await session.execute(text("DELETE FROM activitys"))
        await session.execute(text("DELETE FROM buildings"))

        # Создаем здания
        buildings = [
            Building(
                address="г. Москва, ул. Блюхера, 32/1",
                latitude=55.7558,
                longitude=37.6173,
            ),
            Building(
                address="г. Москва, ул. Ленина, 1, офис 3",
                latitude=55.7517,
                longitude=37.6178,
            ),
            Building(
                address="г. Санкт-Петербург, Невский пр., 25",
                latitude=59.9343,
                longitude=30.3351,
            ),
        ]

        session.add_all(buildings)
        await session.flush()  # Получаем ID для зданий

        # Создаем древовидную структуру деятельностей (3 уровня)
        # Уровень 1
        food_activity = Activity(name="Еда", parent_id=None)
        cars_activity = Activity(name="Автомобили", parent_id=None)
        electronics_activity = Activity(name="Электроника", parent_id=None)

        session.add_all([food_activity, cars_activity, electronics_activity])
        await session.flush()

        # Уровень 2 для Еды
        meat_activity = Activity(name="Мясная продукция", parent_id=food_activity.id)
        dairy_activity = Activity(name="Молочная продукция", parent_id=food_activity.id)
        bakery_activity = Activity(
            name="Хлебобулочные изделия", parent_id=food_activity.id
        )

        # Уровень 2 для Автомобилей
        trucks_activity = Activity(name="Грузовые", parent_id=cars_activity.id)
        cars_parts_activity = Activity(name="Легковые", parent_id=cars_activity.id)

        # Уровень 2 для Электроники
        computers_activity = Activity(
            name="Компьютеры", parent_id=electronics_activity.id
        )
        phones_activity = Activity(name="Телефоны", parent_id=electronics_activity.id)

        session.add_all(
            [
                meat_activity,
                dairy_activity,
                bakery_activity,
                trucks_activity,
                cars_parts_activity,
                computers_activity,
                phones_activity,
            ]
        )
        await session.flush()

        # Уровень 3 для Легковых автомобилей
        car_parts_activity = Activity(name="Запчасти", parent_id=cars_parts_activity.id)
        car_accessories_activity = Activity(
            name="Аксессуары", parent_id=cars_parts_activity.id
        )

        # Уровень 3 для Компьютеров
        laptops_activity = Activity(name="Ноутбуки", parent_id=computers_activity.id)
        components_activity = Activity(
            name="Комплектующие", parent_id=computers_activity.id
        )

        # Уровень 3 для Мясной продукции
        beef_activity = Activity(name="Говядина", parent_id=meat_activity.id)
        pork_activity = Activity(name="Свинина", parent_id=meat_activity.id)
        poultry_activity = Activity(name="Птица", parent_id=meat_activity.id)

        session.add_all(
            [
                car_parts_activity,
                car_accessories_activity,
                laptops_activity,
                components_activity,
                beef_activity,
                pork_activity,
                poultry_activity,
            ]
        )
        await session.flush()

        # Создаем организации
        organizations = [
            Organization(name='ООО "Рога и Копыта"', building_id=buildings[0].id),
            Organization(name='АО "МолПродукт"', building_id=buildings[1].id),
            Organization(name="ИП Иванов", building_id=buildings[2].id),
            Organization(name='ЗАО "АвтоДеталь"', building_id=buildings[0].id),
            Organization(name='ООО "ТехноМир"', building_id=buildings[1].id),
        ]

        session.add_all(organizations)
        await session.flush()

        # Добавляем телефоны (у первой организации несколько номеров)
        phones = [
            # Для ООО "Рога и Копыта" - несколько номеров
            Phone(number="2-222-222", organization_id=organizations[0].id),
            Phone(number="3-333-333", organization_id=organizations[0].id),
            Phone(number="8-923-666-13-13", organization_id=organizations[0].id),
            # Для других организаций по одному номеру
            Phone(number="4-444-444", organization_id=organizations[1].id),
            Phone(number="5-555-555", organization_id=organizations[2].id),
            Phone(number="6-666-666", organization_id=organizations[3].id),
            Phone(number="7-777-777", organization_id=organizations[4].id),
        ]

        session.add_all(phones)

        # Создаем связи организаций с видами деятельности
        organization_activities = [
            # ООО "Рога и Копыта" - занимается разными видами деятельности
            Organization_Activity_Rel(
                organization_id=organizations[0].id, activity_id=meat_activity.id
            ),
            Organization_Activity_Rel(
                organization_id=organizations[0].id, activity_id=dairy_activity.id
            ),
            Organization_Activity_Rel(
                organization_id=organizations[0].id, activity_id=car_parts_activity.id
            ),
            # АО "МолПродукт" - специализируется на молочной продукции
            Organization_Activity_Rel(
                organization_id=organizations[1].id, activity_id=dairy_activity.id
            ),
            # ИП Иванов - мясная продукция разных видов
            Organization_Activity_Rel(
                organization_id=organizations[2].id, activity_id=beef_activity.id
            ),
            Organization_Activity_Rel(
                organization_id=organizations[2].id, activity_id=pork_activity.id
            ),
            # ЗАО "АвтоДеталь" - автомобильные запчасти и аксессуары
            Organization_Activity_Rel(
                organization_id=organizations[3].id, activity_id=car_parts_activity.id
            ),
            Organization_Activity_Rel(
                organization_id=organizations[3].id,
                activity_id=car_accessories_activity.id,
            ),
            # ООО "ТехноМир" - электроника и компьютеры
            Organization_Activity_Rel(
                organization_id=organizations[4].id, activity_id=laptops_activity.id
            ),
            Organization_Activity_Rel(
                organization_id=organizations[4].id, activity_id=components_activity.id
            ),
            Organization_Activity_Rel(
                organization_id=organizations[4].id, activity_id=phones_activity.id
            ),
        ]

        session.add_all(organization_activities)

        # Сохраняем все изменения
        await session.commit()

        print("Тестовые данные успешно созданы!")
        print(f"Создано: {len(buildings)} зданий")
        print(
            f"Создано: {len([a for a in session.identity_map.values() if isinstance(a, Activity)])} видов деятельности"
        )
        print(f"Создано: {len(organizations)} организаций")
        print(f"Создано: {len(phones)} телефонных номеров")
        # print(f"У организации 'ООО \"Рога и Копыта\"' создано {len([p for p in phones if p.organization_id == organizations[0].id])} телефонных номера")


async def main():
    await create_test_data()


if __name__ == "__main__":
    asyncio.run(main())
