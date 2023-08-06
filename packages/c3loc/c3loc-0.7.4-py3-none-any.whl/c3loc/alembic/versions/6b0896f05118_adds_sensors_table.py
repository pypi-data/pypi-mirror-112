"""Adds sensors table

Revision ID: 6b0896f05118
Revises: 5eae6a0253f5
Create Date: 2021-05-03 15:29:54.558118

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '6b0896f05118'
down_revision = '5eae6a0253f5'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """CREATE TABLE sensors
(
    id     serial,
    tag_id int,
    type   int,
    value  bytea,
    ts     timestamp without time zone DEFAULT (now() at time zone 'utc'),
    device_ts integer,
    PRIMARY KEY (id),
    CONSTRAINT fk_tags
        FOREIGN KEY (tag_id)
            REFERENCES tags (id) ON DELETE CASCADE)""")


def downgrade():
    op.execute('DROP TABLE sensors')
