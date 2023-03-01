"""empty message

Revision ID: 798a58dc98e3
Revises: 6594be44fddb
Create Date: 2023-03-01 13:44:41.790195

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '798a58dc98e3'
down_revision = '6594be44fddb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('patient', schema=None) as batch_op:
        batch_op.drop_index('ix_patient_id_series')
        batch_op.create_index(batch_op.f('ix_patient_id_series'), ['id_series'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('patient', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_patient_id_series'))
        batch_op.create_index('ix_patient_id_series', ['id_series'], unique=False)

    # ### end Alembic commands ###
