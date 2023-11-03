import { Sword, ShipWheel, Bookmark } from "lucide-react";
import { useState } from "react";
export function SideMenu() {
  const [activeMode, setActiveMode] = useState("Vigil");
  return (
    <div className="">
      <div className="flex flex-col space-y-2 ml-4  text-lg mr-4 font-medium ">
        <div
          className={`flex items-center justify-start space-x-3 hover:bg-gray-100 px-2 py-1 hover:cursor-pointer rounded-lg pl-4 ${
            activeMode == "Vigil" ? "text-purple-600" : ""
          }`}
        >
          <ShipWheel size={20} /> <div>Vigil</div>
        </div>
        <div className="flex items-center justify-start  space-x-3  hover:bg-gray-100 px-2 py-1 hover:cursor-pointer rounded-lg pl-4">
          <Sword size={20} /> <div>Hunt</div>
        </div>
        <div className="flex items-center justify-start space-x-3  hover:bg-gray-100 px-2 py-1 hover:cursor-pointer rounded-lg pl-4">
          <Bookmark size={20} /> <div>Favorites</div>
        </div>
      </div>
    </div>
  );
}
