from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import assets
from api.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="The core API engine for CreatorNexus AI asset management."
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(assets.router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {
        "message": "Welcome to CreatorNexus AI API",
        "docs": "/docs",
        "status": "operational"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)