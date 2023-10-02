"""create links table

Revision ID: 2a47c99beb01
Revises: 
Create Date: 2023-10-02 08:44:43.628348

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2a47c99beb01'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("links", sa.Column("link_id", sa.Integer, primary_key=True), 
                    sa.Column("link_url", sa.String, nullable=False),
                    sa.Column("category", sa.String, nullable=True))
    
    pass


def downgrade() -> None:
    op.drop_table("links")
    pass
