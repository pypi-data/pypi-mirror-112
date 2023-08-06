from abc import ABC
from typing import Optional
from lgt.common.python.slack_client.web_client import SlackWebClient
from lgt_data.mongo_repository import BotMongoRepository, DedicatedBotRepository
from pydantic import BaseModel

from ..basejobs import BaseBackgroundJob, BaseBackgroundJobData

"""
Update bots statistics
"""


class BotStatsUpdateJobData(BaseBackgroundJobData, BaseModel):
    dedicated_bot_id: Optional[str]
    bot_name: Optional[str]


class BotStatsUpdateJob(BaseBackgroundJob, ABC):
    @property
    def job_data_type(self) -> type:
        return BotStatsUpdateJobData

    def exec(self, data: BotStatsUpdateJobData):
        bots_rep = None
        bot = None
        if data.dedicated_bot_id:
            bots_rep = DedicatedBotRepository()
            bot = bots_rep.get_by_id(data.dedicated_bot_id)
        else:
            bots_rep = BotMongoRepository()
            bot = bots_rep.get_by_id(data.bot_name)

        if not bot:
            return

        client = SlackWebClient(bot.token, bot.cookies)
        channels = client.channels_list()['channels']
        bot.connected_channels = sum(1 for channel in channels if channel['is_member'])
        bot.channels = len(channels)
        bots_rep.add_or_update(bot)
