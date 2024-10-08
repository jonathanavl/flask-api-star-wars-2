"""empty message

Revision ID: 87028a3113a0
Revises: 02092b5a4720
Create Date: 2024-09-26 12:29:05.964462

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87028a3113a0'
down_revision = '02092b5a4720'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('favorite_planet')
    op.drop_table('favorite_character')
    op.drop_table('favorite_vehicle')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favorite_vehicle',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('vehicle_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='favorite_vehicle_user_id_fkey'),
    sa.ForeignKeyConstraint(['vehicle_id'], ['vehicle.id'], name='favorite_vehicle_vehicle_id_fkey'),
    sa.PrimaryKeyConstraint('user_id', 'vehicle_id', name='favorite_vehicle_pkey')
    )
    op.create_table('favorite_character',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('character_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['character_id'], ['character.id'], name='favorite_character_character_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='favorite_character_user_id_fkey'),
    sa.PrimaryKeyConstraint('user_id', 'character_id', name='favorite_character_pkey')
    )
    op.create_table('favorite_planet',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('planet_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['planet_id'], ['planet.id'], name='favorite_planet_planet_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='favorite_planet_user_id_fkey'),
    sa.PrimaryKeyConstraint('user_id', 'planet_id', name='favorite_planet_pkey')
    )
    # ### end Alembic commands ###
