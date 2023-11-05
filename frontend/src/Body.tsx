import { useEffect, useState } from "react";
import { Card } from "./Card";
import { SideMenu } from "./SideMenu";
import { useQuery } from "react-query";
import Loader from "./components/Loader";
import { useToast } from "@/components/ui/use-toast";
import { Toaster } from "@/components/ui/toaster";
export interface Article {
  title: string;
  description: string;
  image_url: string;
  badges: string[];
  link: string;
  source: string;
}

export function Body() {
  const { toast } = useToast();
  const {
    isLoading,
    error,
    data: articles,
  } = useQuery<Article[], Error>("repoData", () => {
    return fetch("/api/get_articles").then((res) => {
      if (!res.ok) {
        throw new Error(res.statusText);
      }
      return res.json();
    });
  });
  useEffect(() => {
    if (error) {
      toast({
        title: "Network error",
        description: error.message,
      });
    }
  }, [error, toast]);

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
              {isLoading ? (
                <Loader />
              ) : (
                <div>
                  {articles &&
                    articles!.map((art) => (
                      <div key={"art_" + art.title}>
                        <Card article={art} />
                      </div>
                    ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
