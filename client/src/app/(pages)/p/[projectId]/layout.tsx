import React, { ReactNode } from "react";
import Nav from "../../home/_components/Nav";

function layout({ children }: { children: ReactNode }) {
  return (
    <div>
      <Nav />
      {children}
    </div>
  );
}

export default layout;
