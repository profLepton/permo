"""empty message

Revision ID: 1dfb2c836513
Revises: d1b1f11fe898
Create Date: 2022-11-30 00:22:57.765542

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1dfb2c836513'
down_revision = 'd1b1f11fe898'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pn_requests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('requests', schema=None) as batch_op:
        batch_op.drop_index('ix_requests_class_name')
        batch_op.drop_index('ix_requests_course_id')
        batch_op.drop_index('ix_requests_owner')
        batch_op.drop_index('ix_requests_professor_id')
        batch_op.drop_index('ix_requests_status')
        batch_op.drop_index('ix_requests_student_id')

    op.drop_table('requests')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('requests',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('status', sa.BOOLEAN(), nullable=True),
    sa.Column('class_name', sa.VARCHAR(length=64), nullable=True),
    sa.Column('course_id', sa.INTEGER(), nullable=True),
    sa.Column('professor_id', sa.INTEGER(), nullable=True),
    sa.Column('student_id', sa.INTEGER(), nullable=True),
    sa.Column('owner', sa.INTEGER(), nullable=True),
    sa.Column('permission_number', sa.INTEGER(), nullable=True),
    sa.Column('date', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['owner'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('requests', schema=None) as batch_op:
        batch_op.create_index('ix_requests_student_id', ['student_id'], unique=False)
        batch_op.create_index('ix_requests_status', ['status'], unique=False)
        batch_op.create_index('ix_requests_professor_id', ['professor_id'], unique=False)
        batch_op.create_index('ix_requests_owner', ['owner'], unique=False)
        batch_op.create_index('ix_requests_course_id', ['course_id'], unique=False)
        batch_op.create_index('ix_requests_class_name', ['class_name'], unique=False)

    op.drop_table('pn_requests')
    # ### end Alembic commands ###