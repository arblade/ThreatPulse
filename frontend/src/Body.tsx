import { useEffect, useState } from "react";
import { Card } from "./Card";
import { SideMenu } from "./SideMenu";

export interface Article {
  title: string;
  description: string;
  image_url: string;
  badges: string[];
  link: string;
  source: string;
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
      <div className="flex">
        <div className="w-[calc(100vw-17vw)] mt-5    flex flex-col">
          <div className="text-center text-2xl my-10 font-bold text-gray-800 ">
            Welcome hunter, your{" "}
            <span className="bg-gradient-to-r from-purple-600 to-purple-700 bg-clip-text text-transparent">
              feed
            </span>{" "}
            of the day is here ...
          </div>
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
      </div>
    </>
  );
}
