"""Fix table name

Revision ID: f212aff658d2
Revises: 0d42a8a5d153
Create Date: 2024-04-27 23:42:11.365856

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f212aff658d2'
down_revision = '0d42a8a5d153'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('payroll', schema=None) as batch_op:
        batch_op.add_column(sa.Column('deductions', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('payroll_period', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('payroll_cycle', sa.String(length=100), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('payroll', schema=None) as batch_op:
        batch_op.drop_column('payroll_cycle')
        batch_op.drop_column('payroll_period')
        batch_op.drop_column('deductions')

    # ### end Alembic commands ###
