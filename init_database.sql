-- Categories table
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

-- Ingredients table
CREATE TABLE IF NOT EXISTS ingredients (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

-- Recipes table
CREATE TABLE IF NOT EXISTS recipes (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    category_id INT,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- Association table for M2M
CREATE TABLE IF NOT EXISTS recipe_ingredients (
    recipe_id INT,
    ingredient_id INT,
    PRIMARY KEY (recipe_id, ingredient_id),
    FOREIGN KEY (recipe_id) REFERENCES recipes(id),
    FOREIGN KEY (ingredient_id) REFERENCES ingredients(id)
);

-- Simple access log for background task demo
CREATE TABLE IF NOT EXISTS recipe_access_logs (
    id SERIAL PRIMARY KEY,
    recipe_id INT,
    log_time TIMESTAMP,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id)
);

-- Sample categories
INSERT INTO categories (name) VALUES
('Dessert'), ('Main'), ('Appetizer'), ('Salad')
ON CONFLICT DO NOTHING;

-- Sample ingredients
INSERT INTO ingredients (name) VALUES
('Eggs'), ('Milk'), ('Sugar'), ('Flour'), ('Tomato'), ('Cheese')
ON CONFLICT DO NOTHING;

-- Sample recipes
INSERT INTO recipes (title, description, category_id) VALUES
('Pancakes', 'Fluffy breakfast pancakes.', 1),
('Tomato Salad', 'Fresh summer tomato salad.', 4)
ON CONFLICT DO NOTHING;

-- Sample associations
INSERT INTO recipe_ingredients (recipe_id, ingredient_id) VALUES
(1, 1),(1, 2),(1, 3),(1, 4),  -- Pancakes: Eggs, Milk, Sugar, Flour
(2, 5),(2, 6)                 -- Tomato Salad: Tomato, Cheese
ON CONFLICT DO NOTHING;
