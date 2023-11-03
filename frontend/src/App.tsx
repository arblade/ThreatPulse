import { useState } from "react";
import { QueryClient, QueryClientProvider } from "react-query";

import "./App.css";
import "./global.css";
import { Body } from "./Body";
import Header from "./Header";
import { Toaster } from "./components/ui/toaster";

function App() {
  const queryClient = new QueryClient();
  return (
    <QueryClientProvider client={queryClient}>
      <div className="flex">
        <Header />
        <Body />
        <Toaster />
      </div>
    </QueryClientProvider>
  );
}

export default App;
