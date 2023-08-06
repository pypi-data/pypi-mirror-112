import json

from aiohttp import web
from aiohttp_cors import CorsViewMixin  # type: ignore
from marshmallow import ValidationError

from ..config import CONFIG


class ValidatingView(web.View, CorsViewMixin):
    async def _valid_json(self, request):
        try:
            body = await self.request.json()
        except json.JSONDecodeError:
            raise web.HTTPBadRequest(reason='Invalid JSON')
        return body

    def _validate(self, schema, body, **kwargs):
        try:
            return schema.load(body, **kwargs)
        except ValidationError as e:
            item, problem = list(e.messages.items())[0]
            raise web.HTTPBadRequest(
                reason=f'Validation error on field "{item}": {problem[0]}')
        except json.JSONDecodeError:
            raise web.HTTPBadRequest(reason='Invalid JSON')


def paginate_query(request, query_tup, max_limit: int = None):
    if not max_limit:
        max_limit = int(CONFIG['API_RESULT_LIMIT'])
    try:
        offset = int(
            request.query['offset']) if 'offset' in request.query else 0
        limit = None
        if 'limit' in request.query:
            limit = int(request.query['limit'])
        else:
            limit = max_limit
        if limit > max_limit:
            limit = max_limit
    except ValueError:
        raise web.HTTPBadRequest(text='Bad pagination values')
    orig_query, *orig_args = query_tup
    new_query = (
        f'{orig_query} LIMIT ${len(orig_args)+1} OFFSET ${len(orig_args)+2}',
        *orig_args, limit, offset)
    return new_query
