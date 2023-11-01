from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()


class Article(BaseModel):
    title: str
    description: str
    image_url: str
    badges: List[str]


# Exemple de données
articles = [
    Article(
        title="Article 1",
        description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas vel malesuada quam. Donec lacus leo, lobortis at nunc eu, blandit pharetra nisi. Ut sed interdum nunc. Ut venenatis tincidunt metus, a inter",
        image_url="https://www.kaspersky.fr/content/fr-fr/images/repository/isc/2021/threat_intelligence_1.jpg",
        badges=["ioc", "sigma", "yara"],
    ),
    Article(
        title="Article 2",
        description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas vel malesuada quam. Donec lacus leo, lobortis at nunc eu, blandit pharetra nisi. Ut sed interdum nunc. Ut venenatis tincidunt metus, a inter",
        image_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRdjWEZj_RoocKt88H8MUO21ewpqqAfiNx53YZcCG5Riq3nOkX7viEeu3YoE70lVXs0uU4&usqp=CAU",
        badges=["ioc"],
    ),
    Article(
        title="Article 3",
        description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas vel malesuada quam. Donec lacus leo, lobortis at nunc eu, blandit pharetra nisi. Ut sed interdum nunc. Ut venenatis tincidunt metus, a inter",
        image_url="https://media.licdn.com/dms/image/D4E22AQHziIXko3SWEg/feedshare-shrink_2048_1536/0/1681369734931?e=2147483647&v=beta&t=p56kBEbx_80t4KBfRlV9yJ6wDF2ctvO-GiXpH9vyi0M",
        badges=["yara"],
    ),
]


@app.get("/get_articles", response_model=List[Article])
def get_articles():
    return articles
