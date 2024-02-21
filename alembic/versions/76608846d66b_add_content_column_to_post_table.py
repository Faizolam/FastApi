"""add content column to post table

Revision ID: 76608846d66b
Revises: e6e9ec16f68f
Create Date: 2024-02-20 10:37:39.561180

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '76608846d66b'
down_revision: Union[str, None] = 'e6e9ec16f68f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
