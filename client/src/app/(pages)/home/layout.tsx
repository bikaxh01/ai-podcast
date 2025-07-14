import React from "react";
import Nav from "./_components/Nav";

function layout({ children }: { children: React.ReactNode }) {
  return (
    <div>
      <Nav />
      {children}
    </div>
  );
}

export default layout;
