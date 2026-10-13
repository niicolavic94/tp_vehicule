"""seed pagani bugatti cybertruck

Revision ID: 09ffb7a6d448
Revises: e94bd9d6a70a
Create Date: 2026-10-13 16:44:33.861159

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '09ffb7a6d448'
down_revision: Union[str, Sequence[str], None] = 'e94bd9d6a70a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()

    # Pagani Zonda — moteur thermique V12
    res = conn.execute(sa.text(
        "INSERT INTO motors (type, power, consumption_thermic, capacity_thermic) "
        "VALUES ('thermique', 555, 25.0, 98)"
    ))
    zonda_motor_id = res.lastrowid

    # Bugatti Tourbillon — moteur hybride V16
    res = conn.execute(sa.text(
        "INSERT INTO motors (type, power, consumption_thermic, capacity_thermic, consumption_electric, capacity_electric) "
        "VALUES ('hybride', 1800, 30.0, 90, 20.0, 25)"
    ))
    bugatti_motor_id = res.lastrowid

    # Tesla Cybertruck — moteur électrique
    res = conn.execute(sa.text(
        "INSERT INTO motors (type, power, consumption_electric, capacity_electric) "
        "VALUES ('electrique', 845, 35.0, 123)"
    ))
    cybertruck_motor_id = res.lastrowid

    conn.execute(sa.text(
        f"INSERT INTO vehicles (brand, model, year, motor_id, kilometrage, volume_coffre, categorie) "
        f"VALUES ('Pagani', 'Zonda', 2005, {zonda_motor_id}, 15000, 150, 'berline')"
    ))
    conn.execute(sa.text(
        f"INSERT INTO vehicles (brand, model, year, motor_id, kilometrage, volume_coffre, categorie) "
        f"VALUES ('Bugatti', 'Tourbillon', 2024, {bugatti_motor_id}, 500, 150, 'berline')"
    ))
    conn.execute(sa.text(
        f"INSERT INTO vehicles (brand, model, year, motor_id, kilometrage, volume_coffre, categorie) "
        f"VALUES ('Tesla', 'Cybertruck', 2024, {cybertruck_motor_id}, 0, 1200, 'suv')"
    ))


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM vehicles WHERE brand IN ('Pagani', 'Bugatti') OR (brand = 'Tesla' AND model = 'Cybertruck')"))
    conn.execute(sa.text("DELETE FROM motors WHERE power IN (555, 1800, 845)"))
