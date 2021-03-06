"""empty message

Revision ID: 563ba2335746
Revises: 
Create Date: 2020-06-11 16:33:18.410419

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '563ba2335746'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('goals',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('goal_badge', sa.String(length=15), nullable=False),
    sa.Column('goal_name', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('requests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('phone', sa.String(), nullable=False),
    sa.Column('time', sa.String(), nullable=False),
    sa.Column('goal', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tutors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('about', sa.Text(), nullable=False),
    sa.Column('rating', sa.Float(), nullable=False),
    sa.Column('picture', sa.String(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('free', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bookings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('phone', sa.String(), nullable=False),
    sa.Column('day', sa.String(), nullable=False),
    sa.Column('time', sa.String(), nullable=False),
    sa.Column('tutor_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['tutor_id'], ['tutors.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tutors_goals',
    sa.Column('tutor_id', sa.Integer(), nullable=True),
    sa.Column('goal_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['goal_id'], ['goals.id'], ),
    sa.ForeignKeyConstraint(['tutor_id'], ['tutors.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tutors_goals')
    op.drop_table('bookings')
    op.drop_table('tutors')
    op.drop_table('requests')
    op.drop_table('goals')
    # ### end Alembic commands ###
