from vk_search import PeopleSearch
from console_backend import get_criteriums_from_console_input
from service import Application
from config import *

if __name__ == '__main__':
    app = Application(GROUP_TOKEN)
    app.run()
    # while True:
    #     search_criteriums = get_criteriums_from_console_input()
    #     search_request = PeopleSearch(**search_criteriums)
    #     search_request.search()
