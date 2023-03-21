"""empty message

Revision ID: 1a5c5151c315
Revises: 41bbdd669e37
Create Date: 2023-03-21 13:28:48.388744

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a5c5151c315'
down_revision = '41bbdd669e37'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('allergy', schema=None) as batch_op:
        batch_op.drop_index('ix_allergy_name')

    op.drop_table('allergy')
    with op.batch_alter_table('chronic_disease', schema=None) as batch_op:
        batch_op.drop_index('ix_chronic_disease_name')

    op.drop_table('chronic_disease')
    op.drop_table('smoker')
    with op.batch_alter_table('drug', schema=None) as batch_op:
        batch_op.drop_index('ix_drug_name')

    op.drop_table('drug')
    with op.batch_alter_table('doctor', schema=None) as batch_op:
        batch_op.drop_index('ix_doctor_address')
        batch_op.drop_index('ix_doctor_assistants_schedule')
        batch_op.drop_index('ix_doctor_birth_date')
        batch_op.drop_index('ix_doctor_city')
        batch_op.drop_index('ix_doctor_consultation_schedule_away')
        batch_op.drop_index('ix_doctor_consultation_schedule_office')
        batch_op.drop_index('ix_doctor_email')
        batch_op.drop_index('ix_doctor_first_name')
        batch_op.drop_index('ix_doctor_gender')
        batch_op.drop_index('ix_doctor_last_name')
        batch_op.drop_index('ix_doctor_password_hash')
        batch_op.drop_index('ix_doctor_phone_number')
        batch_op.drop_index('ix_doctor_postalcode')
        batch_op.drop_index('ix_doctor_state')
        batch_op.drop_index('ix_doctor_username')

    op.drop_table('doctor')
    op.drop_table('information_sheet_chronic_disease')
    with op.batch_alter_table('consultation', schema=None) as batch_op:
        batch_op.drop_index('ix_consultation_date_time')
        batch_op.drop_index('ix_consultation_urgency_grade')

    op.drop_table('consultation')
    with op.batch_alter_table('patient', schema=None) as batch_op:
        batch_op.drop_index('ix_patient_address')
        batch_op.drop_index('ix_patient_birth_date')
        batch_op.drop_index('ix_patient_city')
        batch_op.drop_index('ix_patient_email')
        batch_op.drop_index('ix_patient_first_name')
        batch_op.drop_index('ix_patient_gender')
        batch_op.drop_index('ix_patient_last_name')
        batch_op.drop_index('ix_patient_marital_status')
        batch_op.drop_index('ix_patient_occupation')
        batch_op.drop_index('ix_patient_passport_id')
        batch_op.drop_index('ix_patient_password_hash')
        batch_op.drop_index('ix_patient_phone_number')
        batch_op.drop_index('ix_patient_postalcode')
        batch_op.drop_index('ix_patient_state')
        batch_op.drop_index('ix_patient_transfer')
        batch_op.drop_index('ix_patient_username')

    op.drop_table('patient')
    op.drop_table('family_history')
    op.drop_table('drinker')
    op.drop_table('brother')
    with op.batch_alter_table('invite_code', schema=None) as batch_op:
        batch_op.drop_index('ix_invite_code_doctor_id')
        batch_op.drop_index('ix_invite_code_id')
        batch_op.drop_index('ix_invite_code_patient_id')

    op.drop_table('invite_code')
    with op.batch_alter_table('information_sheet', schema=None) as batch_op:
        batch_op.drop_index('ix_information_sheet_blood_type')
        batch_op.drop_index('ix_information_sheet_height')
        batch_op.drop_index('ix_information_sheet_shoe_size')
        batch_op.drop_index('ix_information_sheet_weight')

    op.drop_table('information_sheet')
    op.drop_table('mother')
    op.drop_table('father')
    op.drop_table('information_sheet_allergy')
    op.drop_table('hospitalization')
    op.drop_table('sister')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sister',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('patient_id', sa.INTEGER(), nullable=True),
    sa.Column('death_age', sa.INTEGER(), nullable=True),
    sa.Column('cause', sa.VARCHAR(length=256), nullable=False),
    sa.ForeignKeyConstraint(['patient_id'], ['family_history.patient_id'], name='fk_sister_patient_id_family_history'),
    sa.PrimaryKeyConstraint('id', name='pk_sister')
    )
    op.create_table('hospitalization',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('patient_id', sa.INTEGER(), nullable=True),
    sa.Column('date', sa.DATE(), nullable=True),
    sa.Column('reason', sa.VARCHAR(length=500), nullable=True),
    sa.ForeignKeyConstraint(['patient_id'], ['information_sheet.patient_id'], name='fk_hospitalization_patient_id_information_sheet'),
    sa.PrimaryKeyConstraint('id', name='pk_hospitalization')
    )
    op.create_table('information_sheet_allergy',
    sa.Column('patient_id', sa.INTEGER(), nullable=True),
    sa.Column('allergy_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['allergy_id'], ['allergy.id'], name='fk_information_sheet_allergy_allergy_id_allergy'),
    sa.ForeignKeyConstraint(['patient_id'], ['information_sheet.patient_id'], name='fk_information_sheet_allergy_patient_id_information_sheet')
    )
    op.create_table('father',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('patient_id', sa.INTEGER(), nullable=True),
    sa.Column('death_age', sa.INTEGER(), nullable=True),
    sa.Column('cause', sa.VARCHAR(length=256), nullable=False),
    sa.ForeignKeyConstraint(['patient_id'], ['family_history.patient_id'], name='fk_father_patient_id_family_history'),
    sa.PrimaryKeyConstraint('id', name='pk_father')
    )
    op.create_table('mother',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('patient_id', sa.INTEGER(), nullable=True),
    sa.Column('death_age', sa.INTEGER(), nullable=True),
    sa.Column('cause', sa.VARCHAR(length=256), nullable=False),
    sa.ForeignKeyConstraint(['patient_id'], ['family_history.patient_id'], name='fk_mother_patient_id_family_history'),
    sa.PrimaryKeyConstraint('id', name='pk_mother')
    )
    op.create_table('information_sheet',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('patient_id', sa.INTEGER(), nullable=True),
    sa.Column('weight', sa.INTEGER(), nullable=True),
    sa.Column('height', sa.INTEGER(), nullable=True),
    sa.Column('shoe_size', sa.INTEGER(), nullable=True),
    sa.Column('blood_type', sa.VARCHAR(length=256), nullable=True),
    sa.ForeignKeyConstraint(['patient_id'], ['patient.id'], name='fk_information_sheet_patient_id_patient'),
    sa.PrimaryKeyConstraint('id', name='pk_information_sheet')
    )
    with op.batch_alter_table('information_sheet', schema=None) as batch_op:
        batch_op.create_index('ix_information_sheet_weight', ['weight'], unique=False)
        batch_op.create_index('ix_information_sheet_shoe_size', ['shoe_size'], unique=False)
        batch_op.create_index('ix_information_sheet_height', ['height'], unique=False)
        batch_op.create_index('ix_information_sheet_blood_type', ['blood_type'], unique=False)

    op.create_table('invite_code',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('invite_code', sa.INTEGER(), nullable=True),
    sa.Column('patient_id', sa.INTEGER(), nullable=True),
    sa.Column('doctor_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['doctor_id'], ['doctor.id'], name='fk_invite_code_doctor_id_doctor'),
    sa.ForeignKeyConstraint(['patient_id'], ['patient.id'], name='fk_invite_code_patient_id_patient'),
    sa.PrimaryKeyConstraint('id', name='pk_invite_code')
    )
    with op.batch_alter_table('invite_code', schema=None) as batch_op:
        batch_op.create_index('ix_invite_code_patient_id', ['patient_id'], unique=False)
        batch_op.create_index('ix_invite_code_id', ['id'], unique=False)
        batch_op.create_index('ix_invite_code_doctor_id', ['doctor_id'], unique=False)

    op.create_table('brother',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('patient_id', sa.INTEGER(), nullable=True),
    sa.Column('death_age', sa.INTEGER(), nullable=True),
    sa.Column('cause', sa.VARCHAR(length=256), nullable=False),
    sa.ForeignKeyConstraint(['patient_id'], ['family_history.patient_id'], name='fk_brother_patient_id_family_history'),
    sa.PrimaryKeyConstraint('id', name='pk_brother')
    )
    op.create_table('drinker',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('patient_id', sa.INTEGER(), nullable=True),
    sa.Column('quantity', sa.INTEGER(), nullable=True),
    sa.Column('frequency', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['patient_id'], ['information_sheet.patient_id'], name='fk_drinker_patient_id_information_sheet'),
    sa.PrimaryKeyConstraint('id', name='pk_drinker')
    )
    op.create_table('family_history',
    sa.Column('patient_id', sa.INTEGER(), nullable=False),
    sa.Column('heart_disease', sa.VARCHAR(length=256), nullable=False),
    sa.Column('diabetes', sa.VARCHAR(length=256), nullable=False),
    sa.Column('high_blood_pressure', sa.VARCHAR(length=256), nullable=False),
    sa.Column('stroke', sa.VARCHAR(length=256), nullable=False),
    sa.Column('varicose_veins', sa.VARCHAR(length=256), nullable=False),
    sa.Column('gout', sa.VARCHAR(length=256), nullable=False),
    sa.Column('arthritis', sa.VARCHAR(length=256), nullable=False),
    sa.Column('neuropathy', sa.VARCHAR(length=256), nullable=False),
    sa.Column('bleeding_disorder', sa.VARCHAR(length=256), nullable=False),
    sa.Column('foot_problems', sa.VARCHAR(length=256), nullable=False),
    sa.ForeignKeyConstraint(['patient_id'], ['information_sheet.patient_id'], name='fk_family_history_patient_id_information_sheet'),
    sa.PrimaryKeyConstraint('patient_id', name='pk_family_history')
    )
    op.create_table('patient',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(length=64), nullable=True),
    sa.Column('first_name', sa.VARCHAR(length=64), nullable=True),
    sa.Column('last_name', sa.VARCHAR(length=64), nullable=True),
    sa.Column('phone_number', sa.INTEGER(), nullable=True),
    sa.Column('email', sa.VARCHAR(length=128), nullable=True),
    sa.Column('address', sa.VARCHAR(length=256), nullable=True),
    sa.Column('postalcode', sa.VARCHAR(length=256), nullable=True),
    sa.Column('city', sa.VARCHAR(length=256), nullable=True),
    sa.Column('state', sa.VARCHAR(length=256), nullable=True),
    sa.Column('passport_id', sa.VARCHAR(length=16), nullable=True),
    sa.Column('birth_date', sa.VARCHAR(length=128), nullable=True),
    sa.Column('marital_status', sa.VARCHAR(length=16), nullable=True),
    sa.Column('gender', sa.VARCHAR(length=8), nullable=True),
    sa.Column('occupation', sa.VARCHAR(length=256), nullable=True),
    sa.Column('password_hash', sa.VARCHAR(length=256), nullable=True),
    sa.Column('doctor_id', sa.INTEGER(), nullable=True),
    sa.Column('transfer', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['doctor_id'], ['doctor.id'], name='fk_patient_doctor_id_doctor'),
    sa.PrimaryKeyConstraint('id', name='pk_patient')
    )
    with op.batch_alter_table('patient', schema=None) as batch_op:
        batch_op.create_index('ix_patient_username', ['username'], unique=False)
        batch_op.create_index('ix_patient_transfer', ['transfer'], unique=False)
        batch_op.create_index('ix_patient_state', ['state'], unique=False)
        batch_op.create_index('ix_patient_postalcode', ['postalcode'], unique=False)
        batch_op.create_index('ix_patient_phone_number', ['phone_number'], unique=False)
        batch_op.create_index('ix_patient_password_hash', ['password_hash'], unique=False)
        batch_op.create_index('ix_patient_passport_id', ['passport_id'], unique=False)
        batch_op.create_index('ix_patient_occupation', ['occupation'], unique=False)
        batch_op.create_index('ix_patient_marital_status', ['marital_status'], unique=False)
        batch_op.create_index('ix_patient_last_name', ['last_name'], unique=False)
        batch_op.create_index('ix_patient_gender', ['gender'], unique=False)
        batch_op.create_index('ix_patient_first_name', ['first_name'], unique=False)
        batch_op.create_index('ix_patient_email', ['email'], unique=False)
        batch_op.create_index('ix_patient_city', ['city'], unique=False)
        batch_op.create_index('ix_patient_birth_date', ['birth_date'], unique=False)
        batch_op.create_index('ix_patient_address', ['address'], unique=False)

    op.create_table('consultation',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('patient_id', sa.INTEGER(), nullable=True),
    sa.Column('doctor_id', sa.INTEGER(), nullable=True),
    sa.Column('date_time', sa.DATETIME(), nullable=True),
    sa.Column('pdf', sa.VARCHAR(length=128), nullable=True),
    sa.Column('urgency_grade', sa.VARCHAR(length=128), nullable=True),
    sa.ForeignKeyConstraint(['doctor_id'], ['doctor.id'], name='fk_consultation_doctor_id_doctor'),
    sa.ForeignKeyConstraint(['patient_id'], ['patient.id'], name='fk_consultation_patient_id_patient'),
    sa.PrimaryKeyConstraint('id', name='pk_consultation')
    )
    with op.batch_alter_table('consultation', schema=None) as batch_op:
        batch_op.create_index('ix_consultation_urgency_grade', ['urgency_grade'], unique=False)
        batch_op.create_index('ix_consultation_date_time', ['date_time'], unique=False)

    op.create_table('information_sheet_chronic_disease',
    sa.Column('patient_id', sa.INTEGER(), nullable=True),
    sa.Column('chronic_disease_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['chronic_disease_id'], ['chronic_disease.id'], name='fk_information_sheet_chronic_disease_chronic_disease_id_chronic_disease'),
    sa.ForeignKeyConstraint(['patient_id'], ['information_sheet.patient_id'], name='fk_information_sheet_chronic_disease_patient_id_information_sheet')
    )
    op.create_table('doctor',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(length=64), nullable=True),
    sa.Column('first_name', sa.VARCHAR(length=64), nullable=True),
    sa.Column('last_name', sa.VARCHAR(length=64), nullable=True),
    sa.Column('phone_number', sa.INTEGER(), nullable=True),
    sa.Column('email', sa.VARCHAR(length=128), nullable=True),
    sa.Column('address', sa.VARCHAR(length=256), nullable=True),
    sa.Column('postalcode', sa.VARCHAR(length=256), nullable=True),
    sa.Column('city', sa.VARCHAR(length=256), nullable=True),
    sa.Column('state', sa.VARCHAR(length=256), nullable=True),
    sa.Column('birth_date', sa.VARCHAR(length=128), nullable=True),
    sa.Column('gender', sa.VARCHAR(length=8), nullable=True),
    sa.Column('consultation_schedule_office', sa.VARCHAR(length=128), nullable=True),
    sa.Column('consultation_schedule_away', sa.VARCHAR(length=128), nullable=True),
    sa.Column('assistants_schedule', sa.VARCHAR(length=128), nullable=True),
    sa.Column('password_hash', sa.VARCHAR(length=256), nullable=True),
    sa.Column('medical_proof', sa.VARCHAR(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id', name='pk_doctor')
    )
    with op.batch_alter_table('doctor', schema=None) as batch_op:
        batch_op.create_index('ix_doctor_username', ['username'], unique=False)
        batch_op.create_index('ix_doctor_state', ['state'], unique=False)
        batch_op.create_index('ix_doctor_postalcode', ['postalcode'], unique=False)
        batch_op.create_index('ix_doctor_phone_number', ['phone_number'], unique=False)
        batch_op.create_index('ix_doctor_password_hash', ['password_hash'], unique=False)
        batch_op.create_index('ix_doctor_last_name', ['last_name'], unique=False)
        batch_op.create_index('ix_doctor_gender', ['gender'], unique=False)
        batch_op.create_index('ix_doctor_first_name', ['first_name'], unique=False)
        batch_op.create_index('ix_doctor_email', ['email'], unique=False)
        batch_op.create_index('ix_doctor_consultation_schedule_office', ['consultation_schedule_office'], unique=False)
        batch_op.create_index('ix_doctor_consultation_schedule_away', ['consultation_schedule_away'], unique=False)
        batch_op.create_index('ix_doctor_city', ['city'], unique=False)
        batch_op.create_index('ix_doctor_birth_date', ['birth_date'], unique=False)
        batch_op.create_index('ix_doctor_assistants_schedule', ['assistants_schedule'], unique=False)
        batch_op.create_index('ix_doctor_address', ['address'], unique=False)

    op.create_table('drug',
    sa.Column('patient_id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=256), nullable=True),
    sa.Column('dosage', sa.VARCHAR(length=256), nullable=True),
    sa.Column('frequency', sa.VARCHAR(length=256), nullable=True),
    sa.ForeignKeyConstraint(['patient_id'], ['information_sheet.patient_id'], name='fk_drug_patient_id_information_sheet'),
    sa.PrimaryKeyConstraint('patient_id', name='pk_drug')
    )
    with op.batch_alter_table('drug', schema=None) as batch_op:
        batch_op.create_index('ix_drug_name', ['name'], unique=False)

    op.create_table('smoker',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('patient_id', sa.INTEGER(), nullable=True),
    sa.Column('current_packs_per_day', sa.INTEGER(), nullable=True),
    sa.Column('previous_pack_per_day', sa.INTEGER(), nullable=True),
    sa.Column('smoking_years', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['patient_id'], ['information_sheet.patient_id'], name='fk_smoker_patient_id_information_sheet'),
    sa.PrimaryKeyConstraint('id', name='pk_smoker')
    )
    op.create_table('chronic_disease',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id', name='pk_chronic_disease')
    )
    with op.batch_alter_table('chronic_disease', schema=None) as batch_op:
        batch_op.create_index('ix_chronic_disease_name', ['name'], unique=False)

    op.create_table('allergy',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id', name='pk_allergy')
    )
    with op.batch_alter_table('allergy', schema=None) as batch_op:
        batch_op.create_index('ix_allergy_name', ['name'], unique=False)

    # ### end Alembic commands ###