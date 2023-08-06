import json
import requests
"""
from mongoengine import *
from tpicore.meta import Connector
from tpicore.resources.secrets import secret_parser
from flask import g
"""


class TpiRestApi:
    @classmethod
    def get_response(cls, api_req: requests.Response):
        """Json Response or {} or None"""
        if api_req.status_code > 300:
            return None
        try:
            return api_req.json()
        except (UnicodeDecodeError, json.JSONDecodeError, TypeError):
            return api_req.content

    def __init__(self, api_root: str, api_key: str, ssl_verify: bool = False):
        self.api_root = api_root
        self.api_auth = {"TPI_API_KEY": api_key}
        self.ssl_verify = ssl_verify

    def get_headers(self, transaction_id: str = "") -> dict:
        headers = self.api_auth.copy()
        if transaction_id:
            headers["TPI_TRANSACTION_ID"] = transaction_id
        return headers

    def ping(self, user_name: str):
        endpoint = "/".join([self.api_root, "owner/public/user", user_name])
        try:
            ping_req = requests.get(endpoint, verify=False, headers=self.get_headers(), timeout=60)
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
            return False
        return True if ping_req.status_code < 300 else False

    def rest_list(self, owner_name: str, resource_type: str, payload: dict = None, transaction_id: str = ""):
        payload = {} if not payload else payload
        api_endpoint = "/".join([self.api_root, "owner", owner_name, resource_type])
        api_req = requests.get(api_endpoint, headers=self.get_headers(transaction_id), json=payload.copy(),
                               verify=self.ssl_verify, timeout=60)
        return self.get_response(api_req)

    def rest_load(self, owner_name: str, resource_type: str, resource_name: str, payload: dict = None,
                  transaction_id: str = ""):
        payload = {} if not payload else payload
        api_endpoint = "/".join([self.api_root, "owner", owner_name, resource_type, resource_name])
        api_req = requests.get(api_endpoint, headers=self.get_headers(transaction_id), json=payload.copy(),
                               verify=self.ssl_verify, timeout=60)
        return self.get_response(api_req)

    def rest_new(self, owner_name: str, resource_type: str, resource_name: str, payload: dict = None,
                 transaction_id: str = "") -> bool:
        payload = {} if not payload else payload
        api_endpoint = "/".join([self.api_root, "owner", owner_name, resource_type, resource_name])
        api_req = requests.post(api_endpoint, headers=self.get_headers(transaction_id), json=payload.copy(),
                                verify=self.ssl_verify, timeout=60)
        return self.get_response(api_req)

    def rest_remove(self, owner_name: str, resource_type: str, resource_name: str,
                    transaction_id: str = "") -> bool:
        api_endpoint = "/".join([self.api_root, "owner", owner_name, resource_type, resource_name])
        api_req = requests.delete(api_endpoint, headers=self.get_headers(transaction_id),
                                  verify=self.ssl_verify, timeout=60)
        return self.get_response(api_req)

    def rest_update(self, owner_name: str, resource_type: str, resource_name: str, payload: dict = None,
                    transaction_id: str = "") -> bool:
        payload = {} if not payload else payload
        api_endpoint = "/".join([self.api_root, "owner", owner_name, resource_type, resource_name])
        api_req = requests.patch(api_endpoint, headers=self.get_headers(transaction_id), json=payload.copy(),
                                 verify=self.ssl_verify, timeout=60)
        return self.get_response(api_req)

    def rest_log_read(self, owner_name: str, resource_type: str, resource_name: str, transaction_id: str = "") -> bool:
        if transaction_id:
            api_endpoint = "/".join([self.api_root, "owner", owner_name, resource_type, resource_name,
                                     "log", transaction_id])
        else:
            api_endpoint = "/".join([self.api_root, "owner", owner_name, resource_type, resource_name, "log"])
        api_req = requests.get(api_endpoint, headers=self.get_headers(transaction_id),
                               verify=self.ssl_verify, timeout=60)
        return self.get_response(api_req)

    def rest_transaction_read(self, owner_name: str, resource_type: str, resource_name: str,
                              transaction_id: str = "") -> bool:
        if transaction_id:
            api_endpoint = "/".join([self.api_root, "owner", owner_name, resource_type, resource_name,
                                     "transaction", transaction_id])
        else:
            api_endpoint = "/".join([self.api_root, "owner", owner_name, resource_type, resource_name, "transaction"])
        api_req = requests.get(api_endpoint, headers=self.get_headers(transaction_id),
                               verify=self.ssl_verify, timeout=60)
        return self.get_response(api_req)

    def rest_attach(self, owner_name: str, resource_type: str, resource_name: str, payload: dict = None,
                    transaction_id: str = "") -> bool:
        payload = {} if not payload else payload
        api_endpoint = "/".join([self.api_root, "owner", owner_name, resource_type, resource_name, "handler"])
        api_req = requests.post(api_endpoint, headers=self.get_headers(transaction_id), json=payload.copy(),
                                verify=self.ssl_verify, timeout=180)
        return self.get_response(api_req)

    def rest_detach(self, owner_name: str, resource_type: str, resource_name: str,
                    transaction_id: str = "") -> bool:
        api_endpoint = "/".join([self.api_root, "owner", owner_name, resource_type, resource_name, "handler"])
        api_req = requests.delete(api_endpoint, headers=self.get_headers(transaction_id),
                                  verify=self.ssl_verify, timeout=180)
        return self.get_response(api_req)

    def rest_migrate(self, owner_name: str, resource_type: str, resource_name: str, payload: dict = None,
                     transaction_id: str = "") -> bool:
        payload = {} if not payload else payload
        api_endpoint = "/".join([self.api_root, "owner", owner_name, resource_type, resource_name, "handler"])
        api_req = requests.put(api_endpoint, headers=self.get_headers(transaction_id), json=payload.copy(),
                               verify=self.ssl_verify, timeout=180)
        return self.get_response(api_req)

    def rest_action(self, owner_name: str, resource_type: str, resource_name: str, action: str, payload: dict = None,
                    transaction_id: str = ""):
        payload = {} if not payload else payload
        api_endpoint = "/".join([self.api_root, "owner", owner_name, resource_type, resource_name, "handler", action])
        api_req = requests.post(api_endpoint, headers=self.get_headers(transaction_id), json=payload.copy(),
                                verify=self.ssl_verify, timeout=600)
        return self.get_response(api_req)

    def rest_unlock_task(self, owner_name: str, resource_type: str, resource_name: str, action: str,
                         transaction_id: str = ""):
        api_endpoint = "/".join([self.api_root, "owner", owner_name, resource_type, resource_name, "handler", action])
        api_req = requests.delete(api_endpoint, headers=self.get_headers(transaction_id),
                                  verify=self.ssl_verify, timeout=60)
        return self.get_response(api_req)

    def rest_long_run_task(self, owner_name: str, resource_type: str, resource_name: str, action: str,
                           payload: dict = None, transaction_id: str = ""):
        payload = {} if not payload else payload
        api_endpoint = "/".join([self.api_root, "owner", owner_name, resource_type, resource_name, "handler", action])
        headers = self.get_headers(transaction_id)
        try:
            # Wait 2 seconds for catching quick fail and reset the transaction status
            api_req = requests.post(api_endpoint, headers=headers, json=payload.copy(),
                                    verify=self.ssl_verify, timeout=2)
        except requests.exceptions.Timeout:
            return {"task_status": "running", "transaction_id": headers.get("TPI_TRANSACTION_ID", "")}
        if api_req.status_code == 200:
            return {"task_status": "successful", "transaction_id": headers.get("TPI_TRANSACTION_ID", "")}
        elif api_req.status_code == 409:
            return {"task_status": "conflict", "transaction_id": headers.get("TPI_TRANSACTION_ID", "")}
        else:
            self.rest_unlock_task(owner_name, resource_type, resource_name, action, transaction_id)
            return {"task_status": "failed", "transaction_id": headers.get("TPI_TRANSACTION_ID", "")}
