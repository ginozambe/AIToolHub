import sys
import re
import streamlit as st
import openai
from youtube_transcript_api import YouTubeTranscriptApi
import newspaper as nk


def openAI_generate_text(prompt, model, api_key):
    openai.api_key = api_key
    completion = openai.ChatCompletion.create(
        model=model, messages=[{"role": "user", "content": prompt}])
    return completion.choices[0].message.content


def get_article_from_url(url):
    try:
        # Scrape the web page for content using newspaper
        article = nk.Article(url)
        # Download the article's content with a timeout of 10 seconds
        article.download()
        # Check if the download was successful before parsing the article
        if article.download_state == 2:
            article.parse()
            # Get the main text content of the article
            article_text = article.text
            return article_text
        else:
            st.write("Error: Unable to download article from URL:", url)
            return None
    except Exception as e:
        st.write("An error occurred while processing the URL:", url)
        st.write(str(e))
        return None


def get_video_transcript(video_url):
    match = re.search(
        r"(?:youtube\.com\/watch\?v=|youtu\.be\/)(.*)", video_url)
    if match:
        VIDEO_ID = match.group(1)
    else:
        raise ValueError("Invalid YouTube URL")

    video_id = VIDEO_ID

    # Fetch the transcript using the YouTubeTranscriptApi
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    # Extract the text of the transcript
    transcript_text = ""
    for line in transcript:
        transcript_text += line["text"] + " "
    return transcript_text


def tool_1_yt_url(api_key):
    st.title("Youtube AI Automator")
    yt_url = st.text_area("Enter Youtube URL:")
    yt_user_prompt = st.text_area("Enter Prompt:")
    model = st.selectbox("Choose a model", [
                         "gpt-3.5-turbo-0125", "gpt-4-0125-preview"])

    if st.button("Generate"):
        video_transcript = get_video_transcript(yt_url)
        st.write("Video Scraped")
        st.write("Processing...")
        prompt = yt_user_prompt + video_transcript
        result = openAI_generate_text(prompt, model, api_key)
        st.markdown("### Result:")
        st.success("Successfully generated result!")
        st.write(result)


def tool_2_blog_url(api_key):
    st.title("Blog AI Automator")
    blog_url = st.text_input("Enter Blog URL:")
    blog_user_prompt = st.text_area("Enter Prompt:")
    model = st.selectbox("Choose a model", [
                         "gpt-3.5-turbo-0125", "gpt-4-0125-preview"])

    if st.button("Generate"):
        blog_article = get_article_from_url(blog_url)
        st.write("Article Scraped")
        st.write("Processing...")
        prompt = blog_user_prompt + blog_article
        result = openAI_generate_text(prompt, model, api_key)
        st.markdown("### Result:")
        st.success("Successfully generated result!")
        st.write(result)


def main():
    # Sidebar
    st.sidebar.header("Settings")

    # Input for OpenAI API key in the sidebar
    api_key = st.sidebar.text_input(
        "OpenAI API key", type="password")

    # Tool selection as a dropdown in the sidebar
    tool_selection = st.sidebar.selectbox(
        "Choose a tool", ["Youtube AI Automator", "Blog AI Automator"])

    # Depending on the tool selection, display the UI
    if tool_selection == "Youtube AI Automator":
        tool_1_yt_url(api_key)
    elif tool_selection == "Blog AI Automator":
        tool_2_blog_url(api_key)


if __name__ == "__main__":
    main()
