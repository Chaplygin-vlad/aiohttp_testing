from aiohttp import web

from utils.logger import LogDispatcher
from utils.utils import create_mile_transaction_query, create_query_for_profile, prepare_pg_record_to_json

logger = LogDispatcher().log


async def get_profile(request):
    """Подробная информация по профилю по profile_id или phone_number
    Пример .../api/v1/profile/?profile_id=1
    profile_id - profile_id профиля

    Пример .../api/v1/profile/?phone_number=+7999999999999
    phone_number - phone_number профиля

    result = {
    "id": id(int),
    "uid": uid(str),
    "first_name": first_name(str),
    "last_name": last_name(str),
    "patronymic": patronymic(str),
    "appeal_type_id": appeal_type_id(int),
    "birth_date": birth_date(str),
    "phone_number": phone_number(str),
    "email": email(str),
    "is_superuser": is_superuser(bool),
    "user_status_id": user_status_id(int),
    "active": active(bool),
    "update_date": update_date(str),
    "is_deleted": is_deleted(bool),
    "created_date": created_date(str),
    "last_login": last_login(str),
    "mile_count": mile_count(int),
    "pqr": pqr(str),
    "pass_count": pass_count(int),
    "pass_count_1": pass_count_1(int),
    "pass_count_2": pass_count_2(int),
    "pass_count_3": pass_count_3(int),
    "sent": sent(bool),
    "channel_sms_enable": channel_sms_enable(bool),
    "channel_push_enable": channel_push_enable(bool),
    "channel_email_enable": channel_email_enable(bool),
    "unread_banners_count": unread_banners_count(int),
    "email_for_receipts": email_for_receipts(str),
    "email_confirmed": email_confirmed(bool),
    "last_time_sent_email": last_time_sent_email(str)
}
    """
    pool = request.app['db']
    async with pool.acquire() as connection:
        async with connection.transaction():
            query = create_query_for_profile(request)
            result = await connection.fetchrow(query)
            dict_result = prepare_pg_record_to_json(result)
            logger.info(f'Получена информация по профилю - id = {dict_result["id"]}')
            return web.json_response(dict_result)


async def get_mile_transactions(request):
    """Подробная информация о всех мильных транзакциях пользователя с возможностью указания временных промежутков
    Пример .../api/v1/mile_transactions/1?start_datetime=2021-12-04 10:36:00&last_datetime=2022-03-03 10:36:00
    1 - profile_id
    start_datetime - стартовое время фильтрации
    last_datetime - конечное время фильтрации

    result = [
        {
        "id": id(int),
        "mile_packet_id": mile_packet_id(int),
        "mile_count": mile_count(int),
        "transaction_type_id": transaction_type_id(int),
        "table_name": table_name(str),
        "primary_key": primary_key(int),
        "mile_general_count": mile_general_count(int),
        "confirmation_code": confirmation_code(int),
        "created_date": created_date(str),
        "receipt": receipt(str),
        "charged_back": charged_back(bool),
        "profile_id": profile_id(int),
        "isprocessed": isprocessed(bool),
        "issended": issended(bool)
        }
        ]
    """
    pool = request.app['db']
    async with pool.acquire() as connection:
        query = create_mile_transaction_query(request)
        async with connection.transaction():
            result = await connection.fetch(query)
            dict_result = [prepare_pg_record_to_json(ix) for ix in result]
            logger.info(f'Получены мильные транзакции профиля - id = {request.match_info["profile_id"]}')
            return web.json_response(dict_result)
