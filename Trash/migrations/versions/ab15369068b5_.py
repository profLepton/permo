"""empty message

Revision ID: ab15369068b5
Revises: 1dfb2c836513
Create Date: 2022-11-30 02:00:45.611018

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab15369068b5'
down_revision = '1dfb2c836513'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pn_requests', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('message', sa.String(length=512), nullable=True))
        batch_op.add_column(sa.Column('class_name', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('course_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('professor_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('student_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('owner', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('permission_number', sa.Integer(), nullable=True))
        batch_op.create_index(batch_op.f('ix_pn_requests_class_name'), ['class_name'], unique=False)
        batch_op.create_index(batch_op.f('ix_pn_requests_course_id'), ['course_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_pn_requests_owner'), ['owner'], unique=False)
        batch_op.create_index(batch_op.f('ix_pn_requests_professor_id'), ['professor_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_pn_requests_status'), ['status'], unique=False)
        batch_op.create_index(batch_op.f('ix_pn_requests_student_id'), ['student_id'], unique=False)
        batch_op.create_foreign_key(None, 'user', ['owner'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pn_requests', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_index(batch_op.f('ix_pn_requests_student_id'))
        batch_op.drop_index(batch_op.f('ix_pn_requests_status'))
        batch_op.drop_index(batch_op.f('ix_pn_requests_professor_id'))
        batch_op.drop_index(batch_op.f('ix_pn_requests_owner'))
        batch_op.drop_index(batch_op.f('ix_pn_requests_course_id'))
        batch_op.drop_index(batch_op.f('ix_pn_requests_class_name'))
        batch_op.drop_column('permission_number')
        batch_op.drop_column('owner')
        batch_op.drop_column('student_id')
        batch_op.drop_column('professor_id')
        batch_op.drop_column('course_id')
        batch_op.drop_column('class_name')
        batch_op.drop_column('message')
        batch_op.drop_column('status')

    # ### end Alembic commands ###
