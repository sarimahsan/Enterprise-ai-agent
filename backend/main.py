from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from api.routes import router
from api.extended_routes import extended_router
from core.database import init_db
import traceback

app = FastAPI(
    title="FlowForge API",
    description="Multi-agent enterprise sales outreach system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Custom exception handler for validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors with detailed debug logging"""
    print(f"\n⚠️  [VALIDATION ERROR] 422 Unprocessable Content")
    print(f"⚠️  [REQUEST PATH] {request.url.path}")
    print(f"⚠️  [REQUEST METHOD] {request.method}")
    print(f"⚠️  [VALIDATION ERRORS]")
    for error in exc.errors():
        print(f"  - {error['loc']}: {error['msg']} (type: {error['type']})")
    print(f"⚠️  [BODY] {exc.body if hasattr(exc, 'body') else 'N/A'}\n")
    
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation error - check server logs for details",
            "errors": [
                {
                    "loc": list(error["loc"]),
                    "msg": error["msg"],
                    "type": error["type"]
                }
                for error in exc.errors()
            ]
        },
    )

app.include_router(router, prefix="/api")
app.include_router(extended_router, prefix="/api")

@app.on_event("startup")
async def startup():
    """Initialize database on startup"""
    init_db()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)