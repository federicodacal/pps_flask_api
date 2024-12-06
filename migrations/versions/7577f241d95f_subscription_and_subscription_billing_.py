"""subscription and subscription_billing tables

Revision ID: 7577f241d95f
Revises: 
Create Date: 2024-12-05 19:19:50.123140

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7577f241d95f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['email'])

    with op.batch_alter_table('users_details', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['username'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users_details', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    # ### end Alembic commands ###