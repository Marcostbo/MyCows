"""empty message

Revision ID: f4ce36850eb2
Revises: 7db1bebc66c9
Create Date: 2023-11-06 17:54:12.352928

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4ce36850eb2'
down_revision = '7db1bebc66c9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('animal_vaccination', schema=None) as batch_op:
        batch_op.add_column(sa.Column('vaccinated_on', sa.Date(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('animal_vaccination', schema=None) as batch_op:
        batch_op.drop_column('vaccinated_on')

    # ### end Alembic commands ###