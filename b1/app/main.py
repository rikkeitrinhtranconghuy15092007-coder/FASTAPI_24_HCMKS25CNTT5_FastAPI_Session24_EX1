from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine, SessionLocal
from app.services import init_mock_data

# Khởi tạo bảng dữ liệu và mock data
Base.metadata.create_all(bind=engine)
db = SessionLocal()
init_mock_data(db)
db.close()

app = FastAPI(title="Demo Role & CORS Authorization System")

# ==================== PHẦN 4: CẤU HÌNH CORS ====================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://internal.megamart.com"],  # Tuyệt đối không dùng "*"
    allow_methods=["GET", "POST"],                    # Chỉ cho phép GET, POST
    allow_headers=["Content-Type", "X-User-Role"],    # Chỉ cho phép Content-Type, X-User-Role
    allow_credentials=True,
)

# ==================== PHẦN 1 & 2: CUSTOM MIDDLEWARE PHÂN QUYỀN ====================
ROUTE_PERMISSIONS = {
    "/api/v1/system/settings": ["ADMIN"],
    "/api/v1/salary/modify": ["ADMIN", "HR"],
    "/api/v1/profile": ["ADMIN", "HR", "STAFF"],
}

@app.middleware("http")
async def role_based_access_control_middleware(request: Request, call_next):
    path = request.url.path

    # Bỏ qua kiểm tra quyền cho tài liệu OpenAPI (Swagger UI) và options request của CORS
    if path.startswith(("/docs", "/openapi.json", "/redoc")) or request.method == "OPTIONS":
        return await call_next(request)

    # Kiểm tra nếu endpoint yêu cầu phân quyền
    if path in ROUTE_PERMISSIONS:
        required_roles = ROUTE_PERMISSIONS[path]
        user_role = request.headers.get("X-User-Role")

        # Chặn nếu không có role hoặc role không khớp quyền
        if not user_role or user_role not in required_roles:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"error": "Permission Denied"}
            )

    return await call_next(request)

# ==================== PHẦN 3: CÁC API ENDPOINTS ====================

@app.get("/api/v1/salary/modify", tags=["Salary"])
def modify_salary(request: Request):
    return {
        "status": 200,
        "message": "Truy cập bảng lương thành công.",
        "granted_for_role": request.headers.get("X-User-Role"),
        "data": {"salary_budget": "500,000,000 VND", "action": "modify_permitted"}
    }

@app.get("/api/v1/system/settings", tags=["System"])
def get_system_settings(request: Request):
    return {
        "status": 200,
        "message": "Truy cập cấu hình hệ thống thành công.",
        "granted_for_role": request.headers.get("X-User-Role"),
        "data": {"maintenance_mode": False, "server_version": "v1.0.4"}
    }

@app.get("/api/v1/profile", tags=["Profile"])
def get_profile(request: Request):
    return {
        "status": 200,
        "message": "Truy cập thông tin cá nhân thành công.",
        "granted_for_role": request.headers.get("X-User-Role"),
        "data": {"username": "current_user", "profile_status": "active"}
    }