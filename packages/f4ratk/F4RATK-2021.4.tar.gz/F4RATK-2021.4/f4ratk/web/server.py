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

import typing
from dataclasses import dataclass
from enum import Enum, auto, unique

from click import group
from flask import Flask, Response, make_response
from flask.cli import FlaskGroup

# noinspection PyPackageRequirements
from marshmallow import Schema, ValidationError
from marshmallow.fields import List, Nested, Str
from werkzeug.exceptions import BadRequest, HTTPException, NotFound

from f4ratk.infrastructure import (
    configure_logging,
    instantiate_dependencies as main_dependencies,
)
from f4ratk.ticker.api import NoTickerData
from f4ratk.web.controller import web_blueprint
from f4ratk.web.infrastructure import (
    instantiate_dependencies as web_dependencies,
    mail_enabled,
    server_cache,
)
from f4ratk.web.mail.controller import mail_blueprint


@unique
class Error(Enum):
    GENERAL = auto()
    NO_DATA = auto()
    INVALID = auto()


@dataclass(frozen=True)
class Source:
    pointer: str


@dataclass(frozen=True)
class ErrorMessage:
    code: str
    status: str
    title: str = None
    detail: str = None
    source: Source = None


@dataclass(frozen=True)
class ErrorsMessage:
    errors: typing.List[ErrorMessage]


class SourceSchema(Schema):
    pointer = Str()


class ErrorSchema(Schema):
    code = Str(required=True)
    status = Str(required=True)
    title = Str()
    detail = Str()
    source = Nested(SourceSchema)


class ErrorsSchema(Schema):
    errors = List(Nested(ErrorSchema))


def create_app() -> Flask:
    configure_logging(verbose=False, server=True)
    main_dependencies()
    web_dependencies()

    app = Flask('f4ratk-server', static_folder=None)

    server_cache.init_app(app)

    @app.errorhandler(HTTPException)
    def error_500(exception: HTTPException) -> Response:
        return make_response(
            ErrorsSchema().dump(
                ErrorsMessage(
                    errors=[
                        ErrorMessage(
                            code=Error.GENERAL.name,
                            status=str(exception.code),
                            title=str("General Error"),
                            detail=str(exception.description),
                        )
                    ]
                )
            ),
            exception.code,
        )

    @app.errorhandler(NoTickerData)
    def error_symbol_unknown(exception: NoTickerData) -> Response:

        return make_response(
            ErrorsSchema().dump(
                ErrorsMessage(
                    errors=[
                        ErrorMessage(
                            code=Error.NO_DATA.name,
                            status=str(NotFound.code),
                            title="No data",
                            detail=str(exception),
                        )
                    ]
                )
            ),
            NotFound.code,
        )

    @app.errorhandler(ValidationError)
    def error_validation(exception: ValidationError) -> Response:
        return make_response(
            ErrorsSchema().dump(
                ErrorsMessage(
                    errors=[
                        ErrorMessage(
                            code=Error.INVALID.name,
                            status=str(BadRequest.code),
                            title="Invalid Attribute",
                            detail=f"{description}",
                            source=Source(pointer=f"/{attribute}"),
                        )
                        for attribute, message in exception.messages.items()
                        for description in message
                    ]
                )
            ),
            BadRequest.code,
        )

    with app.app_context():
        app.register_blueprint(web_blueprint)

        if mail_enabled():
            app.register_blueprint(mail_blueprint)
    return app


@group(cls=FlaskGroup, create_app=create_app)
def server_main():
    pass
