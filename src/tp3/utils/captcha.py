import io
from urllib.parse import urljoin

import pytesseract
import requests
from PIL import Image


class Captcha:
    def __init__(self, url, http_session=None):
        self.url = url
        self.image = b""
        self.value = ""
        self._http_session = http_session or requests.Session()

    def capture(self):
        """
        Télécharge l'image du captcha via la session HTTP partagée.
        """
        captcha_url = urljoin(self.url, "../captcha.php")
        try:
            r = self._http_session.get(captcha_url, timeout=10)
            r.raise_for_status()
            self.image = r.content
        except requests.RequestException:
            self.image = b""

    def solve(self):
        """
        Résout le captcha par OCR (Tesseract) et stocke la valeur dans self.value.
        """
        if not self.image:
            return
        img = Image.open(io.BytesIO(self.image))
        self.value = pytesseract.image_to_string(
            img, config="--psm 7 -c tessedit_char_whitelist=0123456789"
        ).strip()

    def get_value(self):
        """
        Retourne la valeur résolue du captcha.
        """
        return self.value
