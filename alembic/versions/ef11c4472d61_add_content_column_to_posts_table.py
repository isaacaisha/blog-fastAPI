"""add content column to posts table

Revision ID: ef11c4472d61
Revises: e05067135bed
Create Date: 2024-02-18 16:13:25.157696

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ef11c4472d61'
down_revision: Union[str, None] = 'e05067135bed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_colum("posts", "content")
    pass
