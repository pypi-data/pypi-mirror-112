from logging import Logger, LoggerAdapter
from typing import Union
from urllib.parse import urljoin

from requests import Response, Session
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError

from ..version import VERSION

# REFACTOR: Check similarities with Socrates connection and reduce code duplication.


class AthenaHttpSession(object):
    """
    Connection to access the Athena API.
    """

    def __init__(
        self,
        api_url: str,
        username: str,
        password: str,
        logger: Union[Logger, LoggerAdapter],
    ):
        self.__url = api_url
        self.__session = Session()
        self.__username = username
        self.__password = password
        self.__logger = logger

        # https://2.python-requests.org/en/master/api/#requests.adapters.HTTPAdapter
        retry_adapter = HTTPAdapter(max_retries=5)
        self.__session.mount("http://", retry_adapter)
        self.__session.mount("https://", retry_adapter)

        self.__session.headers.update(
            {
                "Accept-Charset": "utf-8",
                "Content-Type": "application/json",
                "User-Agent": "paretos/{}".format(VERSION),
            }
        )

    def request(
        self,
        path: str,
        contains_sensitive_data: bool,
        data=None,
        method: str = "POST",
    ):
        """
        Issues a request to the Athena API.
        """

        if method not in ["POST", "GET"]:
            raise ValueError("Invalid Request method chosen.")

        auth = None

        if self.__username:
            auth = (self.__username, self.__password)

        url = urljoin(self.__url, path)

        self.__log_request(
            url=url,
            method=method,
            data=data,
            contains_sensitive_data=contains_sensitive_data,
        )

        try:
            response = self.__session.request(method, url, json=data, auth=auth)
        except ConnectionError:
            self.__logger.error("Unable to connect to Athena API.", extra={"url": url})

            raise RuntimeError("Unable to connect to Athena API.")

        self.__log_response(
            contains_sensitive_data=contains_sensitive_data, response=response
        )

        if response.status_code == 401:
            self.__logger.error(
                "The Athena API rejected the authorization credentials."
            )
            raise RuntimeError("Athena API rejected authorization.")

        if response.status_code != 200:
            self.__logger.error(
                "A request to the Athena API failed because of a bad HTTP status code.",
                extra={"url": url, "http_status_code": response.status_code},
            )
            raise RuntimeError("Request to Athena API failed.")

        try:
            response_json = response.json()
        except ValueError:
            self.__logger.error("Unable to parse Athena API response json.")
            raise RuntimeError("Unable to parse Athena API response json.")

        return response_json

    def __log_request(self, url: str, method: str, data, contains_sensitive_data: bool):
        details = {"url": url, "method": method}

        if not contains_sensitive_data:
            details["data"] = data

        self.__logger.debug("Athena API request.", extra=details)

    def __log_response(self, contains_sensitive_data: bool, response: Response):
        details = {"status": response.status_code}

        if not contains_sensitive_data:
            details["data"] = response.text

        self.__logger.debug("Athena API response.", extra=details)
