"""empty message

Revision ID: 0be2f912239e
Revises: c92291292a65
Create Date: 2024-03-01 17:38:00.438953

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0be2f912239e'
down_revision = 'c92291292a65'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('review', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rating', sa.Integer(), nullable=False))
        batch_op.alter_column('text',
               existing_type=sa.VARCHAR(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('review', schema=None) as batch_op:
        batch_op.alter_column('text',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.drop_column('rating')

    # ### end Alembic commands ###
