from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from app.schemas.schemas import RecipeCreate, RecipeOut, RecipeSearchResults
from app.database import get_db_pool
import asyncio

router = APIRouter(prefix="/recipes", tags=["recipes"])

def log_access(conn, recipe_id: int):
    # Simple background log (non-blocking write)
    asyncio.create_task(conn.execute("""
        INSERT INTO recipe_access_logs (recipe_id, log_time) VALUES ($1, NOW())
    """, recipe_id))

@router.post("/", response_model=RecipeOut)
async def create_recipe(payload: RecipeCreate, background_tasks: BackgroundTasks):
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        rec = await conn.fetchrow(
            """
            INSERT INTO recipes (title, description, category_id) VALUES ($1, $2, $3)
            RETURNING id, title, description, category_id
            """,
            payload.title, payload.description, payload.category_id
        )
        for ing in payload.ingredients:
            await conn.execute(
                """
                INSERT INTO recipe_ingredients (recipe_id, ingredient_id)
                VALUES ($1, $2)
                """,
                rec['id'], ing
            )
        background_tasks.add_task(log_access, conn, rec['id'])
        return RecipeOut(**dict(rec), ingredients=payload.ingredients)

@router.get("/search", response_model=RecipeSearchResults)
async def search_recipes(category_id: int = None, ingredient_id: int = None):
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        recipes = []
        # Efficient WHERE clause usage for index scan — as per candidate's index/schema
        if category_id and ingredient_id:
            rows = await conn.fetch(
                """
                SELECT r.id, r.title, r.description
                FROM recipes r
                JOIN recipe_ingredients ri ON r.id = ri.recipe_id
                WHERE r.category_id=$1 AND ri.ingredient_id=$2
                """,
                category_id, ingredient_id
            )
        elif category_id:
            rows = await conn.fetch(
                "SELECT id, title, description FROM recipes WHERE category_id=$1", category_id)
        elif ingredient_id:
            rows = await conn.fetch(
                """
                SELECT r.id, r.title, r.description
                FROM recipes r
                JOIN recipe_ingredients ri ON r.id = ri.recipe_id
                WHERE ri.ingredient_id=$1
                """,
                ingredient_id
            )
        else:
            rows = await conn.fetch("SELECT id, title, description FROM recipes LIMIT 20")
        for row in rows:
            recipes.append({"id": row["id"], "title": row["title"], "description": row["description"]})
        return RecipeSearchResults(recipes=recipes)

@router.get("/{recipe_id}", response_model=RecipeOut)
async def get_recipe(recipe_id: int):
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        rec = await conn.fetchrow("SELECT id, title, description, category_id FROM recipes WHERE id=$1", recipe_id)
        if not rec:
            raise HTTPException(status_code=404, detail='Recipe not found')
        ing_rows = await conn.fetch("SELECT ingredient_id FROM recipe_ingredients WHERE recipe_id=$1", recipe_id)
        ingredient_ids = [r['ingredient_id'] for r in ing_rows]
        return RecipeOut(**dict(rec), ingredients=ingredient_ids)
