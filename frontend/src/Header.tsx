import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "./components/ui/button";
import { Bookmark } from "lucide-react";

export default function Header() {
  return (
    <>
      <div className="sticky top-0 h-[50px] flex w-full justify-center">
        <div className="w-1/5 flex justify-start items-center pl-8 text-xl font-bold leading-7 font-['Inter']">
          <span className="text-gray-900 ">Threat</span>
          <span className="bg-gradient-to-r from-purple-600 to-purple-700 bg-clip-text text-transparent">
            Pulse
          </span>
        </div>
        <div className="w-4/5 flex justify-end pr-8 items-center">
          <div className="flex space-x-4">
            <div className="mr-2">
              <Button variant="outline" size={"sm"} className="flex space-x-2">
                <Bookmark size={16} />
                <div> Saved</div>
              </Button>
            </div>
            <Avatar className="h-8 w-8">
              <AvatarImage src="https://github.com/shadcn.png" />
              <AvatarFallback>CN</AvatarFallback>
            </Avatar>
          </div>{" "}
        </div>
      </div>
    </>
  );
}
