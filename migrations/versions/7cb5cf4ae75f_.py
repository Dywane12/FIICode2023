"""empty message

Revision ID: 7cb5cf4ae75f
Revises: 798a58dc98e3
Create Date: 2023-03-01 13:47:45.206230

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7cb5cf4ae75f'
down_revision = '798a58dc98e3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('consultation', schema=None) as batch_op:
        batch_op.drop_index('ix_consultation_time')
        batch_op.create_index(batch_op.f('ix_consultation_time'), ['time'], unique=False)

    with op.batch_alter_table('patient', schema=None) as batch_op:
        batch_op.drop_index('ix_patient_cnp')
        batch_op.create_index(batch_op.f('ix_patient_cnp'), ['cnp'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('patient', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_patient_cnp'))
        batch_op.create_index('ix_patient_cnp', ['cnp'], unique=False)

    with op.batch_alter_table('consultation', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_consultation_time'))
        batch_op.create_index('ix_consultation_time', ['time'], unique=False)

    # ### end Alembic commands ###
