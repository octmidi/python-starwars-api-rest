"""initial migration

Revision ID: 29ea4d0959d7
Revises: 
Create Date: 2023-12-22 17:48:30.270015

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '29ea4d0959d7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('peoples',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('url', sa.String(length=500), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('url')
    )
    op.create_table('planets',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('url', sa.String(length=500), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('name', name='planets_name_key'),
    sa.UniqueConstraint('url'),
    sa.UniqueConstraint('url', name='planets_url_key')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=80), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('email', name='user_email_key')
    )
    op.create_table('favorite_people',
    sa.Column('id_user', sa.Integer(), nullable=False),
    sa.Column('id_people', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['id_people'], ['peoples.id'], ),
    sa.ForeignKeyConstraint(['id_user'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id_people', 'id_user', name='favorite_people_pk')
    )
    op.create_table('favorite_planets',
    sa.Column('id_planet', sa.Integer(), nullable=False),
    sa.Column('id_user', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['id_planet'], ['planets.id'], ),
    sa.ForeignKeyConstraint(['id_user'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id_user', 'id_planet', name='favorite_planets_pk')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('favorite_planets')
    op.drop_table('favorite_people')
    op.drop_table('users')
    op.drop_table('planets')
    op.drop_table('peoples')
    # ### end Alembic commands ###
