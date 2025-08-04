# Recipe Management System — FastAPI & PostgreSQL Task

## Task Overview
You are working on a recipe management backend where users need to efficiently search and browse recipes by category or ingredient. While the FastAPI application’s routing and endpoints are complete, you must design and implement the PostgreSQL database schemas, relationships, and async-compatible integration logic. The business has reported slow recipe searches and difficulty managing growing datasets, so your work is critical to support a smooth user experience as the system scales.

## Guidance
- Design normalized PostgreSQL schemas for recipes, ingredients, categories, and their relationships, including appropriate foreign keys and indexing.
- Implement async, non-blocking database operations so FastAPI endpoints can serve many requests concurrently without blocking.
- Ensure your schema supports efficient filtering of recipes by category or ingredient, and includes the correct keys and constraints.
- Add indexes on columns likely used in WHERE clauses (e.g., category_id, ingredient_id, recipe_id) to improve lookup speed.
- Test your logic using the provided endpoints; the API scaffolding and routing is already set up — focus on the database, not API code.
- Use basic background tasks (such as logging or stats tracking) that demonstrate proper async PostgreSQL integration.

## Database Access
- Host: <DROPLET_IP>
- Port: 5432
- Database: recipes
- Username: utkrusht
- Password: utkrushtpass
- Connect with tools like pgAdmin, DBeaver, or psql for direct schema or query validation as needed.

## Objectives
- Implement normalized PostgreSQL schemas for all required entities with proper relationships and constraints.
- Write FastAPI data access logic using async (asyncpg or equivalent) for all create, read, and search operations.
- Ensure that filtering recipes by ingredient or category is performant and non-blocking.
- Support at least one FastAPI background task safely writing to the database (e.g., access logging, recipe view counts).
- Validate correct async DB usage by running concurrent requests to the endpoints.

## How to Verify
- Verify the schema in PostgreSQL using database tools; relationships, primary and foreign keys, and indexes must be present.
- Confirm that all FastAPI endpoints related to recipe search, creation, and detail retrieval work as expected with the designed schema.
- Use ab or similar to make concurrent requests and ensure performance does not degrade or block under load.
- Check that background tasks involving the database execute successfully without blocking main request handling.
