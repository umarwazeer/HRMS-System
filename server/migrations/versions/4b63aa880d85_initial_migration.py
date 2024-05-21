"""Initial migration.

Revision ID: 4b63aa880d85
Revises: 2311a9cad5b9
Create Date: 2023-05-02 14:05:10.360782

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4b63aa880d85'
down_revision = '2311a9cad5b9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('employee', schema=None) as batch_op:
        batch_op.add_column(sa.Column('role', sa.String(length=400), nullable=False))
        batch_op.add_column(sa.Column('gender', sa.String(length=400), nullable=False))
        batch_op.add_column(sa.Column('phone', sa.Integer(), nullable=False))
        batch_op.alter_column('name',
               existing_type=mysql.VARCHAR(length=50),
               type_=sa.String(length=220),
               nullable=False)
        batch_op.alter_column('email',
               existing_type=mysql.VARCHAR(length=50),
               type_=sa.String(length=400),
               nullable=False)
        batch_op.create_unique_constraint(None, ['gender'])
        batch_op.create_unique_constraint(None, ['email'])
        batch_op.create_unique_constraint(None, ['phone'])
        batch_op.drop_column('salary')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('employee', schema=None) as batch_op:
        batch_op.add_column(sa.Column('salary', mysql.FLOAT(), nullable=True))
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('email',
               existing_type=sa.String(length=400),
               type_=mysql.VARCHAR(length=50),
               nullable=True)
        batch_op.alter_column('name',
               existing_type=sa.String(length=220),
               type_=mysql.VARCHAR(length=50),
               nullable=True)
        batch_op.drop_column('phone')
        batch_op.drop_column('gender')
        batch_op.drop_column('role')

    # ### end Alembic commands ###
