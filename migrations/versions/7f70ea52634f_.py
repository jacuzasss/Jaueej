"""empty message

Revision ID: 7f70ea52634f
Revises: aa5eed55ef06
Create Date: 2019-01-10 14:43:36.805369

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f70ea52634f'
down_revision = 'aa5eed55ef06'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('email',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('server', sa.String(length=128), nullable=True),
    sa.Column('port', sa.Integer(), nullable=True),
    sa.Column('username', sa.String(length=128), nullable=True),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.Column('outgoing_email', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('email')
    # ### end Alembic commands ###
