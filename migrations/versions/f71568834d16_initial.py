"""initial

Revision ID: f71568834d16
Revises: 
Create Date: 2023-04-20 18:54:45.420619

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = 'f71568834d16'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('task',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('time_work', sa.Integer(), nullable=False),
    sa.Column('size_raw', sa.Integer(), nullable=False),
    sa.Column('type_input', sa.Integer(), nullable=False, default=1),
    sa.Column('type_output', sa.Integer(), nullable=False, default=1),
    sa.Column('path_files', sa.String(), nullable=False),
    sa.Column('number_shipments', sa.Integer(), nullable=False, default=100),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('type_compilation',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name_compilation', sa.String(), nullable=True),
    sa.Column('path_compilation', sa.String(), nullable=True),
    sa.Column('path_commands', sa.String(), nullable=True),
    sa.Column('extension', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('answer',
    sa.Column('date_send', sa.DateTime(), nullable=False, default=datetime.now()),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('id_team', sa.Integer(), nullable=True, default=0),
    sa.Column('id_user', sa.Integer(), nullable=True),
    sa.Column('id_task', sa.Integer(), nullable=True),
    sa.Column('id_contest', sa.Integer(), nullable=True),
    sa.Column('type_compiler', sa.Integer(), nullable=True),
    sa.Column('total', sa.String(), nullable=False, default="-"),
    sa.Column('time', sa.String(), nullable=False, default="-"),
    sa.Column('memory_size', sa.Float(), nullable=False, default=0),
    sa.Column('number_test', sa.Integer(), nullable=False, default=0),
    sa.Column('points', sa.Integer(), nullable=False, default=0),
    sa.Column('path_report_file', sa.String(), nullable=False, default="None"),
    sa.Column('path_programme_file', sa.String(), nullable=False),
    sa.Column('is_completed', sa.Boolean(), nullable=True, default=False),
    sa.ForeignKeyConstraint(['id_task'], ['task.id'], ),
    sa.ForeignKeyConstraint(['type_compiler'], ['type_compilation.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('answer')
    op.drop_table('type_compilation')
    op.drop_table('task')
    # ### end Alembic commands ###
