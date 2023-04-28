

import re


class Slug:
    __slug: str

    def __init__(self, slug) -> None:
        self.__slug = slug

    @staticmethod
    def create(text):
        if isinstance(text, str):
            slug = Slug.slugify(text)
            return Slug(slug)
        else:
            raise ValueError("Type Error")
        
    def get_slug(self):
        return self.__slug

    def slugify(text):
        text = re.sub(r'[^\w\s-]', '', text).strip().lower()
        text = re.sub(r'[-\s]+', '-', text)
        return text
            
