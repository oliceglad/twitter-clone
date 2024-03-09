from typing import Any, Dict

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    token = Column(
        String,
        nullable=False,
    )

    tweets = relationship("Tweet", back_populates="author")
    following = relationship(
        "Followers", foreign_keys="Followers.follower_id", back_populates="follower"
    )
    followers = relationship(
        "Followers", foreign_keys="Followers.user_id", back_populates="user"
    )
    likes = relationship("Like")

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Tweet(Base):
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("User", back_populates="tweets")
    media = relationship("Media", uselist=True, back_populates="tweet")
    likes = relationship("Like")

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    tweet_id = Column(Integer, ForeignKey("tweets.id"))

    user = relationship("User", foreign_keys=[user_id], back_populates="likes")

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Followers(Base):
    __tablename__ = "followers"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    follower_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", foreign_keys=[user_id], back_populates="followers")
    follower = relationship(
        "User", foreign_keys=[follower_id], back_populates="following"
    )

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Media(Base):
    __tablename__ = "medias"

    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    tweet_id = Column(Integer, ForeignKey("tweets.id"))

    tweet = relationship("Tweet", back_populates="media")

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
