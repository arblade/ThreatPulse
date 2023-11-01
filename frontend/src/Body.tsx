import { useEffect, useState } from "react";
import { Card } from "./Card";

export interface Article {
  title: string;
  description: string;
  image_url: string;
  badges: string[];
}

export function Body() {
  const [articles, setArticles] = useState<Article[]>([]);
  useEffect(() => {
    fetch(window.origin + "/api/get_articles")
      .then((data) => {
        return data.json();
      })
      .then((data) => {
        setArticles(data);
      });
  }, []);
  return (
    <>
      <div className="mx-16 mt-10 flex flex-col">
        <div className="flex justify-start items-center flex-col space-y-2">
          <div className="flex flex-col space-y-4">
            {" "}
            {articles.map((art) => (
              <div>
                <Card article={art} />
              </div>
            ))}
          </div>
        </div>
      </div>
    </>
  );
}
