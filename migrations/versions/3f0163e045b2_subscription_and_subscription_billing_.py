"""subscription and subscription_billing tables

Revision ID: 3f0163e045b2
Revises: 7577f241d95f
Create Date: 2024-12-05 19:21:41.562648

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f0163e045b2'
down_revision = '7577f241d95f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('subscriptions',
    sa.Column('ID', sa.String(length=50), nullable=False),
    sa.Column('type', sa.String(length=25), nullable=False),
    sa.Column('renewal_time_in_days', sa.Integer(), nullable=False),
    sa.Column('revenue_percentage', sa.Float(), nullable=False),
    sa.Column('monthly_price', sa.Float(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('modified_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('ID')
    )
    op.create_table('subscriptions_billings',
    sa.Column('ID', sa.String(length=50), nullable=False),
    sa.Column('account_ID', sa.String(length=50), nullable=False),
    sa.Column('subscription_ID', sa.String(length=50), nullable=False),
    sa.Column('state', sa.String(length=50), nullable=False),
    sa.Column('last_payment_date', sa.DateTime(), nullable=True),
    sa.Column('next_payment_date', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('modified_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['account_ID'], ['accounts.ID'], ),
    sa.ForeignKeyConstraint(['subscription_ID'], ['subscriptions.ID'], ),
    sa.PrimaryKeyConstraint('ID')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('subscriptions_billings')
    op.drop_table('subscriptions')
    # ### end Alembic commands ###
