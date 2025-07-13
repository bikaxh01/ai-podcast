import cloudinary.uploader
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from utils.utils import generate
from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import AzureChatOpenAI
from typing import List
import asyncio
from pydub import AudioSegment
from pydantic import BaseModel, Field
import cloudinary
import os

load_dotenv()
API_KEY = os.getenv("GEMINI_API")
CLOUD_NAME = os.getenv("CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

# project_data = {
# "id":"VSD34F5X9",
#     "prompt": "Make also conver what are ai agents",
#     "docKey": "mypdf.pdf",
#     "docUrl": "https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf",
# }

project_data = {
    "id": "VSD34F5X9",
    "prompt": "Generate a begineer friendly podcast on docker and k8s",
    "docKey": "",
    "docUrl": "https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf",
}


def parse_doc(doc_path: str):
    loader = PyPDFLoader(doc_path)
    doc_chunks = loader.load()
    doc_string = " ".join(doc.page_content for doc in doc_chunks)

    return doc_string


def document_filter(doc_content: str, user_prompt: str):
    prompt = PromptTemplate(
        template="""

You are a highly experienced content writer and text-cleaning specialist, skilled in refining raw document data for voice-based educational podcasts.

You will receive:
- A User Prompt indicating how the content should be used (e.g., podcast tone, format, focus or any topic use want's to add).
- Raw Content, which has been extracted from a parsed PDF and may include formatting artifacts, noise, and broken structures.

 Your Task:

Analyze the User Prompt and design your cleanup approach accordingly. Then clean the Raw Content while strictly and add any content if user want's following the below rules:

 CLEANING RULES:

 Clean and filter the raw content by removing:
- Unnecessary symbols or characters (e.g., ■, ###, ...)
- Garbled or incomplete lines
- Repeated metadata (e.g., "Page 1", "Scanned by...", "Confidential", etc.)
- Accidental line breaks and visual formatting glitches

 Preserve the content exactly:
- Do NOT paraphrase, summarize, or alter the original message
- Do NOT skip meaningful content
- Only fix sentence flow or formatting when absolutely necessary for readability

 Reconstruct layout and tone with care:
- Maintain structure (headings, lists, sections)
- Clarify only where needed, without reinterpreting the content
- The cleaned content should read as clear, continuous prose, as if originally typed
Important Notes:
- Your role is clean-up only, not rewriting or optimizing for tone unless stated in the User Prompt
- Do not infer or inject meaning
 Input Format:
User Prompt:
    {user_prompt}
Raw Content:
     {raw_content}   
 Output Format:
[Return the cleaned and well-structured version of the raw content,
formatted clearly, preserving all meaning, and ready for use in a podcast or other media as guided by the User Prompt.]

        
        """,
        input_variables=["raw_content,user_prompt"],
    )

    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=API_KEY,
        thinking_budget=0,
        max_output_tokens=10000,
    )
    chain = prompt | model
    final_content = chain.invoke(
        {"raw_content": doc_content, "user_prompt": user_prompt}
    )

    return final_content.content


def generate_content(user_prompt: str):
    prompt = PromptTemplate(
        template="""
  You are an expert content writer. Your task is to generate detailed, high-quality content based on the user prompt.

If the user has not specified the target audience, default to beginner-friendly content. Ensure the explanation is clear, thorough, and easy to understand.

Important:
- Only focus on the topic provided by the user.
- Do NOT generate podcast scripts, dialogues, or audiobook-style content.
- Your output should be detailed, well-organized explanatory content.
- This content will be used in a later phase to generate a podcast script, so focus solely on delivering informative written material.

Include:
- A clear explanation of the main topic
- All relevant subtopics, covered in depth
- Real-world examples wherever appropriate to aid understanding


        User prompt:
        {user_prompt}
        """,
        input_variables=["user_prompt", user_prompt],
    )
    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=API_KEY,
        thinking_budget=0,
        max_output_tokens=10000,
    )
    chain = prompt | model
    final_content = chain.invoke({"user_prompt": user_prompt}).content
    print(f"Content based on user prompt 👌 \n {final_content} \n")
    return final_content


def get_final_content():

    if project_data["docKey"]:
        print("Parsing the doc")
        raw_data = parse_doc(project_data["docUrl"])
        filtered_content = document_filter(raw_data, project_data["prompt"])
        return filtered_content
    else:
        print("User doc not found generating on promt...")
        content = generate_content(project_data["prompt"])
    return content


class PodcastResponseFormat(BaseModel):
    """
    Use this output format
    Host: [Beginner-friendly question or comment] Or
    Guest: [Clear, detailed explanation with examples]
    """

    response: List[str] = Field(
        description="This response list should contain the content eg: Host: [Beginner-friendly question or comment] or  Guest: [Clear, detailed explanation with examples] "
    )


def generate_podcast_script(content: str):
    prompt = PromptTemplate(
        template="""
        You are an expert content writer working for a podcast production company that produces high-quality, audio-based educational content.

Your task is to convert the provided content into a natural, engaging podcast-style script featuring two speakers:

Host:
- Curious, friendly, and relatable
- Asks beginner-friendly questions
- Guides the conversation and ensures clarity for the audience

Guest:
- Knowledgeable, warm, and articulate
- Breaks down concepts in simple language
- Explains complex terms with clear, relatable examples

Your Responsibilities:
- Convert the provided content into a detailed, expressive podcast conversation between the Host and Guest.
- Use a conversational and friendly tone throughout.
- Add natural expressions such as:
  “Ohh, I see.”, “Hmm, interesting.”, “That’s a good point.”, “Got it.” to keep the flow immersive and engaging.
- Ensure the conversation flows smoothly, gradually introducing and explaining each concept in an accessible way.
- For any technical or complex terms, ensure the Guest provides beginner-friendly examples.
- Cover the entire source content thoroughly and accurately—do not skip key points.
- Make sure the final script is long enough to support a 8–10 minute voiceover when read aloud.
- Avoid emojis and non-verbal sound effects unless necessary for comprehension.

Output format:
Host: [Beginner-friendly question or comment]   Or
Guest: [Clear, detailed explanation with examples]

Note: The podcast script should be engaging, informative, and easy to understand for a beginner audience, with clear expressions and explanations.

Content:
{content}
        """,
        input_variables=["content"],
    )
    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=API_KEY,
        thinking_budget=0,
        max_output_tokens=10000,
    )

    model_with_structure = model.with_structured_output(PodcastResponseFormat)
    chain = prompt | model_with_structure
    parser = PydanticOutputParser(pydantic_object=PodcastResponseFormat)
    final_content = chain.invoke({"content": content})
    return final_content.response


async def generate_podcast(script: List[str]):
    finalScript = [" ".join(script[i : i + 20]) for i in range(0, len(script), 20)]
    print(f"Podcast final script length {len(finalScript)} 😁")
    tasks = [generate(sc, i) for i, sc in enumerate(finalScript)]
    results = await asyncio.gather(*tasks)
    file_names = list(results)
    return file_names


def merge_media_files(files: list[str], project_id: str):

    merged_audio = AudioSegment.from_file(f"./media/{files[0]}", format="wav")
    for file in files[1:]:
        audio_data = AudioSegment.from_file(f"./media/{file}", format="wav")
        merged_audio += audio_data
    merged_audio.export(f"./media/{project_id}_final.wav", format="wav")
    print("Audio files merged successfully!")
    return f"{project_id}_final"


def upload_media(file_name: str,project_id:str):

    cloudinary.config(
        secure_url=True,
        cloud_name=CLOUD_NAME,
        api_key=CLOUDINARY_API_KEY,
        api_secret=CLOUDINARY_API_SECRET,
    )
    res = cloudinary.uploader.upload_large(
        f"./media/{file_name}.wav",
        resource_type="video",
        public_id=file_name,
        folder=f"EchoMind/{project_id}",
    )
    print(res["secure_url"])
    return res["secure_url"]


async def main():
    try:
        content = get_final_content()
        #  generate role based script
        podcast_script = generate_podcast_script(content)

     
        print(f"Podcast script length {len(podcast_script)} 🔥")
        files = await generate_podcast(podcast_script)
        final_media = merge_media_files(files,project_data["id"])
        media_url = upload_media(final_media,project_data["id"])
        print(media_url)
        os._exit(1)
    except Exception as e:
        print("Something went wrong \n",e)
        os._exit(1)
    # update the link and dialogs in db
    # Kill self


asyncio.run(main())
