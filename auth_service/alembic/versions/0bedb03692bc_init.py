"""init

Revision ID: 0bedb03692bc
Revises:
Create Date: 2024-09-02 21:16:55.169877

"""
from typing import Sequence, Union
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '0bedb03692bc'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
                    sa.Column('name', sa.String(length=50), nullable=False),
                    sa.Column('description', sa.String(length=255), nullable=True),
                    sa.Column('permissions', sa.ARRAY(sa.String()), nullable=False),
                    sa.Column('id', sa.UUID(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('id'),
                    sa.UniqueConstraint('name')
                    )
    op.create_table('users',
                    sa.Column('login', sa.String(length=255), nullable=False),
                    sa.Column('password', sa.String(length=255), nullable=False),
                    sa.Column('first_name', sa.String(length=50), nullable=True),
                    sa.Column('last_name', sa.String(length=50), nullable=True),
                    sa.Column('is_active', sa.Boolean(), nullable=True),
                    sa.Column('is_superuser', sa.Boolean(), nullable=True),
                    sa.Column('id', sa.UUID(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('id'),
                    sa.UniqueConstraint('login')
                    )
    op.create_table('user_login_history',
                    sa.Column('user_id', sa.UUID(), nullable=False),
                    sa.Column('login_time', sa.DateTime(), nullable=False),
                    sa.Column('user_agent', sa.String(length=255), nullable=True),
                    sa.Column('ip_address', sa.String(length=45), nullable=True),
                    sa.Column('id', sa.UUID(), nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('id')
                    )
    op.create_table('user_roles',
                    sa.Column('user_id', sa.UUID(), nullable=False),
                    sa.Column('role_id', sa.UUID(), nullable=False),
                    sa.Column('id', sa.UUID(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_roles')
    op.drop_table('user_login_history')
    op.drop_table('users')
    op.drop_table('roles')
    # ### end Alembic commands ###
