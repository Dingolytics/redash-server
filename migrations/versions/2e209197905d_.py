"""empty message

Revision ID: 2e209197905d
Revises: 
Create Date: 2023-04-28 13:04:50.178682

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2e209197905d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('streams',
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('data_source_id', sa.Integer(), nullable=False),
    sa.Column('db_table', sa.String(length=255), nullable=False),
    sa.Column('db_create_query', sa.Text(), nullable=True),
    sa.Column('is_enabled', sa.Boolean(), nullable=False),
    sa.Column('is_archived', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['data_source_id'], ['data_sources.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('db_table')
    )
    with op.batch_alter_table('streams', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_streams_is_archived'), ['is_archived'], unique=False)
        batch_op.create_index(batch_op.f('ix_streams_is_enabled'), ['is_enabled'], unique=False)

    with op.batch_alter_table('events', schema=None) as batch_op:
        batch_op.alter_column('additional_properties',
               existing_type=postgresql.JSONB(astext_type=sa.Text()),
               nullable=False,
               existing_server_default=sa.text("'{}'::jsonb"))

    with op.batch_alter_table('organizations', schema=None) as batch_op:
        batch_op.alter_column('settings',
               existing_type=postgresql.JSONB(astext_type=sa.Text()),
               nullable=False,
               existing_server_default=sa.text("'{}'::jsonb"))

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('details',
               existing_type=postgresql.JSONB(astext_type=sa.Text()),
               nullable=False,
               existing_server_default=sa.text("'{}'::jsonb"))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('details',
               existing_type=postgresql.JSONB(astext_type=sa.Text()),
               nullable=True,
               existing_server_default=sa.text("'{}'::jsonb"))

    with op.batch_alter_table('organizations', schema=None) as batch_op:
        batch_op.alter_column('settings',
               existing_type=postgresql.JSONB(astext_type=sa.Text()),
               nullable=True,
               existing_server_default=sa.text("'{}'::jsonb"))

    with op.batch_alter_table('events', schema=None) as batch_op:
        batch_op.alter_column('additional_properties',
               existing_type=postgresql.JSONB(astext_type=sa.Text()),
               nullable=True,
               existing_server_default=sa.text("'{}'::jsonb"))

    with op.batch_alter_table('streams', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_streams_is_enabled'))
        batch_op.drop_index(batch_op.f('ix_streams_is_archived'))

    op.drop_table('streams')
    # ### end Alembic commands ###
