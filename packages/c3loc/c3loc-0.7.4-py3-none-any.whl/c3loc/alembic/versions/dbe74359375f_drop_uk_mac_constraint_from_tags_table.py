"""drop uk_mac constraint from tags table

Revision ID: dbe74359375f
Revises: 6b0896f05118
Create Date: 2021-05-29 06:16:17.197295

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = 'dbe74359375f'
down_revision = '6b0896f05118'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("ALTER TABLE tags DROP CONSTRAINT uk_mac")


def downgrade():
    op.execute("ALTER TABLE tags ADD CONSTRAINT uk_mac UNIQUE (mac)")
