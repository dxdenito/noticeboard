import asyncio
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.role import Role
from app.models.category import Category

ROLE_NAMES = ["admin", "hod", "club_leader", "student_leader", "student"]
CATEGORY_NAMES = ["tender", "vacancy", "event", "academic", "deadline", "general"]


async def seed_roles(db) -> None:
    for name in ROLE_NAMES:
        existing = await db.execute(select(Role).where(Role.role == name))
        if existing.scalar_one_or_none() is None:
            db.add(Role(role=name))


async def seed_categories(db) -> None:
    for name in CATEGORY_NAMES:
        existing = await db.execute(select(Category).where(Category.name == name))
        if existing.scalar_one_or_none() is None:
            db.add(Category(name=name))


async def seed_all() -> None:
    async with AsyncSessionLocal() as db:
        await seed_roles(db)
        await seed_categories(db)
        await db.commit()
        print("Seed complete: roles + categories.")


if __name__ == "__main__":
    asyncio.run(seed_all())