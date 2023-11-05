import json
import datetime
from dataclasses import dataclass

from ..newsfeed.features import Feature


@dataclass
class Article:
    id: int
    title: str
    description: str
    illustration: str
    url: str
    date_scraped: datetime
    file_path: str
    features: list[Feature]
    keywords: list[str]
    source: str

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
        features = [Feature.from_json(f) for f in json.loads(row[7])]
        keywords = json.loads(row[8])

        return Article(
            id=row[0],
            title=row[1],
            description=row[2],
            illustration=row[3],
            url=row[4],
            date_scraped=row[5],
            file_path=row[6],
            features=features,
            keywords=[a[0] for a in keywords],
            source=row[9],
        )
