from aiohttp_session import get_session
from aiohttp_security.abc import AbstractAuthorizationPolicy
from aiohttp_security.abc import AbstractIdentityPolicy
from functools import namedtuple
import logging
from mwsdk import AIORightmanage_inner

User = namedtuple('User', ['user_id', 'user_name', 'systemuser','manageuser','manageuserid','companyid'])

class MWSessionIdentityPolicy(AbstractIdentityPolicy):
    '''
    提供session认证
    '''
    def __init__(self):
        super().__init__()

    async def identify(self, request):
        session = await get_session(request)
        # "uid": "2222", "uname": "dev", "systemuser": true, "manageuser": false, "manageuserid": null}
        current_user = User(user_id = session.get('uid'),
                            user_name = session.get('uname'),
                            systemuser=session.get('systemuser', False),
                            manageuser=session.get('manageuser', False),
                            manageuserid=session.get('manageuserid'),
                            companyid=session.get('companyid'))
        request['current_user'] = current_user
        return session.get('uid')

    async def remember(self, request, response, identity, **kwargs):
        # 不提供登入
        pass

    async def forget(self, request, response):
        # 不提供登出
        pass

class MWAuthorizationPolicy(AbstractAuthorizationPolicy):
    def __init__(self):
        super().__init__()
        self.systemname = None

    async def authorized_userid(self, identity):
        # identiy 为 user.uid
        return identity

    async def permits(self, identity, permission, context=None):
        '''
        调用权限服务，检测权限
        :param identity: user_id
        :param permission: subsystem，如：vehicle,fleet。。。
        :param context: ops，权限的操作，如：insert,delete...
        :return:
        '''
        if identity is None:
            return False
        assert context ,'context can not be null'
        assert self.systemname,'please assign systemname'
        rm = AIORightmanage_inner()
        _,permissions = await rm.permissions(self.systemname,identity)
        # permission为多个
        if isinstance(permission, str):
            subsystem3list = permission.split(',')
        elif isinstance(permission, list):
            subsystem3list = permission
        else:
            raise Exception(
                f'the subsystem{permission} is not support,example:"vehicle" or "vehicle,car" or ["vehicle","car"]')
        for subsystem3 in subsystem3list:
            permission_rm = permissions.get(subsystem3)
            if permission_rm is None:
                # 支持同时检测多个权限后，有些权限可能不会在当前项目中
                logging.warning(f'the permission({permission_rm}) is not exist in the system({self.systemname})')
                continue
                # raise Exception('the permission(%s) is not exist in the system(%s)' % (permission,self.systemname))
            ops = permission_rm.get('ops',[])
            if context in ops :
                return True
        return False

