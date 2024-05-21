"""empty message

Revision ID: 6d14c3fb7ba1
Revises: 2ffd70c341a4
Create Date: 2023-06-08 11:27:05.070739

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d14c3fb7ba1'
down_revision = '2ffd70c341a4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('employee', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_by', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('updated_by', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'user', ['updated_by'], ['id'])
        batch_op.create_foreign_key(None, 'user', ['created_by'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('employee', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('updated_by')
        batch_op.drop_column('created_by')

    # ### end Alembic commands ###
