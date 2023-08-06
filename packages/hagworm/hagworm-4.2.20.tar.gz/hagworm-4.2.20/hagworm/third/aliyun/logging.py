# -*- coding: utf-8 -*-

from aliyun.log import QueuedLogHandler
from aliyun.log.logclient import LogClient
from aliyun.log.version import LOGGING_HANDLER_USER_AGENT


class LogHandler(QueuedLogHandler):

    def __init__(self, end_point, access_key_id, access_key, project, log_store, topic=None, source=None, **kwargs):

        super().__init__(end_point, access_key_id, access_key, project, log_store, topic, **kwargs)

        self._source = source

    def create_client(self):

        self.client = LogClient(self.end_point, self.access_key_id, self.access_key, source=self._source)

        self.client.set_user_agent(LOGGING_HANDLER_USER_AGENT)
