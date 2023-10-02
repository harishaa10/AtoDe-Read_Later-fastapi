"""create fkey for user_id in links table

Revision ID: cd9a02ecda58
Revises: 4f83db3cf474
Create Date: 2023-10-02 11:16:30.128511

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cd9a02ecda58'
down_revision: Union[str, None] = '4f83db3cf474'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("links", 
                  sa.Column("user_id", sa.Integer, sa.ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False))
    pass


def downgrade() -> None:
    op.drop_constraint("links_user_id_fkey", "links", type_="foreignkey")
    op.drop_column("links", "user_id")
    pass
