"""Fix table name

Revision ID: cb21f26e5dbd
Revises: 2f5854ac3039
Create Date: 2024-04-22 17:39:14.725212

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'cb21f26e5dbd'
down_revision = '2f5854ac3039'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('leave',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('leave_type', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('on_date', sa.Date(), nullable=False),
    sa.Column('from_date', sa.Date(), nullable=False),
    sa.Column('to_date', sa.Date(), nullable=False),
    sa.Column('emp_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['emp_id'], ['employee.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('attendance', schema=None) as batch_op:
        batch_op.add_column(sa.Column('check_in_time', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('check_out_time', sa.DateTime(), nullable=True))
        batch_op.alter_column('date',
               existing_type=mysql.VARCHAR(length=100),
               type_=sa.Date(),
               existing_nullable=False)
        batch_op.drop_index('id_UNIQUE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('attendance', schema=None) as batch_op:
        batch_op.create_index('id_UNIQUE', ['id'], unique=False)
        batch_op.alter_column('date',
               existing_type=sa.Date(),
               type_=mysql.VARCHAR(length=100),
               existing_nullable=False)
        batch_op.drop_column('check_out_time')
        batch_op.drop_column('check_in_time')

    op.drop_table('leave')
    # ### end Alembic commands ###