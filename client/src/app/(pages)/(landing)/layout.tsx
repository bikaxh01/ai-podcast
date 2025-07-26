import React, { ReactNode } from "react";
import Nav from "../home/_components/Nav";

function layout({ children  }: { children: ReactNode }) {
  return (
    <div>
      <Nav isLanding={true} />
      <div className=" px-[10rem]">{children}</div>
    </div>
  );
}

export default layout;
