"""
@author: Gabriele Girelli
@contact: gigi.ga90@gmail.com
"""

import bottle  # type: ignore
import copy
from passlib.hash import pbkdf2_sha256  # type: ignore
import time
from tinydb import Query, TinyDB, where  # type: ignore
from tinydb.operations import delete  # type: ignore
from typing import Dict, Optional, Tuple


class Session(object):
    __db: TinyDB
    __q: Query

    def __init__(self, db: TinyDB):
        super(Session, self).__init__()
        self.__db = db
        self.__q = Query()

    def __get_logged_user(self) -> Optional[Dict[str, str]]:
        search_results = self.__db.table("Users").search(self.__q.cookie_key.exists())
        if 0 == len(search_results):
            return None
        if (
            bottle.request.get_cookie("mnemo-email"),
            bottle.request.get_cookie("mnemo-key"),
        ) == (
            search_results[0]["email"],
            search_results[0]["cookie_key"],
        ):
            return search_results[0]
        else:
            return None

    @property
    def is_logged(self) -> bool:
        """Checks if a user is currently logged.
        Only one user can be logged at the same time.
        """
        logged_user = self.__get_logged_user()
        return logged_user is not None

    @property
    def has_users(self) -> bool:
        return 0 != len(self.__db.table("Users"))

    def create_first_user(self, request) -> str:
        assert not self.has_users
        try:
            self.__db.table("Users").insert(
                {
                    "name": "<username>",
                    "email": request.forms.get("user_email"),
                    "password": pbkdf2_sha256.hash(request.forms.get("user_password")),
                    "cookie_key": None,
                    "last_touch": time.time(),
                }
            )
            return '{"response":"success", "success":true}'
        except Exception:
            return '{"response":"failed", "success":false}'

    def __verify_logged_password(self, password: str) -> bool:
        logged_user = self.__get_logged_user()
        assert logged_user is not None
        return pbkdf2_sha256.verify(
            password,
            logged_user["password"],
        )

    def login(self, request) -> str:
        """Logs user based on user_email and user_password fields in request."""
        self.logout()
        try:
            email = request.forms.get("user_email")
            search_results = self.__db.table("Users").search(self.__q.email == email)

            if 0 == len(search_results):
                return '{"response":"not-found", "success":false}'

            if pbkdf2_sha256.verify(
                request.forms.get("user_password"), search_results[0]["password"]
            ):
                cookie_key = pbkdf2_sha256.hash(str(time.time()))
                print(cookie_key)
                self.__db.table("Users").update(
                    {"cookie_key": cookie_key, "last_touch": time.time()},
                    where("email") == email,
                )
                bottle.response.set_cookie(
                    "mnemo-email",
                    email,
                    max_age=60 * 30,
                    httponly=True,
                )
                bottle.response.set_cookie(
                    "mnemo-key",
                    cookie_key,
                    max_age=60 * 30,
                    httponly=True,
                )
                return '{"response":"logged", "success":true}'
            else:
                return '{"response":"wrong-pwd", "success":false}'
        except Exception as e:
            print(e)
            return '{"response":"failed", "success":false}'

    def logout(self) -> str:
        """Logs user out. Does not delete the session cookie."""
        try:
            self.__db.table("Users").update_multiple(
                [
                    ({"last_touch": time.time()}, self.__q.cookie_key.exists()),
                    (delete("cookie_key"), self.__q.cookie_key.exists()),
                ]
            )
            return '{"response":"logged-out", "success":true}'
        except Exception as e:
            print(e)
            return '{"response":"failed", "success":false}'

    def get_logged_user_data(self) -> Dict[str, str]:
        logged_user = self.__get_logged_user()
        if logged_user is None:
            return {}
        user_data = copy.copy(logged_user)
        user_data.pop("password", None)
        user_data.pop("cookie_key", None)
        return user_data

    def __get_field_and_value(self, request) -> Tuple[str, str, Optional[str]]:
        target_field = request.forms.get("field")
        if target_field not in ("email", "password", "name"):
            return (
                target_field,
                "",
                "".join(
                    [
                        '{"response":"wrong-field", ',
                        '"success":false, ',
                        f'"field":"{target_field}"}}',
                    ]
                ),
            )

        if "password" == target_field:
            new_password = request.forms.get("new_password")
            assert new_password == request.forms.get("confirm_password")
            assert 8 <= len(new_password) and 20 >= len(new_password)
            if not self.__verify_logged_password(request.forms.get("old_password")):
                return (
                    target_field,
                    "",
                    '{"response":"wrong-password", "success":false}',
                )
            new_value = pbkdf2_sha256.hash(request.forms.get("new_password"))
        else:
            new_value = request.forms.get("value")
        return (target_field, new_value, None)

    def edit_field(self, request) -> str:
        if not self.is_logged:
            return '{"response":"not-logged", "success":false}'

        target_field, new_value, response = self.__get_field_and_value(request)
        if response is not None:
            return response

        try:
            self.__db.table("Users").update(
                {target_field: new_value, "last_touch": time.time()},
                where("cookie_key") == request.get_cookie("mnemo-key"),
            )
            return '{"response":"edited", "success":true}'
        except Exception as e:
            print(e)
            return '{"response":"failed", "success":false}'
