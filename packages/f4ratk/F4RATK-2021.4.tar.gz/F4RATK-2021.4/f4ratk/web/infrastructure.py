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

import logging
from os import environ, getenv
from pathlib import Path
from typing import Any, Dict, Optional, Type, Union

from flask_caching import Cache

from f4ratk.directories import cache
from f4ratk.web.mail.mail import (
    MailComposer,
    MailConfig,
    MailMessageService,
    MailService,
    ServerConfig,
)

Dependencies = Dict[Type[Any], Any]

di: Dependencies = dict()

log = logging.getLogger(__name__)


def locate_cache_dir() -> Union[str, Path]:
    return getenv('CACHE_DIR', cache.file('server'))


def create_cache() -> Cache:
    cache_type = getenv('CACHE_TYPE')
    cache_dir = locate_cache_dir() if cache_type == 'FileSystemCache' else None

    config = dict()

    if cache_type:
        config['CACHE_TYPE'] = cache_type

    if cache_dir:
        config['CACHE_DIR'] = cache_dir

    return Cache(config=config)


server_cache = create_cache()


def mail_config() -> MailConfig:
    return MailConfig(
        from_address=environ['MAIL_FROM_ADDRESS'], to_address=environ['MAIL_TO_ADDRESS']
    )


def server_config() -> ServerConfig:
    return ServerConfig(
        username=environ['MAIL_SERVER_USERNAME'],
        password=environ['MAIL_SERVER_PASSWORD'],
        host=environ['MAIL_SERVER_HOST'],
        port=environ.get('MAIL_SERVER_PORT', 587),
    )


def mail_service() -> Optional[MailService]:
    try:
        return MailService(
            composer=MailComposer(mail_config=mail_config()),
            messenger=MailMessageService(server_config=server_config()),
        )
    except KeyError as error:
        log.warning(
            f"Deactivating the mail feature due to incomplete configuration (Cause: {error})."  # noqa: E501
        )
        return None


def instantiate_dependencies() -> None:
    log.debug("Bootstrapping mail dependencies")
    di.update({MailService: mail_service()})


def dependencies() -> Dict[Type[Any], Any]:
    return di


def mail_enabled() -> bool:
    return di[MailService] is not None
