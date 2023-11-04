import json
import datetime
from dataclasses import dataclass

from ..newsfeed.features import Feature

@dataclass
class Article:
    id: int
    url: str
    date_scraped: datetime
    file_path: str
    features: list[Feature]
    keywords: list[str]
    
    def serialize_features(self) -> str:
        ft_list = [f.to_json() for f in self.features]
        return json.dumps(ft_list)
    
    def serialize_keywords(self) -> str:
        return json.dumps(self.keywords)
    
    def get_text(self) -> str:
        with open(self.file_path, "r") as f:
            return f.read()
        
    @staticmethod
    def from_row(row) -> "Article":
        features = [Feature.from_json(f) for f in json.loads(row[4])]
        keywords = json.loads(row[5])
        
        return Article(row[0], row[1], row[2], row[3], features, keywords)