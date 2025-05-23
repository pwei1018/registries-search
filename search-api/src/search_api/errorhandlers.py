# Copyright © 2022 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Core error handlers and custom exceptions.

Following best practices from:
http://flask.pocoo.org/docs/1.0/errorhandling/
http://flask.pocoo.org/docs/1.0/patterns/apierrors/
"""

import sys

from flask import current_app, jsonify
from werkzeug.exceptions import HTTPException
from werkzeug.routing import RoutingException


def init_app(app):
    """Initialize the error handlers for the Flask app instance."""
    app.register_error_handler(HTTPException, handle_http_error)
    app.register_error_handler(Exception, handle_uncaught_error)


def handle_http_error(error):
    """Handle HTTPExceptions.

    Include the error description and corresponding status code, known to be
    available on the werkzeug HTTPExceptions.
    """
    # As werkzeug's routing exceptions also inherit from HTTPException,
    # check for those and allow them to return with redirect responses.
    if isinstance(error, RoutingException):
        return error

    response = jsonify({"message": error.description})
    response.status_code = error.code
    return response


def handle_uncaught_error(_: Exception):
    """Handle any uncaught exceptions.

    Since the handler suppresses the actual exception, log it explicitly to ensure it's logged.
    """
    current_app.logger.error("Uncaught exception", exc_info=sys.exc_info())
    response = jsonify({"message": "Internal server error"})
    response.status_code = 500
    return response
