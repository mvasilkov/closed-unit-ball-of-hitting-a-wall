from django.contrib.auth.models import User

import pytest
import requests

from journal.models import Post
from test.test_api_auth import initialize_user, get_auth_token


@pytest.mark.django_db
def test_api_read_post(live_server):
    initialize_user()

    p = Post(user=User.objects.first(), path='hello-world', contents='# hello, world')
    p.save()

    Post(user=User.objects.first(), path='another-one', contents='# another one').save()

    token = get_auth_token(live_server)
    headers = {'Authorization': f'JWT {token}'}

    r = requests.get(f'{live_server}/api/posts/', headers=headers)
    assert r.status_code == 200
    res = r.json()
    assert len(res) == 2
    assert [post['path'] for post in res] == ['another-one', 'hello-world']

    r = requests.get(f'{live_server}/api/posts/{p.objectid}/', headers=headers)
    assert r.status_code == 200
    res = r.json()
    assert 'path' in res
    assert res['path'] == p.path
