import React from "react";


async function Project({ params }: { params: Promise<{ projectId: string }> }) {
  const { projectId } = await params;

  return (
    <div>
      {projectId}
    </div>
  );
}

export default Project;
