from app.routers import products, categories
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


app.include_router(products.router)
app.include_router(categories.router)

