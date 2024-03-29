from uuid import uuid4
import requests
from typing import Dict
from bs4 import BeautifulSoup
from dataclasses import dataclass, field
import re
from models.model import Model


@dataclass(eq=False)
class Item(Model):
    collection: str = field(init=False, default='items')
    url: str
    tag_name: str
    query: Dict
    price: float = field(default=None)
    _id: str = field(default_factory=lambda: uuid4().hex)

    def load_price(self) -> float:
        response = requests.get(self.url)
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        element = soup.find(self.tag_name, self.query)
        string_prince = element.text.strip()

        pattern = re.compile(r'((\d+,)?\d+\.\d+)')
        match = pattern.search(string_prince)
        found_price = match.group(0)
        without_commas = found_price.replace(',', '')
        self.price = float(without_commas)
        return self.price

    def json(self) -> Dict:
        return {
            '_id': self._id,
            'url': self.url,
            'tag_name': self.tag_name,
            'price': self.price,
            'query': self.query
        }
