from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class OperationInput(BaseModel):
    a: int
    b: int

@app.post("/multiply")
async def multiply(input_data: OperationInput):
    result = input_data.a * input_data.b
    return {"result": result}