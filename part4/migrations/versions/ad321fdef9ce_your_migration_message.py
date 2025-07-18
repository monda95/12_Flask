"""Your migration message

Revision ID: ad321fdef9ce
Revises: 
Create Date: 2025-07-16 15:50:44.398072

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ad321fdef9ce'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=mysql.VARCHAR(length=100),
               type_=sa.String(length=30),
               nullable=False)
        batch_op.alter_column('email',
               existing_type=mysql.VARCHAR(length=100),
               nullable=False)
        batch_op.create_unique_constraint(None, ['email'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('email',
               existing_type=mysql.VARCHAR(length=100),
               nullable=True)
        batch_op.alter_column('name',
               existing_type=sa.String(length=30),
               type_=mysql.VARCHAR(length=100),
               nullable=True)

    # ### end Alembic commands ###
