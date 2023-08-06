##############################################################################
# Copyright (C) 2020 - 2021 Tobias Röttger <dev@roettger-it.de>
#
# This file is part of F4RATK.
#
# F4RATK is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License version 3
# as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
##############################################################################

import ssl
from dataclasses import dataclass
from email.message import EmailMessage
from smtplib import SMTP
from typing import Optional


@dataclass(frozen=True)
class MailRequest:
    name: Optional[str]
    contact: Optional[str]
    content: Optional[str]
    bot: bool


@dataclass(frozen=True)
class MailConfig:
    from_address: str
    to_address: str


class MailComposer:
    def __init__(self, mail_config: MailConfig):
        self._mail_config = mail_config

    def mail(self, request: MailRequest) -> EmailMessage:
        sender = self._format_sender(request)
        bot = "[BOT]" if request.bot else ""

        message = EmailMessage()
        if request.content:
            message.set_content(request.content)
        message['Subject'] = f"[F4RATK]{bot} Feedback from '{sender}'"
        message['From'] = self._mail_config.from_address
        message['To'] = self._mail_config.to_address

        return message

    @staticmethod
    def _format_sender(request: MailRequest) -> str:
        if request.name and request.contact:
            return f"{request.name} ({request.contact})"
        elif request.name or request.contact:
            return request.name or request.contact
        else:
            return "Anonymous User"


@dataclass(frozen=True)
class ServerConfig:
    username: str
    password: str
    host: str
    port: int


class MailMessageService:
    def __init__(self, server_config: ServerConfig):
        self._server_config = server_config

    def send(self, message: EmailMessage):
        with self._server_connection() as server:
            server.starttls(context=ssl.create_default_context())
            server.login(
                user=self._server_config.username, password=self._server_config.password
            )
            server.send_message(message)
            server.quit()

    def _server_connection(self) -> SMTP:
        return SMTP(
            host=self._server_config.host,
            port=self._server_config.port,
        )


class MailService:
    def __init__(self, composer: MailComposer, messenger: MailMessageService):
        self._composer = composer
        self._messenger = messenger

    def relay(self, request: MailRequest):
        self._messenger.send(self._composer.mail(request))
