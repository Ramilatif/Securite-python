import re

import requests

from src.tp3.utils.captcha import Captcha


class Session:
    """
    Class representing a session to solve a captcha and submit a flag.
    """

    def __init__(self, url):
        self.url = url
        self.captcha_value = ""
        self.flag_value = ""
        self.valid_flag = ""
        self._http_session = requests.Session()
        self._response = None
        flag_start = 1000 if "captcha1" in url else 2000
        flag_end = 2001 if "captcha1" in url else 3001
        self._flag_iter = iter(range(flag_start, flag_end))

    def prepare_request(self):
        """
        Prépare la requête : capture et résout le captcha, incrémente la valeur du flag.
        """
        captcha = Captcha(self.url, self._http_session)
        captcha.capture()
        captcha.solve()
        self.captcha_value = captcha.get_value()
        self.flag_value = str(next(self._flag_iter))

    def submit_request(self):
        """
        Envoie le flag et la valeur du captcha au serveur.
        """
        self._response = self._http_session.post(
            self.url,
            data={"flag": self.flag_value, "captcha": self.captcha_value, "submit": "submit"},
            timeout=10,
        )

    def process_response(self):
        """
        Analyse la réponse du serveur.
        Retourne True si le flag est correct, False sinon.
        """
        if self._response is None:
            return False
        text = self._response.text
        if "Invalid captcha" in text or "Incorrect flag" in text:
            return False
        match = re.search(r'alert-success[^>]*>([^<]+)<', text)
        self.valid_flag = match.group(1).strip() if match else self.flag_value
        return True

    def get_flag(self):
        """
        Retourne le flag valide.
        """
        return self.valid_flag
