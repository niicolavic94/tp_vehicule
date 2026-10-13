"""seed data

Revision ID: e94bd9d6a70a
Revises: ae12b7276c6b
Create Date: 2026-10-13 16:41:25.239547

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e94bd9d6a70a'
down_revision: Union[str, Sequence[str], None] = 'ae12b7276c6b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()

    res = conn.execute(sa.text(
        "INSERT INTO motors (type, power, consumption_thermic, capacity_thermic) "
        "VALUES ('thermique', 130, 6.5, 50)"
    ))
    thermic_id = res.lastrowid

    res = conn.execute(sa.text(
        "INSERT INTO motors (type, power, consumption_electric, capacity_electric) "
        "VALUES ('electrique', 150, 18.0, 60)"
    ))
    electric_id = res.lastrowid

    res = conn.execute(sa.text(
        "INSERT INTO motors (type, power, consumption_thermic, capacity_thermic, consumption_electric, capacity_electric) "
        "VALUES ('hybride', 200, 6.3, 45, 21.0, 11)"
    ))
    hybrid_id = res.lastrowid

    conn.execute(sa.text(
        f"INSERT INTO vehicles (brand, model, year, motor_id, kilometrage, volume_coffre, categorie) "
        f"VALUES ('Peugeot', '308', 2020, {thermic_id}, 0, 300, 'berline')"
    ))
    conn.execute(sa.text(
        f"INSERT INTO vehicles (brand, model, year, motor_id, kilometrage, volume_coffre, categorie) "
        f"VALUES ('Tesla', 'Model 3', 2024, {electric_id}, 0, 300, 'berline')"
    ))
    conn.execute(sa.text(
        f"INSERT INTO vehicles (brand, model, year, motor_id, kilometrage, volume_coffre, categorie) "
        f"VALUES ('Volvo', 'XC40', 2025, {hybrid_id}, 0, 300, 'suv')"
    ))


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM vehicles"))
    conn.execute(sa.text("DELETE FROM motors"))
