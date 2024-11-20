import streamlit as st
import pandas as pd

# Import the function to get the movie data
def get_movie_data():
    from src.scraping.run_scraper import get_movie_data as fetch_movie_data
    return fetch_movie_data()

# Import the function to add trending scores
from add_scores import add_scores  # Assuming you have this function to add the 'Trending Score'

# Custom CSS for styling
def local_css():
    st.markdown("""
        <style>
            /* Card Container */
            .card {
                background-color: #ffffff;
                padding: 20px;
                margin: 20px 0;
                border-radius: 15px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }

            /* Header */
            .header {
                display: flex;
                align-items: center;
                justify-content: space-between;
            }

            .header h3 {
                margin: 0;
                font-size: 1.5em;
                color: #333333;
            }

            /* Trending Score Badge */
            .badge {
                width: 60px;
                height: 60px;
                border-radius: 50%;
                background-color: #4CAF50;
                color: white;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                font-size: 1em;
            }

            /* Section Titles */
            .section-title {
                font-size: 1.2em;
                color: #555555;
                margin-top: 15px;
                margin-bottom: 5px;
            }

            /* Recommendations Box */
            .recommendations {
                background-color: #f0f0f0;
                padding: 15px;
                border-radius: 10px;
                margin-top: 20px;
                margin-bottom: 20px;
            }

            /* Ratings List */
            .ratings-list {
                list-style-type: none;
                padding-left: 0;
            }

            .ratings-list li {
                padding: 5px 0;
                border-bottom: 1px solid #e0e0e0;
            }

            /* Responsive Columns */
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

# Apply the custom CSS
local_css()

# Helper functions
def render_header(movie_name, trending_score):
    header_html = f"""
    <div class="header">
        <h3>{movie_name}</h3>
        <div class="badge">{trending_score}</div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)

def render_section(title, content):
    section_html = f"""
    <div>
        <div class="section-title"><strong>{title}</strong></div>
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

def render_recommendations(seo_keywords, trend_recommendation):
    recommendations_html = f"""
    <div class="recommendations">
        <p><strong>SEO Keywords:</strong> {seo_keywords}<br>
        <strong>Trend Recommendation:</strong> {trend_recommendation}</p>
    </div>
    """
    st.markdown(recommendations_html, unsafe_allow_html=True)

def main():
    # Set page layout for the Streamlit app
    st.set_page_config(layout="wide")
    st.title("Direct TV SEO Movie Research Dashboard")
    st.markdown("View movie details and insights.")

    # Fetch movie data (using the cached approach)
    try:
        movie_df = get_movie_data()
    except Exception as e:
        st.error(f"Error loading movie data: {e}")
        return

    # Calculate and add 'Trending Score'
    movie_df = add_scores(movie_df)

    # Optional: Search functionality
    search_query = st.text_input("Search by Movie Name, Director, Actor, or Genre", "")

    # Sorting option
    sort_option = st.selectbox("Sort movies by:", ["Movie Name", "Trending Score"])
    if sort_option == "Trending Score":
        movie_df['Trending Score Numeric'] = pd.to_numeric(movie_df['Trending Score'], errors='coerce')
        movie_df = movie_df.sort_values(by='Trending Score Numeric', ascending=False)
    else:
        movie_df = movie_df.sort_values(by='Movie Name')

    # Remove the temporary 'Trending Score Numeric' column
    movie_df = movie_df.drop(columns=['Trending Score Numeric'], errors='ignore')

    # Create columns for expand/collapse buttons
    col2, col3, cc = st.columns([0.5, 0.5, 5])

    # Expand/Collapse buttons
    with col2:
        expand_all = st.button("Expand All")
    with col3:
        collapse_all = st.button("Collapse All")

    # Filter the DataFrame based on the search query
    if search_query:
        filtered_df = movie_df[
            movie_df.apply(lambda row:
                           search_query.lower() in str(row['Movie Name']).lower() or
                           search_query.lower() in str(row.get('Director', '')).lower() or
                           search_query.lower() in str(row.get('Genres', '')).lower() or
                           search_query.lower() in str(row.get('Actors', '')).lower(),
                           axis=1)
        ]
    else:
        filtered_df = movie_df

    # Display movies
    display_movies(filtered_df, expand_all, collapse_all)

def display_movies(filtered_df, expand_all, collapse_all):
    """
    Display movie information with expandable sections.
    """
    # Determine expand state
    expand_state = True if expand_all else False if collapse_all else True

    for i, (index, row) in enumerate(filtered_df.iterrows(), 1):
        with st.expander(f"{i}. {row['Movie Name']}", expanded=expand_state):
            # Create two equal-width columns
            col1, col2 = st.columns([3, 3])

            with col1:
                # Render Header
                trending_score = row.get('Trending Score', 'N/A')
                render_header(row['Movie Name'], trending_score)

                # Render Director, Actors, Genres
                render_section("Director", row.get('Director', 'N/A'))
                render_section("Actors", row.get('Actors', 'N/A'))
                render_section("Genres", row.get('Genres', 'N/A'))

                # Render Synopsis
                render_section("Synopsis", row.get('Synopsis', 'No synopsis available.'))

                # Render Ratings
                st.markdown("**Ratings:**", unsafe_allow_html=True)
                ratings = {
                    'IMDb Rating': row.get('IMDb Rating', 'N/A'),
                    'Rotten Tomatoes': row.get('Rotten Tomatoes Rating', 'N/A'),
                    'Metacritic': row.get('Metacritic Rating', 'N/A'),
                    'Metascore': row.get('Metascore', 'N/A'),
                    'IMDb Votes': row.get('IMDb Votes', 'N/A')
                }
                render_ratings(ratings)

                # Render Release Dates and Runtime
                render_section("Theater Release Date", row.get('Release Date (Theaters)', 'N/A'))
                render_section("Streaming Release Date", row.get('Release Date (Streaming)', 'N/A'))
                render_section("Runtime", row.get('Runtime', 'N/A'))

            with col2:
                # Render Sentiment Analysis
                render_section("Sentiment Analysis", row.get('Sentiment Analysis', 'No analysis available'))

            # Render SEO and Trend Recommendations
            render_recommendations(
                row.get('SEO Keywords', 'Recommended keywords for promotion'),
                row.get('Trend Recommendation', 'Potential peak audience engagement period')
            )

if __name__ == "__main__":
    main()
