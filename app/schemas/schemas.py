from pydantic import BaseModel
from typing import List, Optional

class RecipeCreate(BaseModel):
    title: str
    description: Optional[str]
    category_id: int
    ingredients: List[int]

class RecipeOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    category_id: int
    ingredients: List[int]

class RecipeSearchResults(BaseModel):
    recipes: List[dict]
