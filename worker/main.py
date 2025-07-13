from dotenv import load_dotenv
import shutil
from utils.utils import (
    get_final_content,
    generate_podcast_script,
    generate_podcast,
    merge_media_files,
    upload_media,
)
import asyncio
import os

load_dotenv()


project_data = {
"id":"VSD34F5X9CCCC",
    "prompt": "Make also conver what are ai agents",
    "docKey": "mypdf.pdf",
    "docUrl": "https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf",
}

# project_data = {
#     "id": "VSD34X9",
#     "prompt": "Generate a begineer friendly podcast on docker and k8s",
#     "docKey": "",
#     "docUrl": "https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf",
# }


async def main():
    try:
        content = get_final_content(project_data)
        #  generate role based script
        podcast_script = generate_podcast_script(content)

        print(f"Podcast script length {len(podcast_script)} 🔥")
        files = await generate_podcast(podcast_script)
        final_media = merge_media_files(files, project_data["id"])
        media_url = upload_media(final_media, project_data["id"])
    # update the link and dialogs in db
        
        print(media_url)
        shutil.rmtree("./media")     
    except Exception as e:
        print("Something went wrong \n", e)
        shutil.rmtree("./media",ignore_errors=True)   
        
        
    


asyncio.run(main())
