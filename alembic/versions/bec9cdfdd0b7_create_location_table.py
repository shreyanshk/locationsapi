"""create location table

Revision ID: bec9cdfdd0b7
Revises:
Create Date: 2017-05-13 16:26:45.021708

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'bec9cdfdd0b7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "locationsTable",
        sa.Column("name", sa.String(50), primary_key = True),
        sa.Column("lat", sa.Float, nullable = False),
        sa.Column("lng", sa.Float, nullable = False),
    )

def downgrade():
    op.drop_table("locationsTable")
