"""initial

Revision ID: cf2f13bb0616
Revises: f71568834d16
Create Date: 2023-04-21 10:35:34.446637

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf2f13bb0616'
down_revision = 'f71568834d16'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contest_report',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('id_contest', sa.Integer(), nullable=False),
    sa.Column('id_task', sa.Integer(), nullable=False),
    sa.Column('id_user', sa.Integer(), nullable=False),
    sa.Column('id_team', sa.Integer(), nullable=False),
    sa.Column('id_answer', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_answer'], ['answer.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('contest_report')
    # ### end Alembic commands ###
