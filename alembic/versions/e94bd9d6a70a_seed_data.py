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
    op.execute(sa.text(
        "INSERT INTO motors (type, power, consumption_thermic, capacity_thermic) "
        "VALUES ('thermique', 130, 6.5, 50)"
    ))

    op.execute(sa.text(
        "INSERT INTO motors (type, power, consumption_electric, capacity_electric) "
        "VALUES ('electrique', 150, 18.0, 60)"
    ))

    op.execute(sa.text(
        "INSERT INTO motors (type, power, consumption_thermic, capacity_thermic, consumption_electric, capacity_electric) "
        "VALUES ('hybride', 200, 6.3, 45, 21.0, 11)"
    ))

    op.execute(sa.text(
        "INSERT INTO vehicles (brand, model, year, motor_id, kilometrage, volume_coffre, categorie) "
        "VALUES ('Peugeot', '308', 2020, "
        "(SELECT id FROM motors WHERE type='thermique' AND power=130 "
        "ORDER BY id DESC LIMIT 1), 0, 300, 'berline')"
    ))
    op.execute(sa.text(
        "INSERT INTO vehicles (brand, model, year, motor_id, kilometrage, volume_coffre, categorie) "
        "VALUES ('Tesla', 'Model 3', 2024, "
        "(SELECT id FROM motors WHERE type='electrique' AND power=150 "
        "ORDER BY id DESC LIMIT 1), 0, 300, 'berline')"
    ))
    op.execute(sa.text(
        "INSERT INTO vehicles (brand, model, year, motor_id, kilometrage, volume_coffre, categorie) "
        "VALUES ('Volvo', 'XC40', 2025, "
        "(SELECT id FROM motors WHERE type='hybride' AND power=200 "
        "ORDER BY id DESC LIMIT 1), 0, 300, 'suv')"
    ))


def downgrade() -> None:
    op.execute(sa.text(
        "DELETE FROM vehicles WHERE (brand, model) IN "
        "(('Peugeot', '308'), ('Tesla', 'Model 3'), ('Volvo', 'XC40'))"
    ))
    op.execute(sa.text(
        "DELETE FROM motors WHERE (type, power) IN "
        "(('thermique', 130), ('electrique', 150), ('hybride', 200))"
    ))
