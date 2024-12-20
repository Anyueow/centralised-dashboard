import requests
import streamlit as st
import pandas as pd
import datetime
import os
import subprocess
from datetime import datetime
from src.scraping.cache_manager import CacheManager  # Assuming cache_manager.py is in the same directory


# ============================================
# Set Page Configuration
# ============================================
st.set_page_config(
    page_title="Movie Research Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================
# Custom CSS for Styling
# ============================================
def local_css():
    st.markdown("""
        <style>
            body {
                background-color: #f5f5f5;
            }
            .title {
                color: #2E3A59;
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                font-weight: bold;
                text-align: left;
                margin-bottom: 20px;
            }
            .subtitle {
                text-align: left;
                color: #555555;
                margin-bottom: 40px;
            }
            .section-title {
                font-size: 1.1em;
                color: #555555;
                margin-top: 10px;
                margin-bottom: 5px;
                font-weight: bold;
            }
            .recommendations {
                background-color: #e0f7fa;
                padding: 15px;
                border-radius: 10px;
                margin-top: 20px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            .ratings-list {
                list-style-type: none;
                padding-left: 0;
            }
            .ratings-list li {
                padding: 5px 0;
                border-bottom: 1px solid #e0e0e0;
            }
            .stButton>button {
                background-color: #2E3A59;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 1em;
                cursor: pointer;
            }
            .stButton>button:hover {
                background-color: #1B2A40;
            }
            .stTextInput>div>div>input {
                border-radius: 5px;
                padding: 10px;
                border: 1px solid #ccc;
            }
            .stSelectbox>div>div>div>div>select {
                border-radius: 5px;
                padding: 10px;
                border: 1px solid #ccc;
            }
            @media (max-width: 768px) {
                .columns {
                    flex-direction: column;
                }
                .columns > div {
                    width: 100% !important;
                }
            }
        </style>
    """, unsafe_allow_html=True)

local_css()

# ============================================
# Helper Functions
# ============================================
def render_section(title, content):
    section_html = f"""
    <div>
        <div class="section-title">{title}</div>
        <div>{content}</div>
    </div>
    """
    st.markdown(section_html, unsafe_allow_html=True)

def render_ratings(ratings):
    ratings_html = '<ul class="ratings-list">'
    for key, value in ratings.items():
        ratings_html += f"<li><strong>{key}:</strong> {value}</li>"
    ratings_html += '</ul>'
    st.markdown(ratings_html, unsafe_allow_html=True)

def display_movies(filtered_df, expand_all):
    for i, (index, row) in enumerate(filtered_df.iterrows(), 1):
        trend_score = row.get('Trending Score', 'N/A')

        # Determine emoji color based on trend score
        if trend_score == 'N/A':
            emoji = '⚫'
        else:
            try:
                score_val = float(trend_score)
                if score_val > 75:
                    emoji = '🟢'
                elif 60 <= score_val <= 75:
                    emoji = '🟡'
                else:
                    emoji = '🔴'
            except ValueError:
                emoji = '⚫'

        # Extract the release date and format it
        release_date = row.get('Release Date (Theaters)', 'N/A')


        formatted_release_date = f"| {release_date.strftime('%b-%d')}"  # Bold and italic format

        expander_label = f"**{row.get('Movie Name', 'N/A')} {formatted_release_date}**   {emoji} {trend_score}"

        with st.expander(expander_label, expanded=expand_all):
            col1, col2 = st.columns([3, 3])

            with col1:


                # Director, Actors, Genres
                render_section("Director", row.get('Director', 'N/A'))
                render_section("Actors", row.get('Actors', 'N/A'))
                render_section("Genres", row.get('Genres', 'N/A'))

                theater_date = row.get('Release Date (Theaters)')
                streaming_date = row.get('Release Date (Streaming)')

                theater_date_str = theater_date.strftime("%b %d, %Y") if theater_date else "N/A"
                streaming_date_str = streaming_date.strftime("%b %d, %Y") if streaming_date else "N/A"

                render_section("Theater Release Date", theater_date_str)
                render_section("Streaming Release Date", streaming_date_str)

                render_section("Runtime", row.get('Runtime', 'N/A'))

                # Awards
                render_section("Awards", row.get('Awards', 'No awards available.'))

                # SEO Keywords
                seo_keywords = row.get('SEO Keywords', "No SEO Keywords")
                render_section("SEO Keywords", seo_keywords)

                # Image rendering
                image_url = row.get('Poster', None)
                print(row)  # Debugging line to see the row content

                try:
                    # Fetch the image content for download
                    response = requests.get(image_url)
                    response.raise_for_status()  # Raise an exception for HTTP errors
                    image_data = response.content

                    # Add custom spacing to create more padding
                    st.markdown("<br>", unsafe_allow_html=True)  # Adds space before the button

                    st.download_button(
                        label=f"Download {row['Movie Name']} Image",
                        data=image_data,
                        file_name=f"{row['Movie Name'].replace(' ', '_')}.jpg",
                        mime="image/jpeg"
                    )
                except requests.exceptions.RequestException as e:
                    st.error(f"Error fetching image: {e}")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")



            with col2:

                # Ratings
                st.markdown("<div class='section-title'>Ratings:</div>", unsafe_allow_html=True)
                ratings = {
                    'IMDb Rating': row.get('IMDb Rating', 'N/A'),
                    'Rotten Tomatoes': row.get('Rotten Tomatoes Rating', 'N/A'),
                    'Metacritic': row.get('Metacritic Rating', 'N/A'),
                    'Metascore': row.get('Metascore', 'N/A'),
                    'IMDb Votes': row.get('IMDb Votes', 'N/A')
                }
                render_ratings(ratings)

                # Synopsis
                render_section("Synopsis", row.get('Synopsis', 'No synopsis available.'))

                # Sentiment Analysis
                render_section("Sentiment Analysis", row.get('Sentiment Analysis', 'No analysis available'))



# ============================================
# Main Function
# ============================================
def main():
    st.markdown('<h1 class="title">Direct TV SEO Movie Research Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Trending Top movies, sources: Rotten Tomatoes, IMDB, Google, Wikipedia, Twitter.</p>", unsafe_allow_html=True)

    # Initialize CacheManager
    cache = CacheManager()

    # Check if cache is valid and load data
    if cache.is_cache_valid():
        df = cache.load_cache()
        # Show last updated
        cache_file = cache.cache_file
        mod_time = datetime.fromtimestamp(os.path.getmtime(cache_file))
        st.sidebar.write(f"**Data Last Updated:** {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")

        # Button to force refresh
        if st.button("Force Refresh Data"):
            # Run the `run_with_cache.py` script to update cache
            subprocess.run(["python", "run_with_cache.py"], check=True)
            # Reload page to reflect the new data
            st.experimental_set_query_params(reload="1")
            st.experimental_rerun()
    else:
        st.warning("No valid cache found. Please refresh the data.")
        if st.button("Generate New Cache"):
            # Run the `run_with_cache.py` script to generate a new cache
            subprocess.run(["python", "run_with_cache.py"], check=True)
            st.experimental_set_query_params(reload="1")
            st.experimental_rerun()
        return

    search_query = st.text_input("Search by Movie Name, Director, Actor, or Genre", "")
    sort_option = st.selectbox("Sort movies by:",
                               ["Trending Score",  # Default option should be trending score
                                "Movie Name",
                                "Release Date (Streaming)",
                                "Release Date (Theaters)"])

    # If no sort option is selected, default to Trending Score
    if sort_option == "Movie Name":
        df = df.sort_values(by='Movie Name')
    elif sort_option == "Release Date (Streaming)":
        # Sort by Streaming Release Date (descending)
        df = df.sort_values(by='Release Date (Streaming)', ascending=False, na_position='last')
    elif sort_option == "Release Date (Theaters)":
        # Sort by Theatrical Release Date (descending)
        df = df.sort_values(by='Release Date (Theaters)', ascending=False, na_position='last')
    else:
        # Default is score (descending)
        df = df.sort_values(by='Trending Score', ascending=False)

    col2, col3, cc = st.columns([1, 1, 5])

    with col2:
        if st.button("Expand All"):
            st.session_state['expand_all'] = True
    with col3:
        if st.button("Collapse All"):
            st.session_state['expand_all'] = False

    if 'expand_all' not in st.session_state:
        st.session_state['expand_all'] = False

    if search_query:
        search_query_lower = search_query.lower()
        filtered_df = df[
            df.apply(lambda row:
                     search_query_lower in str(row['Movie Name']).lower() or
                     search_query_lower in str(row.get('Director', '')).lower() or
                     search_query_lower in str(row.get('Genres', '')).lower() or
                     search_query_lower in str(row.get('Actors', '')).lower(),
                     axis=1)
        ]
    else:
        filtered_df = df

    display_movies(filtered_df, st.session_state['expand_all'])

if __name__ == "__main__":
    main()
