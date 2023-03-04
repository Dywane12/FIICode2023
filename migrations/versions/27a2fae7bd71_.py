"""empty message

Revision ID: 27a2fae7bd71
Revises: 5462a7a16f28
Create Date: 2023-03-04 14:07:58.171608

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '27a2fae7bd71'
down_revision = '5462a7a16f28'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('doctor', schema=None) as batch_op:
        batch_op.drop_index('ix_doctor_address')
        batch_op.drop_index('ix_doctor_assistants_schedule')
        batch_op.drop_index('ix_doctor_birth_date')
        batch_op.drop_index('ix_doctor_consultation_schedule_away')
        batch_op.drop_index('ix_doctor_consultation_schedule_office')
        batch_op.drop_index('ix_doctor_email')
        batch_op.drop_index('ix_doctor_first_name')
        batch_op.drop_index('ix_doctor_gender')
        batch_op.drop_index('ix_doctor_last_name')
        batch_op.drop_index('ix_doctor_password_hash')
        batch_op.drop_index('ix_doctor_phone_number')
        batch_op.drop_index('ix_doctor_username')

    op.drop_table('doctor')
    with op.batch_alter_table('patient', schema=None) as batch_op:
        batch_op.drop_index('ix_patient_address')
        batch_op.drop_index('ix_patient_birth_date')
        batch_op.drop_index('ix_patient_cnp')
        batch_op.drop_index('ix_patient_email')
        batch_op.drop_index('ix_patient_first_name')
        batch_op.drop_index('ix_patient_gender')
        batch_op.drop_index('ix_patient_id_number')
        batch_op.drop_index('ix_patient_id_series')
        batch_op.drop_index('ix_patient_last_name')
        batch_op.drop_index('ix_patient_marital_status')
        batch_op.drop_index('ix_patient_medical_record_id')
        batch_op.drop_index('ix_patient_password_hash')
        batch_op.drop_index('ix_patient_phone_number')
        batch_op.drop_index('ix_patient_username')

    op.drop_table('patient')
    with op.batch_alter_table('consultation', schema=None) as batch_op:
        batch_op.drop_index('ix_consultation_id')
        batch_op.drop_index('ix_consultation_time')

    op.drop_table('consultation')
    with op.batch_alter_table('medical_record', schema=None) as batch_op:
        batch_op.drop_index('ix_medical_record_id')

    op.drop_table('medical_record')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('medical_record',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('pdf', sa.VARCHAR(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id', name='pk_medical_record'),
    sa.UniqueConstraint('pdf', name='uq_medical_record_pdf')
    )
    with op.batch_alter_table('medical_record', schema=None) as batch_op:
        batch_op.create_index('ix_medical_record_id', ['id'], unique=False)

    op.create_table('consultation',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('patient_id', sa.INTEGER(), nullable=False),
    sa.Column('doctor_id', sa.INTEGER(), nullable=False),
    sa.Column('time', sa.VARCHAR(length=128), nullable=False),
    sa.Column('pdf', sa.VARCHAR(length=128), nullable=True),
    sa.ForeignKeyConstraint(['doctor_id'], ['doctor.id'], name='fk_consultation_doctor_id_doctor'),
    sa.ForeignKeyConstraint(['patient_id'], ['patient.id'], name='fk_consultation_patient_id_patient'),
    sa.PrimaryKeyConstraint('id', name='pk_consultation')
    )
    with op.batch_alter_table('consultation', schema=None) as batch_op:
        batch_op.create_index('ix_consultation_time', ['time'], unique=False)
        batch_op.create_index('ix_consultation_id', ['id'], unique=False)

    op.create_table('patient',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(length=64), nullable=False),
    sa.Column('first_name', sa.VARCHAR(length=64), nullable=False),
    sa.Column('last_name', sa.VARCHAR(length=64), nullable=False),
    sa.Column('phone_number', sa.INTEGER(), nullable=False),
    sa.Column('email', sa.VARCHAR(length=128), nullable=False),
    sa.Column('address', sa.VARCHAR(length=256), nullable=False),
    sa.Column('id_series', sa.VARCHAR(length=8), nullable=False),
    sa.Column('id_number', sa.VARCHAR(length=16), nullable=False),
    sa.Column('cnp', sa.INTEGER(), nullable=False),
    sa.Column('birth_date', sa.VARCHAR(length=128), nullable=False),
    sa.Column('marital_status', sa.VARCHAR(length=16), nullable=False),
    sa.Column('gender', sa.VARCHAR(length=8), nullable=False),
    sa.Column('medical_record_id', sa.INTEGER(), nullable=False),
    sa.Column('password_hash', sa.VARCHAR(length=256), nullable=False),
    sa.Column('doctor_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['doctor_id'], ['doctor.id'], name='fk_patient_doctor_id_doctor'),
    sa.PrimaryKeyConstraint('id', name='pk_patient')
    )
    with op.batch_alter_table('patient', schema=None) as batch_op:
        batch_op.create_index('ix_patient_username', ['username'], unique=False)
        batch_op.create_index('ix_patient_phone_number', ['phone_number'], unique=False)
        batch_op.create_index('ix_patient_password_hash', ['password_hash'], unique=False)
        batch_op.create_index('ix_patient_medical_record_id', ['medical_record_id'], unique=False)
        batch_op.create_index('ix_patient_marital_status', ['marital_status'], unique=False)
        batch_op.create_index('ix_patient_last_name', ['last_name'], unique=False)
        batch_op.create_index('ix_patient_id_series', ['id_series'], unique=False)
        batch_op.create_index('ix_patient_id_number', ['id_number'], unique=False)
        batch_op.create_index('ix_patient_gender', ['gender'], unique=False)
        batch_op.create_index('ix_patient_first_name', ['first_name'], unique=False)
        batch_op.create_index('ix_patient_email', ['email'], unique=False)
        batch_op.create_index('ix_patient_cnp', ['cnp'], unique=False)
        batch_op.create_index('ix_patient_birth_date', ['birth_date'], unique=False)
        batch_op.create_index('ix_patient_address', ['address'], unique=False)

    op.create_table('doctor',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(length=64), nullable=False),
    sa.Column('first_name', sa.VARCHAR(length=64), nullable=False),
    sa.Column('last_name', sa.VARCHAR(length=64), nullable=False),
    sa.Column('phone_number', sa.INTEGER(), nullable=False),
    sa.Column('email', sa.VARCHAR(length=128), nullable=False),
    sa.Column('address', sa.VARCHAR(length=256), nullable=False),
    sa.Column('birth_date', sa.VARCHAR(length=128), nullable=False),
    sa.Column('gender', sa.VARCHAR(length=8), nullable=False),
    sa.Column('consultation_schedule_office', sa.VARCHAR(length=128), nullable=False),
    sa.Column('consultation_schedule_away', sa.VARCHAR(length=128), nullable=False),
    sa.Column('assistants_schedule', sa.VARCHAR(length=128), nullable=True),
    sa.Column('password_hash', sa.VARCHAR(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id', name='pk_doctor')
    )
    with op.batch_alter_table('doctor', schema=None) as batch_op:
        batch_op.create_index('ix_doctor_username', ['username'], unique=False)
        batch_op.create_index('ix_doctor_phone_number', ['phone_number'], unique=False)
        batch_op.create_index('ix_doctor_password_hash', ['password_hash'], unique=False)
        batch_op.create_index('ix_doctor_last_name', ['last_name'], unique=False)
        batch_op.create_index('ix_doctor_gender', ['gender'], unique=False)
        batch_op.create_index('ix_doctor_first_name', ['first_name'], unique=False)
        batch_op.create_index('ix_doctor_email', ['email'], unique=False)
        batch_op.create_index('ix_doctor_consultation_schedule_office', ['consultation_schedule_office'], unique=False)
        batch_op.create_index('ix_doctor_consultation_schedule_away', ['consultation_schedule_away'], unique=False)
        batch_op.create_index('ix_doctor_birth_date', ['birth_date'], unique=False)
        batch_op.create_index('ix_doctor_assistants_schedule', ['assistants_schedule'], unique=False)
        batch_op.create_index('ix_doctor_address', ['address'], unique=False)

    # ### end Alembic commands ###
