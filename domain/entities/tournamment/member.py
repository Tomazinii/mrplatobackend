

from domain.entities.user import User
from domain.entities.tournamment import Group


class Member:
    boss: bool
    user: User
    group: Group
    online: bool

    def __init__(self, boss, user, group, online):
        self.boss = boss
        self.user = user
        self.group = group
        self.online = online
        
    @staticmethod
    def create(boss: bool, user: User, group: Group, online: bool):
        if isinstance(user,User) and isinstance(group, Group):
            return Member(boss, user, group, online)
        
        raise Exception("Invalid format")
