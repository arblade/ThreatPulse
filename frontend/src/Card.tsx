import { Article } from "./Body";
import { Badge } from "@/components/ui/badge";
export function Card({ article }: { article: Article }) {
  return (
    <>
      <div className="rounded-lg max-w-[40rem] max-h-[8rem] break-words">
        <div className="flex space-x-4">
          <div className="object-fill max-h-5rem max-w-5rem inline-flex ">
            <img
              src={article.image_url}
              className="w-[13rem] h-[8rem] min-w-[13rem] min-h-[8rem] object-cover rounded-xl"
            />
          </div>
          <div className="">
            {" "}
            <div className="font-semibold">{article.title}</div>
            <div className="font-normal text-gray-600 mt-1 max-h-[4.5rem] overflow-clip">
              {article.description}
            </div>
            <div className="flex space-x-1 mt-1 mb-0.5">
              {article.badges.map((bg) => (
                <div className="">
                  {" "}
                  <Badge variant="outline">{bg}</Badge>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
