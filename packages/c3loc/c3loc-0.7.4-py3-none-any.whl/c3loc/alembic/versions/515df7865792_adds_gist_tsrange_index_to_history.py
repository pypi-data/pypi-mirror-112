"""Adds gist tsrange index to history

Revision ID: 515df7865792
Revises: dbe74359375f
Create Date: 2021-07-10 14:25:16.407379

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '515df7865792'
down_revision = 'dbe74359375f'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        'create index tsrange_idx on history '
        'using gist (tsrange(start_ts, end_ts))')


def downgrade():
    op.execute('drop index history.tsrange_idx')
