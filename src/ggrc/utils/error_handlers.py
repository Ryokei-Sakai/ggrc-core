# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Custom HTTP error handlers.

Setup is done in ggrc/app.py
We need these custom error handlers to make error responses available in json
when front-end requests it. This makes it easy for the front-end to show
error messages without a need to parse html.
"""

from flask import current_app, request

from ggrc.utils import as_json


def make_error_response(err, force_json=False):
  """Compose the response based on the request content_type"""
  if request.content_type == 'application/json' or force_json:
    resp = {"code": err.code,
            "message": err.description}
    headers = [('Content-Type', 'application/json'), ]
    return current_app.make_response((as_json(resp), err.code, headers), )
  return err.get_response()


def register_handlers(app):
  # pylint: disable=unused-variable; we use bad_request in the decorator
  @app.errorhandler(400)
  def bad_request(err):
    """Custom handler for BadRequest error

    Returns JSON object with error code and message in response body.
    """
    return make_error_response(err, force_json=True)

  @app.errorhandler(401)
  def unauthorized(err):
    """Custom handler for Unauthorized error
    """
    return make_error_response(err)

  @app.errorhandler(404)
  def not_found(err):
    """CUstom handler for NotFound error
    """
    return make_error_response(err)

  @app.errorhandler(500)
  def internal_error(err):
    """CUstom handler for InternalServerError
    """
    return make_error_response(err)
