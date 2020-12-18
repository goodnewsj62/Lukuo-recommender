"""empty message

Revision ID: 4cd27cd8de47
Revises: 
Create Date: 2020-12-14 16:29:10.220694

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4cd27cd8de47'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('movie',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=30), nullable=False),
    sa.Column('homepage', sa.String(length=30), nullable=False),
    sa.Column('cast', sa.String(length=100), nullable=False),
    sa.Column('crew', sa.String(length=300), nullable=False),
    sa.Column('release_date', sa.String(length=20), nullable=False),
    sa.Column('original_language', sa.String(length=10), nullable=False),
    sa.Column('production_countries', sa.String(length=30), nullable=False),
    sa.Column('tagline', sa.String(length=30), nullable=False),
    sa.Column('genres', sa.String(length=100), nullable=False),
    sa.Column('overview', sa.String(length=100), nullable=False),
    sa.Column('director', sa.String(length=30), nullable=False),
    sa.Column('vote_count', sa.Integer(), nullable=False),
    sa.Column('vote_average', sa.Float(), nullable=False),
    sa.Column('keywords', sa.String(length=50), nullable=False),
    sa.Column('soup', sa.String(length=100), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('music',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('song_id', sa.String(length=30), nullable=False),
    sa.Column('title', sa.String(length=30), nullable=False),
    sa.Column('release', sa.String(length=30), nullable=False),
    sa.Column('artist_name', sa.String(length=30), nullable=False),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('genres', sa.String(length=30), nullable=False),
    sa.Column('url', sa.String(length=30), nullable=False),
    sa.Column('producer', sa.String(length=30), nullable=False),
    sa.Column('label', sa.String(length=30), nullable=False),
    sa.Column('date', sa.String(length=30), nullable=False),
    sa.Column('country', sa.String(length=30), nullable=False),
    sa.Column('languages', sa.String(length=30), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('vote_count', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=30), nullable=False),
    sa.Column('email', sa.String(length=30), nullable=False),
    sa.Column('password', sa.String(length=50), nullable=False),
    sa.Column('genre_a', sa.String(length=20), nullable=False),
    sa.Column('genre_b', sa.String(length=20), nullable=False),
    sa.Column('genre_c', sa.String(length=20), nullable=False),
    sa.Column('genre_d', sa.String(length=20), nullable=False),
    sa.Column('genre_e', sa.String(length=20), nullable=False),
    sa.Column('genre_f', sa.String(length=20), nullable=False),
    sa.Column('genre_g', sa.String(length=20), nullable=False),
    sa.Column('genre_h', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('userinfo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.String(length=40), nullable=False),
    sa.Column('song_id', sa.String(length=30), nullable=False),
    sa.Column('listen_count', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('association',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('movie_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['movie_id'], ['movie.id'], ondelete='cascade'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('user_id', 'movie_id')
    )
    op.create_table('music_association',
    sa.Column('users', sa.Integer(), nullable=False),
    sa.Column('music_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['music_id'], ['music.id'], ondelete='cascade'),
    sa.ForeignKeyConstraint(['users'], ['user.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('users', 'music_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('music_association')
    op.drop_table('association')
    op.drop_table('userinfo')
    op.drop_table('user')
    op.drop_table('music')
    op.drop_table('movie')
    # ### end Alembic commands ###
