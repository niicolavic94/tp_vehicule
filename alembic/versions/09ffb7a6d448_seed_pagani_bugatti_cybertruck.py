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
    # Pagani Zonda — moteur thermique V12
    op.execute(sa.text(
        "INSERT INTO motors (type, power, consumption_thermic, capacity_thermic) "
        "VALUES ('thermique', 555, 25.0, 98)"
    ))

    # Bugatti Tourbillon — moteur hybride V16
    op.execute(sa.text(
        "INSERT INTO motors (type, power, consumption_thermic, capacity_thermic, consumption_electric, capacity_electric) "
        "VALUES ('hybride', 1800, 30.0, 90, 20.0, 25)"
    ))

    # Tesla Cybertruck — moteur électrique
    op.execute(sa.text(
        "INSERT INTO motors (type, power, consumption_electric, capacity_electric) "
        "VALUES ('electrique', 845, 35.0, 123)"
    ))

    op.execute(sa.text(
        "INSERT INTO vehicles (brand, model, year, motor_id, kilometrage, volume_coffre, categorie) "
        "VALUES ('Pagani', 'Zonda', 2005, "
        "(SELECT id FROM motors WHERE type='thermique' AND power=555 "
        "ORDER BY id DESC LIMIT 1), 15000, 150, 'berline')"
    ))
    op.execute(sa.text(
        "INSERT INTO vehicles (brand, model, year, motor_id, kilometrage, volume_coffre, categorie) "
        "VALUES ('Bugatti', 'Tourbillon', 2024, "
        "(SELECT id FROM motors WHERE type='hybride' AND power=1800 "
        "ORDER BY id DESC LIMIT 1), 500, 150, 'berline')"
    ))
    op.execute(sa.text(
        "INSERT INTO vehicles (brand, model, year, motor_id, kilometrage, volume_coffre, categorie) "
        "VALUES ('Tesla', 'Cybertruck', 2024, "
        "(SELECT id FROM motors WHERE type='electrique' AND power=845 "
        "ORDER BY id DESC LIMIT 1), 0, 1200, 'suv')"
    ))


def downgrade() -> None:
    op.execute(sa.text(
        "DELETE FROM vehicles WHERE (brand, model) IN "
        "(('Pagani', 'Zonda'), ('Bugatti', 'Tourbillon'), ('Tesla', 'Cybertruck'))"
    ))
    op.execute(sa.text("DELETE FROM motors WHERE power IN (555, 1800, 845)"))
