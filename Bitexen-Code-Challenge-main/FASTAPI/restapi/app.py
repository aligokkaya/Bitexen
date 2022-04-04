from fastapi import FastAPI
from crud.main import bitexenAPI
import uvicorn
app = FastAPI()

app.include_router(bitexenAPI)

if __name__ == "__main__":
    uvicorn.run(app)    
    