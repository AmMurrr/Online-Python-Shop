from app.routers import sales
from fastapi import FastAPI


description = """
- 


"""


app = FastAPI(
    description=description,
    title="API",
    version="1.0.0",
    swagger_ui_parameters={
        "syntaxHighlight.theme": "monokai",
        "layout": "BaseLayout",
        "filter": True,
        "tryItOutEnabled": True,
        "onComplete": "Ok"
    },
)


app.include_router(sales.router)
