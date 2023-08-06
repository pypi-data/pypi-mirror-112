#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" Модуль авторизации в Полиматике """

import requests
import json
from typing import Tuple, Dict
from .exceptions import AuthError


class Authorization:
    """ Предоставляет возможность авторизации в Полиматике """

    def login(self, user_name: str, url: str, server_codes: Dict, password: str = None, language: str = None) -> Tuple:
        """
        Авторизация (парольная/беспарольная).
        :param user_name: имя пользователя
        :param password: пароль
        :param url: базовый URL стенда
        :param server_codes: значение файла "server_codes.json" (хранит коды команд и их состояний)
        :param language: "en" / "ru" / "de" / "fr"
        :return: (Tuple) идентификатор сессии, uuid, полная версия Полиматики
        """
        # для авторизации с паролем
        session = ""

        auth_manager_command = server_codes.get("manager", {}).get("command", {}).get("authenticate", {})
        auth_command = auth_manager_command.get("id")
        auth_check = auth_manager_command.get("state", {}).get("check")
        auth_login = auth_manager_command.get("state", {}).get("login")
        language = server_codes.get("locale", {}).get(language)

        # для авторизации без пароля формируем id сессии для беспарольного пользователя
        if password is None:
            login_url = "{}login".format(url)
            r = requests.get(url=login_url, params={"login": user_name})
            if not r.ok:
                msg = 'Invalid server response (URL: {}, Code: {}, Reason: "{}", Text: {})'.format(
                    login_url, r.status_code, r.reason, '<empty>' if not r.text else r.text)
                raise AuthError(msg)
            else:
                try:
                    response = r.json()
                except json.decoder.JSONDecodeError:
                    msg = 'Host "{}" not supporting non-password authorization. Please, specify the password!'.format(
                        login_url)
                    raise AuthError(msg)
            if len(r.history) > 0:
                for resp in r.history:
                    session = resp.cookies.get("session")
            else:
                session = response.get("session")

        # формирование command
        command = {"plm_type_code": auth_command}
        if password is None:
            # для авторизации без пароля добавить в command состояние check
            command.update({"state": auth_check})
        else:
            # для авторизации с паролем добавить в command следующие параметры
            command.update({"state": auth_login, "login": user_name, "passwd": password, "locale": language})

        # формирование params
        params = {
            "state": 0,
            "session": session,
            "queries": [
                # query1, query2, ..., queryN will be appended in this list
            ]
        }
        query = {"uuid": "00000000-00000000-00000000-00000000", "command": command}
        params["queries"].append(query)

        # отправляем запрос аутентификации на заданный URL
        r = requests.request(method="POST", url=url, json=params, timeout=60.0)

        # проверки и вывод результата
        status_code = r.status_code
        if not r.ok:
            msg = 'Invalid server response (URL: {}, Code: {}, Reason: "{}", Text: {})'.format(
                url, status_code, r.reason, '<empty>' if not r.text else r.text)
            raise AuthError(msg)
        else:
            try:
                json_response = r.json()
            except json.decoder.JSONDecodeError:
                raise AuthError('Server response cannot be converted to the JSON format')
            return self._authorization_checks(params, json_response, status_code)

    def _get_command(self, data: Dict) -> Dict:
        """
        Возвращает команду запроса/ответа.
        """
        queries = next(iter(data.get("queries")))
        return queries.get("command")

    def _authorization_checks(self, request: Dict, response: Dict, response_code: int) -> Tuple:
        """
        Проверка успешности авторизации. Возвращает идентификатор сессии и manager uuid.
        :param request: (Dict) запрос
        :param response: (Dict) ответ
        :param response_code: (int) код ответа
        :return: (Tuple) идентификатор сессии, uuid, полная версия Полиматики
        """
        # получаем команды и коды запроса/ответа
        request_command = self._get_command(request)
        request_code = request_command.get("plm_type_code")
        resp_command = self._get_command(response)
        resp_code = resp_command.get("plm_type_code")

        # проверки полученных кодов
        assert "error" not in resp_command, resp_command.get("error")
        assert response_code == 200, "Response code != 200"
        assert request_code == resp_code, "plm_type_code in request (%s) != plm_type_code (%s) in response!" % \
                                        (request_code, resp_code)

        # извлекаем идентификаторы
        session_id = resp_command.get("session_id")
        uuid = resp_command.get("manager_uuid")
        polymatica_version = resp_command.get('version')

        # проверки идентификаторов
        assert session_id != "", "session_id == empty string"
        assert session_id is not None, "session_id is None!"
        assert uuid != "", "manager_id == empty string"
        assert uuid is not None, "manager_id is None!"

        return session_id, uuid, polymatica_version
