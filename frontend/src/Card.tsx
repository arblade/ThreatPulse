import { Article } from "./Body";
import { Badge } from "@/components/ui/badge";
import { Bookmark } from "lucide-react";
export function Card({ article }: { article: Article }) {
  return (
    <>
      <div className="rounded-lg max-w-[40rem] max-h-[9rem] break-words hover:bg-gray-100 py-1 px-1 hover:cursor-pointer rounded-xl">
        <div className="flex space-x-4">
          <div className="object-fill max-h-5rem max-w-5rem inline-flex relative">
            <img
              src={article.image_url}
              className="w-[13rem] h-[8rem] min-w-[13rem] min-h-[8rem] object-cover rounded-xl"
            />
            <div className="absolute bottom-[0.25rem] right-1">
              <Badge>{article.source}</Badge>
            </div>
          </div>
          <div className="">
            {" "}
            <div className="font-semibold mt-1 flex relative ">
              <div>{article.title} </div>
              <div className="hover:bg-gray-200 rounded-lg p-1 absolute right-1">
                <Bookmark size={16} className="text-gray-800" />
              </div>
            </div>
            <div className="font-normal text-gray-600 mt-1 max-h-[4rem] overflow-clip text-[0.9rem]">
              {article.description}
            </div>
            <div className="flex space-x-1 mt-1 mb-[0.2rem] relative">
              <div className="flex space-x-1">
                {article.badges.map((bg) => (
                  <div className="">
                    {" "}
                    <Badge variant="outline">{bg}</Badge>
                  </div>
                ))}
              </div>
              <div></div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
