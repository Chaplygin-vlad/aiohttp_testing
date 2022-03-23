from datetime import datetime, date
from urllib.parse import unquote

from aiohttp import web

from utils.logger import LogDispatcher

logger = LogDispatcher().log


def create_query_for_profile(request):
    """Создание запроса для получения информации по профилю"""
    profile_id = request.rel_url.query.get('profile_id')
    phone_number = request.rel_url.query.get('phone_number')
    if validate_profile_id(profile_id) or phone_number:
        query = f'id = {profile_id}' if profile_id else f"phone_number = '{unquote(phone_number)}'"
        query = f'select * from public.profiles where {query}'
        return query
    else:
        logger.error(f'Неправильный запрос {str(request.rel_url)}')
        raise web.HTTPBadRequest()


def create_mile_transaction_query(request):
    """Создание запроса для получения списка мильных транзакций профиля"""
    profile_id = request.match_info['profile_id']
    start_datetime = request.rel_url.query.get('start_datetime', None)
    last_datetime = request.rel_url.query.get('last_datetime', None)
    query = f"SELECT * FROM public.mile_transactions WHERE profile_id = {profile_id}"
    if start_datetime:
        query = query + f" AND created_date >= '{unquote(start_datetime)}'"
    if last_datetime:
        query = query + f" AND created_date <= '{unquote(last_datetime)}'"
    return query


def prepare_pg_record_to_json(record_dict):
    """Подготовка объекта БД к конвертации в JSON"""
    if record_dict:
        return {
            key: str(value) if isinstance(value, (date, datetime)) else value
            for key, value in dict(record_dict).items()
        }
    else:
        return None


def validate_profile_id(profile_id):
    try:
        int(profile_id)
        return profile_id
    except ValueError:
        return None
