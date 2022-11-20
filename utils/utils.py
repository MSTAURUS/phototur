from functools import wraps
from flask import redirect, url_for, flash
import logging
from typing import Dict, List

from .vkrandomphoto import VKRandomPhoto


def exception(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logging.exception(f"Error on {e}")
            flash("Произошла непредвиденная ошибка", "error")
            return redirect(url_for("index"))

    return decorated_function


def stripex(value):
    return value.strip() if value else value


def get_photo_instagram(url: str) -> List[str]:
    pass


def get_photo_vk(url: str) -> List[Dict]:
    vk_photo: VKRandomPhoto = VKRandomPhoto(url=url)

    return vk_photo.get_random_photo(6)