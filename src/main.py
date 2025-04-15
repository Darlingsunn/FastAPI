import uvicorn
from fastapi import FastAPI
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))


from src.api.hotels import router as router_hotels


app = FastAPI()

app.include_router(router_hotels)


# @app.get("/docs", include_in_schema=False)
# async def custom_swagger_ui_html():
#      return get_swagger_ui_html(
#          openapi_url=app.openapi_url,
#          title=app.title + " - Swagger UI",
#          oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
#          swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
#          swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
#      )

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
