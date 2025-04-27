"""add users

Revision ID: a70538a94d14
Revises: c54a10947006
Create Date: 2025-04-27 16:11:46.276880

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



revision: str = "a70538a94d14"
down_revision: Union[str, None] = "c54a10947006"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("password", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )



def downgrade() -> None:

    op.drop_table("users")

