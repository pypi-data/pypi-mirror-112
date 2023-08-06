"""drop unique mac constraint

Revision ID: f57435bbe6e7
Revises: 6b0896f05118
Create Date: 2021-05-28 19:03:26.812018

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f57435bbe6e7'
down_revision = '6b0896f05118'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('ALTER TABLE tags DROP CONSTRAINT uk_mac;')
    op.execute('ALTER TABLE tags ADD CONSTRAINT uk_mac UNIQUE (mac, type);')
    pass


def downgrade():
    op.execute('ALTER TABLE tags DROP CONSTRAINT uk_mac;')
    op.execute('ALTER TABLE tags ADD CONSTRAINT uk_mac UNIQUE (mac);')
    pass
