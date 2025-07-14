import React from "react";
import EditPlan from "./_components/EditPlan";

async function Project({ params }: { params: Promise<{ projectId: string }> }) {
  const { projectId } = await params;

  return (
    <div>
      <EditPlan projectId={projectId} />
    </div>
  );
}

export default Project;
