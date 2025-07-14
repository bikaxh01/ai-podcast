from dotenv import load_dotenv
import shutil
from utils.utils import (
    get_final_content,
    generate_podcast_script,
    generate_podcast,
    merge_media_files,
    upload_media,
    ProjectData
)
import asyncio
import ast
import os

load_dotenv()

id = os.getenv("PROJECT_ID")

#get_data
project_data = {
    "id": "Bikaxh12",
    "prompt": "Generate a begineer friendly podcast on docker and k8s",
    "docKey": "",
    "docUrl": "https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf",
}



print(id)




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
        os._exit(0)    
    except Exception as e:
        print("Something went wrong \n", e)
        shutil.rmtree("./media",ignore_errors=True)   
        os._exit(0)    
        
        
    


asyncio.run(main())
