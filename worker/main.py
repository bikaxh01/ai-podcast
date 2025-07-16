from dotenv import load_dotenv
import shutil
from utils.utils import (
    get_final_content,
    generate_podcast_script,
    generate_podcast,
    merge_media_files,
    upload_media,
    ProjectData,
    update_project,
)
import asyncio
import http
import os

load_dotenv()


# get_data
# project_data = {
#     "id": "Bikaxh12",
#     "prompt": "Generate a begineer friendly podcast on docker and k8s",
#     "docKey": "",
#     "docUrl": "https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf",
# }


project_id = os.getenv("PROJECT_ID")


async def main():
    try:

        # update status

        project_data = update_project(project_id, {"status": "PROCESSING"})

        content = get_final_content(project_data)
        #  generate role based script
        podcast_script = generate_podcast_script(content)
       

        files = await generate_podcast(podcast_script.response)
        final_media = merge_media_files(files, project_data["id"])
        media_url = upload_media(final_media, project_data["id"])
        # update the link and dialogs in db

        print(media_url)
        update_project(
            project_id,
            {
                "status": "COMPLETED",
                "audio_url": media_url,
                "title": podcast_script.title,
                "description": podcast_script.description,
            },
        )
        shutil.rmtree("./media")
        os._exit(0)
    except Exception as e:
        update_project(project_id, {"status": "FAILED"})
        print("Something went wrong \n", e)
        shutil.rmtree("./media", ignore_errors=True)
        os._exit(0)


asyncio.run(main())
