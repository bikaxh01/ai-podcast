from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("GEMINI_API")


project_data = {
    "prompt": "Make also conver what are ai agents",
    "docKey": "mypdf.pdf",
    "docUrl": "https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf",
}

# project_data = {
#     "prompt": "Generate a begineer friendly podcast on docker",
#     "docKey": "",
#     "docUrl": "https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf",
# }


def parse_doc(doc_path: str):
    loader = PyPDFLoader(doc_path)
    doc_chunks = loader.load()
    doc_string = " ".join(doc.page_content for doc in doc_chunks)

    return doc_string


def document_filter(doc_content: str, user_prompt: str):
    prompt = PromptTemplate(
        template="""
  
 PDF Cleanup Master Prompt for Podcast Preparation

You are a highly experienced content writer and text-cleaning specialist, skilled in refining raw document data for voice-based educational podcasts.

You will receive:
- A User Prompt indicating how the content should be used (e.g., podcast tone, format, focus).
- Raw Content, which has been extracted from a parsed PDF and may include formatting artifacts, noise, and broken structures.

 Your Task:

Analyze the User Prompt and design your cleanup approach accordingly. Then clean the Raw Content while strictly following the below rules:

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

    model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=API_KEY)
    chain = prompt | model
    final_content = chain.invoke(
        {"raw_content": doc_content, "user_prompt": user_prompt}
    )

    return final_content.content


def generate_content(user_prompt: str):
    prompt = PromptTemplate(
        template="""
    You are an expert content writer. Your task is to generate detailed content based on the user prompt.

If the user has not specified the target audience, default to beginner-friendly content. Ensure the explanation is clear, thorough, and easy to understand.

Cover the main topic along with all relevant subtopics in depth, providing a complete and informative overview.


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


def main():
    content = get_final_content()
    #  generate role based script 
    #  Generate content audio
    #  push to store 
    print(content)


main()
