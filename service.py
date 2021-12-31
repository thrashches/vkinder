import random
from random import randrange

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from messages import *
from vk_search import PeopleSearch
from datetime import datetime
from banners import BANNERS


class Application(object):
    token = None
    api = None

    def __init__(self, group_token):
        self.token = group_token
        self.api = vk_api.VkApi(token=self.token)

    def write_msg(self, user_id, message, *attachments):
        if not len(attachments):
            self.api.method('messages.send',
                            {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7), })
        else:
            self.api.method('messages.send',
                            {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7),
                             'attachment': ','.join(attachments)})

    def run(self):
        print('\033[92mStarting Vkinder BOT service...\033[0m')
        longpoll = VkLongPoll(self.api)

        print(f'\033[96m{BANNERS[random.randint(0, len(BANNERS) - 1)]}\033[0m')
        last_event = None

        search_criteriums = {}
        print('VkLongPoll listener initialized and started.')
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:

                if event.to_me:
                    request = event.text
                    if request == 'search' and not last_event:
                        self.write_msg(event.user_id, SEARCH_GREETING)
                        self.write_msg(event.user_id, ASK_CITY)
                        last_event = 'wait_for_city'
                    elif request == 'stop' and last_event:
                        self.write_msg(event.user_id, STOP)
                        last_event = None
                        search_criteriums = None
                    elif last_event == 'wait_for_city':
                        if request != '0':
                            search_criteriums['city'] = request
                        self.write_msg(event.user_id, ASK_SEX)
                        last_event = 'wait_for_sex'
                    elif last_event == 'wait_for_sex':
                        search_criteriums['sex'] = request
                        self.write_msg(event.user_id, ASK_AGE_FROM)
                        last_event = 'wait_for_age_from'
                    elif last_event == 'wait_for_age_from':
                        if request != '0':
                            search_criteriums['age_from'] = request
                        self.write_msg(event.user_id, ASK_AGE_TO)
                        last_event = 'wait_for_age_to'
                    elif last_event == 'wait_for_age_to':
                        if request != '0':
                            search_criteriums['age_to'] = request
                        self.write_msg(event.user_id, ASK_STATUS)
                        last_event = 'wait_for_status'
                    elif last_event == 'wait_for_status':
                        if request != '0':
                            search_criteriums['status'] = request

                        last_event = None
                        print(search_criteriums)

                        finder = PeopleSearch(event.user_id, **search_criteriums)
                        results = finder.search()
                        print(results)
                        for item in results:
                            self.write_msg(event.user_id, finder.get_profile_link(item),
                                           *finder.get_best_3_photos(item))
                        search_criteriums = {}
                    print(f'\033[93m[{datetime.now()}] New message - {event.user_id}: {event.text}\033[0m')
