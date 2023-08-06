__all__ = ('User', 'Video', 'Dynamic', 'Comment', 'FavoriteList')



import collections
import math
import re
import requests
import retrying
import time
import warnings

from bs4 import BeautifulSoup

from ..util.session import session
from ..util.decorators import lazy_property



_Comment = collections.namedtuple('Comments', ('content', 'like', 'user_id', 'timestamp'))
_FavoriteList = collections.namedtuple('FavoriteList', ('id', 'title', 'number_of_media'))



class User:
    '''User model

    API:
        - property
            - videos: iterator
            - number_of_videos: int
            - followers: iterator
            - number_of_followers: int
            - followings: iterator
            - number_of_followings: int
            - dynamics: itertor, to be done
            + channels: NotImplementedError
            - favorites: NotImplementedError
            - number_of_favorites
            + bangumis: NotImplementedError
            + cinemas: NotImplementedError
            + tags: NotImplementedError
            - room: dict
        - function
            - set_info()
    '''

    _URL_VIDEO = 'https://api.bilibili.com/x/space/arc/search'
    _URL_FOLLOWER = 'https://api.bilibili.com/x/relation/followers'
    _URL_FOLLOWING = 'https://api.bilibili.com/x/relation/followings'
    _URL_LIVE = 'https://api.live.bilibili.com/room/v1/Room/getRoomInfoOld'

    def __init__(self, id, info=True):
        self.id = int(id)
        self.info = None
        info and self.set_info()


    def __repr__(self):
        if self.info:
            return f'<User("{self.info["name"]}") @ LV {self.info["level"]}>'
        else:
            return f'<User({self.id})>'


    @property
    def videos(self):
        '''Iterate all videos from user

        Example:
            >>> for video in user.videos:
            ...     print(video)
        '''
        url = self._URL_VIDEO
        count = self.number_of_videos
        keys1, key2 = ('data', 'list', 'vlist'), 'aid'
        for page in self._data(url, count, 30, 'pubdate', 'mid', keys1, key2):
            for id in page:
                yield Video(id, info=self.info is not None)


    @property
    def number_of_videos(self):
        '''Return the number of videos
        '''
        data = self._data_at(self._URL_VIDEO, 1, 30, 'pubdate', 'mid')
        return data['data']['page']['count']


    @property
    @session.required_login()
    def followers(self):
        '''Iterate all followers from user

        Example:
            >>> for follower in user.followers:
            ...     print(follower)
        '''
        url = self._URL_FOLLOWER
        count = self.number_of_followers
        keys1, key2 = ('data', 'list'), 'mid'
        for page in self._data(url, count, 20, 'desc', 'vmid', keys1, key2):
            for id in page:
                yield User(id, self.info is not None)


    @property
    def number_of_followers(self):
        '''Return the number of followers
        '''
        data = self._data_at(self._URL_FOLLOWER, 1, 20, 'desc', 'vmid')
        return data['data']['total']


    @property
    @session.required_login()
    def followings(self):
        '''Iterate all followings from user

        Example:
            >>> for following in user.followings:
            ...     print(following)
        '''
        url = self._URL_FOLLOWING
        keys1, key2 = ('data', 'list'), 'mid'
        count = self.number_of_followings
        for page in self._data(url, count, 20, 'desc', 'vmid', keys1, key2):
            for id in page:
                yield User(id, self.info is not None)


    @lazy_property
    def number_of_followings(self):
        '''Return the number of followings
        '''
        data = self._data_at(self._URL_FOLLOWING, 1, 20, 'desc', 'vmid')
        return data['data']['total']


    @property
    def dynamics(self):
        '''Iterable all dynamics
        '''
        # warnings.warn('Dynamics have complex types, to be done.', Warning)
        for dynamic in self._dynamics():
            desc = dynamic.pop('desc')
            yield Dynamic.from_args(
                id=desc['dynamic_id'], user_id=desc['uid'], view=desc['view'],
                repost=desc['repost'], number_of_comments=desc.get('comment'),
                like=desc['like'], timestamp=desc['timestamp'], others=desc,
            )


    @property
    def channels(self):
        '''
        References:
            - https://api.bilibili.com/x/space/channel/list?mid=354576498&guest=true
        '''
        raise NotImplementedError


    @property
    def favorites(self):
        '''
        References:
            - https://api.bilibili.com/x/v3/fav/folder/created/list-all?up_mid=354576498
            - https://api.bilibili.com/x/v3/fav/folder/collected/list?pn=1&ps=20&up_mid=354576498
        '''
        url = 'https://api.bilibili.com/x/v3/fav/folder/created/list-all'
        data = requests.get(url, params=dict(up_mid=self.id)).json()
        for favlist in data['data']['list']:
            yield FavoriteList(favlist['id'], favlist['title'], favlist['media_count'])


    @property
    def number_of_favorites(self):
        url = 'https://api.bilibili.com/x/v3/fav/folder/created/list-all'
        data = requests.get(url, params=dict(up_mid=self.id)).json()
        return len(data['data']['list'])


    @property
    def bangumis(self):
        '''追番

        References:
            - https://api.bilibili.com/x/space/bangumi/follow/list?type=1&follow_status=0&pn=1&ps=15&vmid=354576498&ts=1586024234675
        '''
        raise NotImplementedError


    @property
    def cinemas(self):
        '''追剧

        References:
            - https://api.bilibili.com/x/space/bangumi/follow/list?type=2&follow_status=0&pn=1&ps=15&vmid=354576498&ts=1586024297034
        '''
        raise NotImplementedError


    @property
    def tags(self):
        '''订阅标签

        References:
            - https://space.bilibili.com/ajax/tags/getSubList?mid=354576498
        '''
        raise NotImplementedError


    @lazy_property
    def room(self):
        response = session.requests.get(self._URL_LIVE, params=dict(mid=self.id))
        return response.json()['data']


    def set_info(self):
        '''Set information of current user
        '''
        if not self.info:
            self.info = self._find_info()


    def _data(self, url, count, ps, order, id_name, keys1, key2):
        page_number = math.ceil(count/ps)
        f, g = self._ids_at, self._data_at
        return (
            f(g(url, page+1, ps, order, id_name), keys1, key2)
                for page in range(page_number)
        )


    def _data_at(self, url, page, ps, order, id_name):
        params = dict(ps=ps, pn=page, order=order)
        params[id_name] = self.id
        response = session.session.get(url, params=params)
        return response.json()


    def _ids_at(self, data, keys1, key2):
        try:
            for key in keys1:
                data = data[key]
            for video in data:
                if isinstance(key2, str):
                    yield video[key2]
                else:
                    yield tuple(video[k] for k in key2)
        except KeyError:
            warnings.warn('Unauthenticated access cannot get more information, ' \
                'please login by selenium.', Warning)
            return None


    def _dynamics(self):
        url = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history'
        params = dict(host_uid=self.id, offset_dynamic_id=0)
        while True:
            response = requests.get(url, params=params)  # do not use `session.session`
            data = response.json()['data']
            yield from data['cards']
            if not data['has_more']:
                break
            params['offset_dynamic_id'] = data['next_offset']


    def _find_info(self):
        info = dict()
        # account info
        params = dict(mid=self.id, jsonp='jsonp')
        url = 'https://api.bilibili.com/x/space/acc/info'
        response = session.session.get(url, params=params)
        data = response.json().get('data')
        for key in ('name', 'sex', 'face', 'sign', 'level', 'birthday'):
            info[key] = data.get(key)
        # up status
        url = 'https://api.bilibili.com/x/space/upstat'
        response = session.session.get(url, params=params)
        data = response.json().get('data')
        info['archive_view'] = data.get('archive').get('view')
        info['article_view'] = data.get('article').get('view')
        info['likes'] = data.get('likes')
        # relation status
        params = dict(vmid=self.id, jsonp='jsonp')
        url = 'https://api.bilibili.com/x/relation/stat'
        response = session.session.get(url, params=params)
        data = response.json().get('data')
        info['following'] = data.get('following')
        info['follower'] = data.get('follower')
        # return value
        return info



class Video:
    '''Video model

    API:
        - property
            - comments, iterator
            - tags, iterator
        - function
            - set_info()
    '''

    def __init__(self, id, info=True):
        self.id = int(id)
        self._timestamp = int(1000*time.time())
        self.info = None
        info and self.set_info()


    def __repr__(self):
        if self.info:
            return f'<Video({self.info["title"]}) @ {self.info["view"]}>'
        else:
            return f'<Video({self.id})>'


    @property
    def comments(self):
        '''
        Example:
            >>> for comment in video.comments:
            ...     print(comment)
        '''
        yield from Comment.from_args(self.id)


    @property
    def tags(self):
        # https://www.bilibili.com/v/channel/{tag_id}
        url = f'https://www.bilibili.com/video/av{self.id}'
        pattern = re.compile(r'\d+')
        soup = BeautifulSoup(session.requests.get(url).content, 'lxml')
        for tag in soup.find(class_='tag-area').find_all(class_='tag'):
            btns = tag.find(class_='channel-btns')
            yield dict(
                id=int(pattern.findall(btns.find('a').attrs['href'])[0]),
                title=tag.find(class_='channel-title').text.strip(),
                description=tuple(x.text for x in tag.find(class_='channel-desc').children),
                subscribe=btns.find('div').text.strip(),
            )


    def danmaku(self, date=time.strftime('%Y-%m-%d')):
        warnings.warn('Please login first.', Warning)

        def report(oid, dmid, reason, content=''):
            '''
            1：违法违禁，2：色情低俗，3：赌博诈骗，4：人身攻击，5：侵犯隐私，6：垃圾广告
            7：引战，8：剧透，9：恶意刷屏，10：视频无关，11：其它，12：青少年不良信息
            '''
            url = 'https://api.bilibili.com/x/dm/report/add'
            data = dict(cid=oid, dmid=dmid, reason=reason, csrf=session.session.cookies['bili_jct'])
            response = session.session.post(url, data=data, headers=dict(referer='https://www.bilibili.com'))
            return response.json()['code'] == 0

        try:
            oid = next(
                re.finditer(r'(?<=cid=)\d+', requests.get(f'https://bilibili.com/av{self.id}').text)
            ).group()
        except:
            return
        url = 'https://api.bilibili.com/x/v2/dm/history'
        params = dict(type=1, oid=oid, date=date)
        soup = BeautifulSoup(session.session.get(url, params=params).content, 'lxml')
        for danmaku in soup.find_all('d'):
            data = danmaku.attrs['p'].split(',')
            f = lambda reason=2, content='': report(oid, data[-1], reason, content)
            f.__doc__ = report.__doc__
            yield dict(content=danmaku.text, data=data, report=f)


    def set_info(self):
        if not self.info:
            self.info = self._find_info()


    def _find_info(self):
        info = dict()
        # video info
        url = 'https://api.bilibili.com/x/web-interface/view'
        response = session.session.get(url, params=dict(aid=self.id))
        data = response.json().get('data')
        if data is None:
            print('访问权限不足，需要登录。')
            raise PermissionError
        for key in ('pic', 'title', 'pubdate', 'desc', 'duration'):
            info[key] = data.get(key)
        info['owner'] = data['owner']['mid']
        # stat info
        stat = data['stat']
        for key in ('view', 'danmaku', 'reply', 'favorite', 'coin', 'share', 'like'):
            info[key] = stat.get(key)
        return info



class Dynamic:
    '''Dynamic model

    API:
        - property
            - comments, iterator
            - number_of_comments, int
        - function
            - set_info()
    '''

    def __init__(self, id, info=True):
        self.id = int(id)
        info and self.set_info()


    def __repr__(self):
        view = getattr(self, 'view', 'None')
        return f'<Dynamic({self.id} @ View {view})>'


    @classmethod
    def from_args(cls, id, **kwargs):
        self = cls(id, False)
        keys = ('user_id', 'view', 'repost', 'number_of_comments', 'like', 'timestamp')
        for key in keys:
            setattr(self, key, kwargs.get(key, None))
        self.others = kwargs.get('others', None)
        return self


    @property
    def comments(self):
        yield from Comment.from_args(self.id, type=17)


    def set_info(self):
        url = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail'
        params = dict(dynamic_id=self.id)
        data = requests.get(url, params=params).json()['data']['card']['desc']
        keys = ('view', 'repost', 'like', 'timestamp')
        for key in keys:
            setattr(self, key, data.get(key, None))
        self.number_of_comments = data['comment']



class Comment(_Comment):
    '''Comment model
    '''

    @classmethod
    def from_args(cls, id, type=1):
        for page in cls._comments(id, type):
            yield from page

    @classmethod
    @retrying.retry(stop_max_attempt_number=5)
    def _comments(cls, id, type=1, timestamp=None, ps=10, sort=2):
        timestamp = timestamp or int(time.time())
        first_page = cls._comments_data_at(id, 1, timestamp, 0, ps, sort, type)
        if first_page['data']:
            page_info = first_page['data']['page']
            page_number = math.ceil(page_info['count']/page_info['size'])
            f, g = cls._find_comments, cls._comments_data_at
            return (
                f(
                    g(id, page+1, timestamp, 0, ps, sort, type)['data']['replies'],
                    id, timestamp, ps, sort, type
                ) for page in range(page_number))
        return list(list())


    @classmethod
    def _comments_data_at(cls, id, page, timestap, root, ps, sort, type):
        url = 'https://api.bilibili.com/x/v2/reply'
        params = dict(pn=page, type=type, oid=id, sort=sort, _=timestap)
        if root:
            url += '/reply'
            params.update(dict(root=root, ps=ps))
        return session.session.get(url, params=params).json()


    @classmethod
    def _find_comments(cls, replies, id, timestamp, ps, sort, type):
        if replies:
            for reply in replies:
                message = reply['content']['message']
                mid = int(reply['member']['mid'])
                ctime = reply['ctime']
                like = reply['like']
                yield cls(message, like, mid, ctime)
                rcount = reply['rcount']
                if rcount:
                    for page in range(math.ceil(rcount/ps)):
                        rpid = reply['rpid']
                        data = cls._comments_data_at(id, page+1, timestamp, rpid, ps, sort, type)
                        replies = data['data']['replies']
                        yield from cls._find_comments(replies, id, timestamp, ps, sort, type)



class FavoriteList(_FavoriteList):
    '''Favorite list mode

    API:
        - value
            - id
            - title
            - number_of_media
        - property
            - info
            - videos
    '''

    @lazy_property
    def info(self):
        info = self._data_at(1)['info']
        cnt_info = info['cnt_info']
        return dict(
            cover=info['cover'], time=info['ctime'],
            collect=cnt_info['collect'], play=cnt_info['play'],
            like=cnt_info['thumb_up'], share=cnt_info['share'],
        )


    @property
    def videos(self):
        ps = 20
        pages = math.ceil(self.number_of_media / ps)
        for page in range(pages):
            data = self._data_at(page, ps)['medias']
            for video in data:
                yield Video(video['id'], info=False)


    def _data_at(self, page, ps=20):
        url = 'https://api.bilibili.com/x/v3/fav/resource/list'
        params = dict(media_id=self.id, pn=page, ps=ps)
        return requests.get(url, params=params).json()['data']



if __name__ == '__main__':
    u = User(546195)
    v = next(u.videos)
    c = next(v.comments)
    fer = next(u.followers)
    fing = next(u.followings)

    print('User:', u)
    print('Video:', v)
    print('Comment:', c)
    print('Follower:', fer)
    print('Following:', fing)
