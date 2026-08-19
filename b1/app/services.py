from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.model import User, Role

def init_mock_data(db: Session):
    """Khởi tạo dữ liệu mẫu nếu database chưa có"""
    now = datetime.now(timezone.utc)

    if not db.query(Role).first():
        roles = [
            Role(name="ADMIN", description="Quản trị viên hệ thống", created_at=now),
            Role(name="HR", description="Quản lý nhân sự và bảng lương", created_at=now),
            Role(name="STAFF", description="Nhân viên thông thường", created_at=now),
        ]
        db.add_all(roles)
        db.commit()

    if not db.query(User).first():
        users = [
            User(name="Quản Trị Viên", email="admin@megamart.com", password="adminpassword", role="ADMIN", created_at=now),
            User(name="Nhân Sự HR", email="hr@megamart.com", password="hrpassword", role="HR", created_at=now),
            User(name="Nhân Viên", email="staff@megamart.com", password="staffpassword", role="STAFF", created_at=now),
        ]
        db.add_all(users)
        db.commit()