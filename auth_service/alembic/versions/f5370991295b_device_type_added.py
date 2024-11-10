"""device_type_added

Revision ID: f5370991295b
Revises: 0bedb03692bc
Create Date: 2024-09-25 19:19:27.014505

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f5370991295b'
down_revision: Union[str, None] = '0bedb03692bc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_social_accounts',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('provider', sa.String(length=50), nullable=False),
    sa.Column('provider_user_id', sa.String(length=255), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=True),
    sa.Column('fullname', sa.String(length=255), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('provider_user_id')
    )
    op.create_unique_constraint(None, 'roles', ['id'])
    op.add_column('user_login_history', sa.Column('user_device_type', sa.Text(), nullable=True))
    op.create_unique_constraint(None, 'user_roles', ['id'])
    op.add_column('users', sa.Column('email', sa.String(length=255), nullable=True))
    op.alter_column('users', 'password',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.create_unique_constraint(None, 'users', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.alter_column('users', 'password',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.drop_column('users', 'email')
    op.drop_constraint(None, 'user_roles', type_='unique')
    op.drop_column('user_login_history', 'user_device_type')
    op.drop_constraint(None, 'roles', type_='unique')
    op.drop_table('user_social_accounts')
    # ### end Alembic commands ###
