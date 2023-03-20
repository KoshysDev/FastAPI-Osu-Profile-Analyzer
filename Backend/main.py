from fastapi import FastAPI, Request, Query, status
from fastapi.responses import RedirectResponse
from starlette.responses import HTMLResponse
from services import parse_url

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint to redirect to frontend page
@app.get("/")
async def redirect_to_frontend(request: Request):
    frontend_url = "http://localhost:5173/"
    return RedirectResponse(url=frontend_url)

@app.get("/404", response_class=HTMLResponse)
async def not_found(request: Request):
    return """
        <html>
            <head>
                <title>404 Not Found</title>
            </head>
            <body>
                <h1>404 Not Found</h1>
                <p>The requested resource could not be found.</p>
            </body>
        </html>
    """

@app.get("/{catchall:path}")
async def not_found(request: Request, catchall: str) -> HTMLResponse:
    return RedirectResponse("http://127.0.0.1:8000/404")


@app.get("/parse_url")
async def parse_url_endpoint(url: str = Query(...)):
    parsed_data = parse_url(url)
    return parsed_data