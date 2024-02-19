"""add users table

Revision ID: c069a5ad24ff
Revises: ef11c4472d61
Create Date: 2024-02-18 16:58:39.316980

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c069a5ad24ff'
down_revision: Union[str, None] = 'ef11c4472d61'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table("users",
                    sa.Column("id", sa.Integer(), nullable=False),
                    sa.Column("email", sa.String(), nullable=False),
                    sa.Column("password", sa.String(), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True),
                              server_default=sa.text("now()"), nullable=False),
                              sa.PrimaryKeyConstraint("id"),
                              sa.UniqueConstraint("email"))
    pass


def downgrade():
    op.drop_table("users")
    pass
