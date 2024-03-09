from typing import Any, Dict, List, Optional

from .database import Base, engine, session
from .models import Column, Followers, Like, Media, Tweet, User


def start():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    objects = [
        User(name="test", email="test@test.ru", token="test"),
        User(name="test1", email="test1@test.ru", token="test1"),
        Tweet(text="text", author_id=2),
        Followers(user_id=1, follower_id=2),
        Followers(user_id=2, follower_id=1),
    ]
    session.bulk_save_objects(objects)
    session.commit()


def get_user_by_word(word: str) -> Dict[str, Any]:
    if word.isdigit():
        user = session.query(User).where(User.id == word).one()
    else:
        user = session.query(User).where(User.token == word).one()

    return {
        "id": user.id,
        "name": user.name,
        "followers": [u.to_json() for u in user.followers],
        "following": [u.to_json() for u in user.following],
    }


def follow(user_id: str, token: str) -> Dict[str, Any]:
    user_follower = session.query(User).where(User.token == token).one()
    new_follow = Followers(user_id=user_id, follower_id=user_follower.id)

    session.add(new_follow)
    session.commit()

    return new_follow


def unfollow(user_id: str, token: str) -> Dict[str, Any]:
    user_follower = session.query(User).where(User.token == token).one()
    follow = (
        session.query(Followers)
        .where(
            Followers.follower_id == user_follower.id and Followers.user_id == user_id
        )
        .one()
    )

    session.delete(follow)
    session.commit()
    return follow


def add_media(file_path: str) -> Column[int]:
    new_path = "/images" + file_path.split("/static/images")[-1]
    new_media = Media(url=new_path)

    session.add(new_media)
    session.commit()

    return new_media.id


def get_tweets(token: str) -> List[Dict[str, Any]]:
    user: Optional[User] = session.query(User).filter_by(token=token).first()
    if user:
        following_users = [follower.user_id for follower in user.following]

        feed = []
        for user_id in following_users:
            tweets = session.query(Tweet).filter_by(author_id=user_id).all()
            feed.extend(tweets)

        sorted_feed = sorted(feed, key=lambda tweet: len(tweet.likes), reverse=True)

        formatted_feed = []
        for tweet in sorted_feed:
            attachments = [media.url for media in tweet.media] if tweet.media else []
            likes = [
                {"user_id": like.user.id, "name": like.user.name}
                for like in tweet.likes
            ]
            formatted_tweet = {
                "id": tweet.id,
                "content": tweet.text,
                "attachments": attachments,
                "author": {"id": tweet.author.id, "name": tweet.author.name},
                "likes": likes,
            }
            formatted_feed.append(formatted_tweet)

        return formatted_feed

    return [{}]


def add_tweet(token: str, data: Optional[Dict]) -> Optional[Column[int]]:
    user: Optional[User] = session.query(User).filter_by(token=token).first()

    if user and data:
        tweet_data = data.get("tweet_data")
        tweet_media_ids = data.get("tweet_media_ids")

        new_tweet = Tweet(text=tweet_data, author_id=user.id)
        session.add(new_tweet)
        session.commit()

        tweet_id = new_tweet.id

        if tweet_media_ids:
            for media_id in tweet_media_ids:
                media = session.query(Media).get(media_id)
                if media:
                    media.tweet_id = tweet_id
                    session.add(media)

        session.commit()

        return tweet_id

    return None


def delete_tweet(token: str, tweet_id: str) -> Dict[str, Any]:
    user: Optional[User] = session.query(User).filter_by(token=token).first()
    if user:
        tweet = (
            session.query(Tweet)
            .where(Tweet.id == tweet_id and Tweet.author_id == user.id)
            .one()
        )

        session.delete(tweet)
        session.commit()

        return tweet

    return {}


def like(token: str, tweet_id: str) -> Dict[str, Any]:
    user: Optional[User] = session.query(User).filter_by(token=token).first()
    if user:
        new_like = Like(user_id=user.id, tweet_id=tweet_id)

        session.add(new_like)
        session.commit()

        return new_like

    return {}


def unlike(token: str, tweet_id: str) -> Optional[Like]:
    user: Optional[User] = session.query(User).filter_by(token=token).first()
    if user:
        like: Optional[Like] = (
            session.query(Like)
            .where(Like.user_id == user.id and Like.tweet_id == tweet_id)
            .first()
        )

        session.delete(like)
        session.commit()

        return like
    return None
