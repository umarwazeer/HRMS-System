"""empty message

Revision ID: 72b1d9166587
Revises: c43a96d490db
Create Date: 2023-05-29 02:20:23.427595

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '72b1d9166587'
down_revision = 'c43a96d490db'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('attandence', schema=None) as batch_op:
        batch_op.drop_constraint('attandence_ibfk_3', type_='foreignkey')
        batch_op.drop_column('emp_id')

    with op.batch_alter_table('employee', schema=None) as batch_op:
        batch_op.add_column(sa.Column('dep_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'department', ['dep_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('employee', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('dep_id')

    with op.batch_alter_table('attandence', schema=None) as batch_op:
        batch_op.add_column(sa.Column('emp_id', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('attandence_ibfk_3', 'employee', ['emp_id'], ['id'])

    # ### end Alembic commands ###
