from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column


class UsersOrm(Base):
    __tablename__ = "users"

    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(nullable=False)
    email : Mapped[str] = mapped_column(nullable=False, unique=True)
    password : Mapped[str] = mapped_column(nullable=False)
    team_name : Mapped[str] = mapped_column(nullable=False)
    access_level: Mapped[str] = mapped_column(default="user")
    role: Mapped[str] = mapped_column(default="employee")
    department_name: Mapped[str] = mapped_column()

    