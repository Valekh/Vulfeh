import vk_api
import vk_api.vk_api
import random
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id


class Connect:

    def __init__(self):
        self.vk_session = vk_api.VkApi(
            token='5e9a91916381c387b6cd10bc4a5ddea923e3f2a85ac2ad1ebf848e20ef9f46c1dfb92002ee04d8e6d6688')
        self.longpoll = VkBotLongPoll(self.vk_session, '190173129')
        self.vk_api = self.vk_session.get_api()


class Vk:
    def __init__(self):
        self.ChatBot = Connect()
        self.BotLogic = Bot()

    def check(self):
        for event in self.ChatBot.longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                self.BotLogic.who(event.obj.text.lower(), event.obj.peer_id, self.get_user_name(event.obj.from_id))

    def send_message(self, peer_id, text):
        self.ChatBot.vk_api.messages.send(peer_id=peer_id, message=text, random_id=get_random_id())

    def get_user_name(self, user_id):
        return self.ChatBot.vk_api.users.get(user_id=user_id)[0]['first_name']

    def count_members(self, peer_id):
        return self.ChatBot.vk_api.messages.getConversationMembers(peer_id=peer_id, group_id="190173129")['count']

    def id_of_member(self, peer_id, number):
        return \
        self.ChatBot.vk_api.messages.getConversationMembers(peer_id=peer_id, group_id="190173129")["items"][number][
            "member_id"]


class Bot:
    def __init__(self):
        self.mode = []
        self.HomeWork = []
        self.Confa = []

    def who(self, text, peer, name):
        if peer in self.Confa:
            self.treatment(text, peer, name, self.Confa.index(peer))
        else:
            self.Confa.append(peer)
            self.mode.append("default")
            self.HomeWork.append("пусто")
            self.treatment(text, peer, name, self.Confa.index(peer))
            return

    def treatment(self, text, peer, name, index):
        if text == "":
            return
        text = text.strip()
        newtext = text.split()
        count = len(newtext)
        if self.mode[index] == "default":
            if newtext[0] == "бот" or newtext[0] == "бот,":
                if count == 1:
                    VkBot.send_message(peer, "чего тебе?")
                    return
                elif newtext[1] == "дз":
                    if count == 2:
                        VkBot.send_message(peer, "чо дз-то? показать или записать?")
                        return
                    elif newtext[2] == "запиши":
                        VkBot.send_message(peer, "диктуй")
                        self.mode[index] = "homework record"
                        return
                    elif newtext[2] == "покажи":
                        VkBot.send_message(peer, self.HomeWork[index])
                        VkBot.send_message(peer, "учи уроки, школяр :Р")
                        return
                    else:
                        VkBot.send_message(peer, "заебись объяснил, я прям всё понял (запиши/покажи)")
                        return
                elif newtext[1] == "геймод":
                    VkBot.send_message(peer, "ну чё, народ, погнали нахуй? (выключить - \"вырубись\")")
                    self.mode[index] = "gay mode"
                    return
                elif newtext[1] == "кто" and count > 2:
                    x = random.randint(0, VkBot.count_members(peer)) - 1
                    member_id = VkBot.id_of_member(peer, x)
                    if member_id < 0:
                        VkBot.send_message(peer, "я хуй знает")
                    else:
                        VkBot.send_message(peer, "я думаю, " + newtext[2] + " это *id" + str(member_id) + " (" + VkBot.get_user_name(member_id) + ")")
                        return
                else:
                    VkBot.send_message(peer, "нихуя не понятно, блят. что тебе нужно, нормально говорить можешь?")
                    return
        elif self.mode[index] == "gay mode":
            if text == "вырубись":
                VkBot.send_message(peer, "молчу")
                self.mode[index] = "default"
                return
            else:
                text = name + " гей"
                VkBot.send_message(peer, text)
                return
        elif self.mode[index] == "homework record":
            self.HomeWork[index] = text
            VkBot.send_message(peer, "записал")
            self.mode[index] = "default"
            return
        else:
            VkBot.send_message(peer, "ты нашёл баг, молодец. позови Валеха, пусть пофиксит")


VkBot = Vk()
VkBot.check()
