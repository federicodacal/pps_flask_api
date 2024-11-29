"""email y username como unique

Revision ID: 362d06c1153c
Revises: e7f35af4a73d
Create Date: 2024-11-28 22:39:33.347112

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '362d06c1153c'
down_revision = 'e7f35af4a73d'
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
