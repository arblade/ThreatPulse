import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "./components/ui/button";
import { Bookmark } from "lucide-react";
import { SideMenu } from "./SideMenu";

export default function Header() {
  return (
    <>
      <div className="flex flex-col border-r border-gray-200 h-screen">
        {" "}
        <div className="sticky top-0 h-[60px] flex w-full justify-center ">
          <div className="w-1/5 flex justify-start items-center pl-8 text-xl font-bold leading-7 font-['Inter']">
            <span className="text-gray-900 ">Threat</span>
            <span className="bg-gradient-to-r from-purple-600 to-purple-700 bg-clip-text text-transparent">
              Pulse
            </span>
          </div>
          <div className="w-4/5 flex justify-end pr-8 items-center"></div>
        </div>
        <div className="w-[calc(100vw-87vw)] ">
          <div className="ml-2 mt-4">
            {" "}
            <SideMenu />
          </div>
        </div>
        <div className="flex-grow flex-col">
          <div className="flex flex-col justify-end align-bottom items-end"></div>{" "}
        </div>
        <div className="mb-8 flex items-center space-x-4 justify-start ml-8 mt-4 text-md p-1 hover:bg-gray-100 rounded-lg mr-8 pl-2 py-2 hover:cursor-pointer">
          <Avatar className="h-8 w-8">
            <AvatarImage src="https://github.com/shadcn.png" />
            <AvatarFallback>CN</AvatarFallback>
          </Avatar>{" "}
          <div>Profile</div>
        </div>
      </div>
    </>
  );
}
