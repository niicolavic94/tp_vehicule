"""init database

Revision ID: ae12b7276c6b
Revises: e41ed9c1d480
Create Date: 2026-10-13 16:36:45.971123

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ae12b7276c6b'
down_revision: Union[str, Sequence[str], None] = 'e41ed9c1d480'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'motors',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('type', sa.String(20), nullable=False),
        sa.Column('power', sa.Integer(), nullable=False),
        sa.Column('consumption_thermic', sa.Numeric(6, 2), nullable=True),
        sa.Column('capacity_thermic', sa.Numeric(6, 2), nullable=True),
        sa.Column('consumption_electric', sa.Numeric(6, 2), nullable=True),
        sa.Column('capacity_electric', sa.Numeric(6, 2), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'vehicles',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('brand', sa.String(100), nullable=False),
        sa.Column('model', sa.String(100), nullable=False),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('motor_id', sa.Integer(), nullable=False),
        sa.Column('kilometrage', sa.Numeric(10, 2), server_default='0.00', nullable=False),
        sa.Column('volume_coffre', sa.Numeric(10, 2), server_default='300.00', nullable=False),
        sa.Column('categorie', sa.String(30), server_default='berline', nullable=False),
        sa.ForeignKeyConstraint(['motor_id'], ['motors.id'], name='fk_vehicle_motor', onupdate='CASCADE', ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('vehicles')
    op.drop_table('motors')
