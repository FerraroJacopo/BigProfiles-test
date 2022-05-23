from fastapi import FastAPI, Request, HTTPException, Depends, Security
from route import router as DataRouter
from fastapi.security.api_key import APIKeyHeader, APIKey

X_API_KEY = APIKeyHeader(name='X-API-Key')

def validate_api_key(x_api_key: str = Depends(X_API_KEY)):
    if x_api_key == "BigProfiles-API":
        return True

    raise HTTPException(
        status_code=500,
        detail="Invalid API Key",
    )

app = FastAPI(dependencies=[Security(validate_api_key)],)

app.include_router(DataRouter, tags=["Data"])

@app.get("/", tags=["Root"])
def index():
    return {"name": "Jacopo",
            "surname" : "Ferraro",
            "test for" : "BigProfiles"}