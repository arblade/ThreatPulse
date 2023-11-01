import { useState } from "react";

import "./App.css";
import "./global.css";
import { Body } from "./Body";
import Header from "./Header";

function App() {
  return (
    <div className="flex">
      <Header />
      <Body />
    </div>
  );
}

export default App;
