import pytest


@pytest.mark.parametrize("route", ["/api/users/me", "/api/users/1", "/api/tweets"])
def test_route_get_status(client, route):
    response = client.get(route, headers={"Api-key": "test"})
    assert response.status_code == 200


@pytest.mark.parametrize("route", ["/api/tweets/1/likes", "/api/users/2/follow"])
def test_route_delete_status(client, route):
    response = client.delete(route, headers={"Api-key": "test"})
    assert response.status_code == 200
    assert response.json == {"result": "true"}


@pytest.mark.parametrize("route", ["/api/users/2/follow", "/api/tweets/1/likes"])
def test_route_post_status(client, route):
    response = client.post(route, headers={"Api-key": "test"})
    assert response.status_code == 200
    assert response.json == {"result": "true"}


def test_route_post_status_for_tweet(client):
    tweet = {"tweet_data": "text", "tweet_media_ids": []}
    response = client.post("/api/tweets", json=tweet, headers={"Api-key": "test"})
    assert response.status_code == 200
    assert response.json == {"result": "true", "tweet_id": 2}


def test_route_delete_status_for_tweet(client):
    response = client.delete("/api/tweets/1", headers={"Api-key": "test"})
    assert response.status_code == 200
    assert response.json == {"result": "true"}
