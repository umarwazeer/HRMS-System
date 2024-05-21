"""Initial migration.

Revision ID: 513ef13925b4
Revises: 6d14c3fb7ba1
Create Date: 2023-07-08 13:07:28.880953

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '513ef13925b4'
down_revision = '6d14c3fb7ba1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('my_user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index('email')

    op.drop_table('user')
    with op.batch_alter_table('attandence', schema=None) as batch_op:
        batch_op.add_column(sa.Column('emp_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'employee', ['emp_id'], ['id'])

    with op.batch_alter_table('employee', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_by', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('updated_by', sa.Integer(), nullable=True))
        batch_op.drop_constraint('employee_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'my_user', ['updated_by'], ['id'])
        batch_op.create_foreign_key(None, 'my_user', ['created_by'], ['id'])
        batch_op.drop_column('image')
        batch_op.drop_column('dep_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('employee', schema=None) as batch_op:
        batch_op.add_column(sa.Column('dep_id', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('image', mysql.VARCHAR(length=100), nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('employee_ibfk_1', 'department', ['dep_id'], ['id'])
        batch_op.drop_column('updated_by')
        batch_op.drop_column('created_by')

    with op.batch_alter_table('attandence', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('emp_id')

    op.create_table('user',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=220), nullable=False),
    sa.Column('email', mysql.VARCHAR(length=400), nullable=False),
    sa.Column('dep', mysql.VARCHAR(length=400), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index('email', ['email'], unique=False)

    op.drop_table('my_user')
    # ### end Alembic commands ###