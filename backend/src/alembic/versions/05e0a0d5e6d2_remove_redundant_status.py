"""Remove redundant status

Revision ID: 05e0a0d5e6d2
Revises: 94572f7a47c9
Create Date: 2024-11-18 05:13:13.906779

"""
from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic_postgresql_enum import TableReference

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "05e0a0d5e6d2"
down_revision: Union[str, None] = "94572f7a47c9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.sync_enum_values(
        "public",
        "clothingitemstatus",
        ["PROCESSING", "FINISHED", "FAILED"],
        [
            TableReference(
                table_schema="public", table_name="clothingitem", column_name="status"
            )
        ],
        enum_values_to_rename=[],
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.sync_enum_values(
        "public",
        "clothingitemstatus",
        ["WAITING_FOR_FILE", "PROCESSING", "FINISHED", "FAILED"],
        [
            TableReference(
                table_schema="public", table_name="clothingitem", column_name="status"
            )
        ],
        enum_values_to_rename=[],
    )
    # ### end Alembic commands ###
