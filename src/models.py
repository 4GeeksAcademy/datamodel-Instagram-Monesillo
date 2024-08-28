import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Table, DateTime,datetime , Boolean, Text
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

followers_table = Table('followers', Base.metadata,
    Column('follower_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('followed_id', Integer, ForeignKey('users.id'), primary_key=True)
)

# Usuario
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    posts = relationship('Post', back_populates='user')
    comments = relationship('Comment', back_populates='user')
    likes = relationship('Like', back_populates='user')
    stories = relationship('Story', back_populates='user')
    followed = relationship(
        'User',
        secondary=followers_table,
        primaryjoin=(followers_table.c.follower_id == id),
        secondaryjoin=(followers_table.c.followed_id == id),
        back_populates='followers'
    )
    followers = relationship(
        'User',
        secondary=followers_table,
        primaryjoin=(followers_table.c.followed_id == id),
        secondaryjoin=(followers_table.c.follower_id == id),
        back_populates='followed'
    )

# Publicación
class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True)
    image_url = Column(String, nullable=False)  # URL de la imagen
    description = Column(Text)
    timestamp = Column(DateTime, default= datetime.datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='posts')
    comments = relationship('Comment', back_populates='post')
    likes = relationship('Like', back_populates='post')

# Historia
class Story(Base):
    __tablename__ = 'stories'
    
    id = Column(Integer, primary_key=True)
    image_url = Column(String, nullable=False)  # URL de la imagen o video
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    is_active = Column(Boolean, default=True)  # Indica si la historia está activa (no ha expirado)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='stories')

# Comentario
class Comment(Base):
    __tablename__ = 'comments'
    
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))
    user = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')

# Me gusta
class Like(Base):
    __tablename__ = 'likes'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))
    user = relationship('User', back_populates='likes')
    post = relationship('Post', back_populates='likes')
## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
