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


from http import HTTPStatus

from flask import Blueprint, Response, make_response, request
from marshmallow import EXCLUDE, Schema, post_load
from marshmallow.fields import Email, Str

from f4ratk.web.infrastructure import di
from f4ratk.web.mail.mail import MailRequest, MailService

mail_blueprint = Blueprint(name='mail', import_name=__name__)


class MailRequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    name = Str()
    contact = Email()
    content = Str()

    address = Str()
    additionalName = Str()

    @post_load
    def to_mail_request(self, data: dict, **_):
        bot = (data.get('address') or data.get('additionalName')) is not None

        return MailRequest(
            name=data.get('name'),
            contact=data.get('contact'),
            content=data.get('content'),
            bot=bot,
        )


@mail_blueprint.route('/v0/mails', methods=['POST'])
def mails() -> Response:
    mail_request: MailRequest = MailRequestSchema().load(request.get_json())

    di[MailService].relay(mail_request)

    return make_response(
        '', HTTPStatus.NO_CONTENT, {'Content-Type': 'application/json'}
    )
