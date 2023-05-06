from urllib import response
from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync
from slugify import slugify

from infra.user.models import UserAccount
from infra.tournamments.models import Group,Members
from infra.tournamments.serializers import GroupSerializer,MemberSerializer
from users.serializers import UserCreateSerializer

from exercises.models import ListTournamment,QuestionTounamment
from exercises.serializers import ListTournammentSerializer,QuestionTournammentSerializer


from adapter import websocket_adapter
from composer import create_group_websocker_composite


class ChatConsumer(JsonWebsocketConsumer):
    """
    This consumer is used to show user's online status,
    and send notifications.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.user = None
        self.numembers = 0


    def set_user_online(self,id):
        user = UserAccount.objects.filter(id=id)
        for user in user:
            user.online = True
            user.save()


    def set_user_offine(self,id):
        user = UserAccount.objects.filter(id=id)
        for user in user:
            user.online = False
            user.save()

        
    def get_user_online(self):
        user_filter_online = UserAccount.objects.filter(online=True)
        serializer_user = UserCreateSerializer(user_filter_online,many=True)
        return serializer_user.data
    

    def connect(self):
        self.user = self.scope["user"]

        if not self.user.is_authenticated:
            return
        self.set_user_online(self.user.id)


        print("Connected!")
        self.room_name = "tournamment"
        self.accept()

        members = Members.objects.filter(user=self.user)


        if members.__len__() != 0:
            self.send_json({
                "type":"redirectToGroup",
                "data":members[0].group.slug,
            })


        async_to_sync(self.channel_layer.group_add)(
        self.room_name,
        self.channel_name,
    )

        groups = Group.objects.all()
        serializer = GroupSerializer(groups,many=True)




        self.send_json(
            {
                "type": "getUserOnline",
                "users": self.get_user_online(),
            }
        )

        self.send_json(
            {
                "type": "getGroup",
                "group": serializer.data,
            }
        )
        

    def disconnect(self, code):
        print("Disconnected!")
        self.set_user_offine(self.user.id)

        async_to_sync(self.channel_layer.group_send)(
                        self.room_name,
                        {
                            "type": "refreshUserOnline",
                            "users": self.get_user_online()
                        },
                        
                    ) 
        groups = Group.objects.all()
        serializer = GroupSerializer(groups,many=True)

        async_to_sync(self.channel_layer.group_send)(
                        self.room_name,
                        {
                            "type": "getGroup",
                            "group": serializer.data,

                        },
                    ) 

                 
        return super().disconnect(code)

    def receive_json(self, content, **kwargs):
        
        if content["type"] == "createGroup":
            data = {
                "name": content["content"],
                "turma": self.user.turma.id
            }
            response = websocket_adapter(data, gateway=create_group_websocker_composite())

            async_to_sync(self.channel_layer.group_send)(
                    self.room_name,
                    {
                        "type": "createGroup",
                        "group": {"name":response.name,"slug":response.slug.get_slug()}
                    },
                )
       
        if content["type"] == "refreshUserOnline":

                async_to_sync(self.channel_layer.group_send)(
                self.room_name,
                {
                    "type": "refreshUserOnline",
                    "users": self.get_user_online()
                },
            )

            


        return super().receive_json(content, **kwargs)

    def refreshUserOnline(self,event):
        self.send_json(event)

    def redirectToGroup(self,event):
        self.send_json(event)

    def createGroup(self,event):
        self.send_json(event)


from infra.user.models import Score


class GroupTournamment(JsonWebsocketConsumer):
    """
    This consumer is used to show user's online status,
    and send notifications.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.group_name = None
        self.user = None
        self.slug = None
        self.group = None

    def set_user_online(self,id):
        user = UserAccount.objects.filter(id=id)
        for user in user:
            user.online = True
            user.save()


    def get_question(self):
        lista  = ListTournamment.objects.filter(availability=True)
        if lista.__len__() == 1:
            questions = QuestionTounamment.objects.filter(list=lista[0])
            serializer = QuestionTournammentSerializer(questions, many=True)
            return serializer.data

    def set_user_offine(self,id):
        user = UserAccount.objects.filter(id=id)
        for user in user:
            user.online = False
            user.save()

    def get_user_online(self):
        user_filter_online = Members.objects.filter(online=True,group=self.group[0])
        serializer = MemberSerializer(user_filter_online,many=True)
        return serializer.data

    def get_question_checked(self):
        score = Score.objects.filter(type="tournamment",user_score=self.user,acert=True)
        lista_id = [ x.question_id for x in score ]
        return lista_id


    def connect(self):
        self.user = self.scope["user"]

        if not self.user.is_authenticated:
            return

        self.set_user_online(self.user.id)
        self.slug = self.scope["url_route"]["kwargs"]["slug"]

        groups = Group.objects.filter(slug=self.slug)
        if groups.__len__() == 0:
            return
        self.group = groups

        member = Members.objects.get_or_create(user=self.user,group=groups[0])

        test = Members.objects.filter(user=self.user)

        for i in test:
            i.online = True
            i.save()

        print("Connected!")
        self.room_name = self.slug
        self.accept()

        self.send_json({
            "type":"groupInformation",
            "data":groups[0].name
        })

        self.send_json({
            "type":"get_question",
            "questions": self.get_question()
        })

        

        self.send_json({
            "type":"get_question_checked",
            "questions_checked": self.get_question_checked()
        })



        async_to_sync(self.channel_layer.group_add)(
        self.room_name,
        self.channel_name,
    )



    

        serializer = GroupSerializer(groups,many=True)

        self.send_json(
            {
                "type": "getUserOnline",
                "users": self.get_user_online(),
            }
        )

        self.send_json(
            {
                "type": "getGroup",
                "group": serializer.data,
            }
        )
        

    def disconnect(self, code):
        print("Disconnected!")
        self.set_user_offine(self.user.id)

        test = Members.objects.filter(user=self.user)

        for i in test:
            i.online = False
            i.save()

        async_to_sync(self.channel_layer.group_send)(
                        self.room_name,
                        {
                            "type": "refreshUserOnline",
                            "users": self.get_user_online()
                        },
                    ) 
                    
        return super().disconnect(code)

    def receive_json(self, content, **kwargs):

        if content["type"] == "chat_message":
            async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            {
                "type": "chat_message",
                "name": self.user.username,
                "message": content["message"],
            },
        )


        if content["type"] == "createGroup":
            name = content["content"]
            slug = slugify(name)

            group = Group.objects.get_or_create(name=name, slug=slug)

            async_to_sync(self.channel_layer.group_send)(
                self.room_name,
                {
                    "type": "createGroup",
                    "group": {"name":group[0].name,"slug":group[0].slug}

                },
            )            

        if content["type"] == "question_checked":

            score = Score.objects.filter(type="tournamment",user_score=self.user,acert=True)
            lista_id = [ x.question_id for x in score ]


            async_to_sync(self.channel_layer.group_send)(
                self.room_name,
                {
                    "type": "refresh_question_checked",
                    "questions_checked": self.get_question_checked()
                },
            )

        if content["type"] == "refreshUserOnline":

                async_to_sync(self.channel_layer.group_send)(
                self.room_name,
                {
                    "type": "refreshUserOnline",
                    "users": self.get_user_online()
                },
            ) 

        if content["type"] == "exitGroup":
            m = Members.objects.filter(user=self.user)
            m[0].delete()
            self.send_json({
                "type":"redirect"
            })
            

            


        return super().receive_json(content, **kwargs)

    def refresh_question_checked(self,event):
        self.send_json(event)

    def refreshUserOnline(self,event):
        self.send_json(event)

    def createGroup(self,event):
        self.send_json(event)

    def chat_message(self,event):
        self.send_json(event)