from pydantic import BaseModel


class ProductElasticResponse(BaseModel):
    product_id: int
    title: str
    score: float

class CategoryElasticResponse(BaseModel):
    category_id: int
    title: str
    score: float
