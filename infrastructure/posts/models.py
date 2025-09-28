from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.postgres import Base


class CategoryDatabaseModel(Base):
    """
    Основная модель категории в базе данных.
    """

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(default=True)
    description: Mapped[str] = mapped_column(unique=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class PostDatabaseModel(Base):
    """
    Основная модель поста в базе данных.
    """

    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    body: Mapped[str] = mapped_column(unique=True)
    title: Mapped[str] = mapped_column(default=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category: Mapped[CategoryDatabaseModel] = relationship(lazy="joined", viewonly=True)
