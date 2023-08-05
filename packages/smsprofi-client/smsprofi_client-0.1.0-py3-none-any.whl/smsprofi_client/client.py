import json
from typing import Optional
from requests import Request, Session, Response


class BaseClient:
    _session = ...

    @classmethod
    def _parse_response_body(cls, response: Response) -> dict:
        raw_data = response.content.decode('utf-8')
        if not raw_data:
            return {}
        data = json.loads(raw_data)
        return data


class SmsProfiAPIClient(BaseClient):
    _base_url = 'https://lcab.smsprofi.ru/json/v1.0'

    def __init__(self, token: str):
        self._session = self._init_session(token)

    @staticmethod
    def _init_session(token: str, params: Optional[dict] = None) -> Session:
        session = Session()
        session.headers = {
            "Content-Type": "application/json",
            'X-Token': token
        }
        if params:
            session.headers.update(params)
        return session

    def send_message(self, to: str, text: str, validate: bool = False) -> Response:
        endpoint = f'{self._base_url}/sms/send/text'
        payload = {
            "validate": validate,
            "messages": [
                {
                    "recipient": to,
                    "recipientType": "recipient",
                    "timeout": 3600,
                    "text": text
                },
            ]}
        return self._send_request('post', endpoint, data=payload)

    def _send_request(self, method: str, url: str, data: dict = None) -> Response:
        request = Request(method, url=url, json=data, headers=self._session.headers).prepare()
        return self._session.send(request)