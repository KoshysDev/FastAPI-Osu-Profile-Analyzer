from fastapi import FastAPI, Request, Query, status
from fastapi.responses import RedirectResponse
from typing import Optional
from starlette.responses import HTMLResponse
import httpx, os, fileinput

from dotenv import load_dotenv

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint to redirect to frontend page
@app.get("/")
async def redirect_to_frontend(request: Request):
    frontend_url = "http://localhost:5173/"
    return RedirectResponse(url=frontend_url)

@app.post("/api/authenticate")
async def authenticate():
    app_id = os.getenv("OSU_APP_ID")
    app_secret = os.getenv("OSU_APP_SECRET")
    url = "https://osu.ppy.sh/oauth/token"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    data = {"client_id": app_id, "client_secret": app_secret, "grant_type": "client_credentials", "scope": "public"}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)

    if response.status_code != 200:
        return {"error": "Failed to authenticate"}

    # Replace access token in .env file
    access_token = response.json()["access_token"]
    with fileinput.FileInput(".env", inplace=True) as file:
        for line in file:
            if line.startswith("OSU_ACCESS_KEY="):
                line = f"OSU_ACCESS_KEY={access_token}\n"
            print(line, end='')

    return {"success": "Authenticated successfully"}

# Endpoint to return the user profile data
@app.get("/api/user/{user_id}")
async def get_user_profile(user_id: str):
    access_token = os.getenv("OSU_ACCESS_KEY")

    # If access_token is None, return an error
    if access_token is None:
        return {"error": "Access token not available"}

    # Make API call to get user profile data
    url = f"https://osu.ppy.sh/api/v2/users/{user_id}/osu"
    headers = {"Authorization": f"Bearer {access_token}", "Accept": "application/json", "Content-Type": "application/json"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    return response.json()

# Endpoint to return the user scores
@app.get("/api/user/{user_id}/scores")
async def get_user_scores(user_id: int, mode: str = "osu", limit: int = 100, offset: int = 0, include_fails: int = 0):
    access_token = os.getenv("OSU_ACCESS_KEY")
    if access_token is None:
        return {"error": "Access token not available"}

    url = f"https://osu.ppy.sh/api/v2/users/{user_id}/scores/best"
    headers = {"Authorization": f"Bearer {access_token}", "Accept": "application/json", "Content-Type": "application/json"}

    params = {
        "include_fails": include_fails,
        "mode": mode,
        "limit": limit,
        "offset": offset,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)

    return response.json()



# Validate token method
@app.get("/api/validate_token")
async def validate_token():
    access_token = os.getenv("OSU_ACCESS_KEY")
    
    if not access_token:
        # Call authenticate endpoint to get a new access token
        await authenticate()
        access_token = os.getenv("OSU_ACCESS_KEY")
    
    # Make a test API call to verify if the access token is still valid
    url = "https://osu.ppy.sh/api/v2/me"
    headers = {"Authorization": f"Bearer {access_token}", "Accept": "application/json", "Content-Type": "application/json"}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    if response.status_code != 200:
        # Call authenticate endpoint to get a new access token
        await authenticate()
    
    return {"status": "success"}

# 404 page Enppoint for backend side
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

# if no endpoint found for url on backend side - redirect to 404 page
@app.get("/{catchall:path}")
async def not_found(request: Request, catchall: str) -> HTMLResponse:
    return RedirectResponse("http://127.0.0.1:8000/404")
