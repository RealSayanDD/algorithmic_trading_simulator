from decimal import Decimal
from enum import Enum

from sqlalchemy import Boolean, Enum as SqlEnum, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base


class AssetType(str, Enum):
    STOCK = "stock"
    CRYPTOCURRENCY = "cryptocurrency"


class Asset(Base):
    __tablename__ = "assets"

    id: Mapped[int] = mapped_column(primary_key=True)
    symbol: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    asset_type: Mapped[AssetType] = mapped_column(
        SqlEnum(
            AssetType,
            name="asset_type",
            values_callable=lambda enum_type: [item.value for item in enum_type],
        ),
        nullable=False,
    )
    current_price: Mapped[Decimal] = mapped_column(Numeric(20, 8), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
