"""Fix table name

Revision ID: 2248aa5011fa
Revises: 64321a2e9f88
Create Date: 2024-04-28 00:07:48.526041

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2248aa5011fa'
down_revision = '64321a2e9f88'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('payroll', schema=None) as batch_op:
        batch_op.add_column(sa.Column('deductions', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('payroll', schema=None) as batch_op:
        batch_op.drop_column('deductions')

    # ### end Alembic commands ###
