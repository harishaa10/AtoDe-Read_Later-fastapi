"""create users table

Revision ID: 4f83db3cf474
Revises: 2a47c99beb01
Create Date: 2023-10-02 11:11:55.033145

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4f83db3cf474'
down_revision: Union[str, None] = '2a47c99beb01'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users", 
                    sa.Column("user_id", sa.Integer, primary_key=True, index=True),
                    sa.Column("email", sa.String, unique=True, nullable=False),
                    sa.Column("password", sa.String, nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default= sa.text('now()')))
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
