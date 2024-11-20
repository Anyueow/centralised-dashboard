import streamlit as st
import pandas as pd

# ============================================
# Set Page Configuration
# ============================================
st.set_page_config(
    page_title="Direct TV SEO Movie Research Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================
# Custom CSS for Styling
# ============================================
def local_css():
    st.markdown("""
        <style>
            /* Overall App Styling */
            body {
                background-color: #f5f5f5;
            }

            /* Title Styling */
            .title {
                color: #2E3A59;
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                font-weight: bold;
                text-align: center;
                margin-bottom: 20px;
            }

            /* Subtitle Styling */
            .subtitle {
                text-align: center;
                color: #555555;
                margin-bottom: 40px;
            }

            /* Section Titles */
            .section-title {
                font-size: 1.1em;
                color: #555555;
                margin-top: 10px;
                margin-bottom: 5px;
                font-weight: bold;
            }

            /* Recommendations Box */
            .recommendations {
                background-color: #e0f7fa;
                padding: 15px;
                border-radius: 10px;
                margin-top: 20px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
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

            /* Button Styling */
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

            /* Input Styling */
            .stTextInput>div>div>input {
                border-radius: 5px;
                padding: 10px;
                border: 1px solid #ccc;
            }

            /* SelectBox Styling */
            .stSelectbox>div>div>div>div>select {
                border-radius: 5px;
                padding: 10px;
                border: 1px solid #ccc;
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

# ============================================
# Helper Functions for Reusable Components
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

def render_recommendations(seo_keywords, trend_recommendation):
    recommendations_html = f"""
    <div class="recommendations">
        <p><strong>SEO Keywords:</strong> {seo_keywords}<br>
        <strong>Trend Recommendation:</strong> {trend_recommendation}</p>
    </div>
    """
    st.markdown(recommendations_html, unsafe_allow_html=True)

# ============================================
# Data Fetching Function
# ============================================

@st.cache_data
def get_movie_data():
    from src.scraping.run_scraper import get_movie_data as fetch_movie_data
    return fetch_movie_data()

# ============================================
# Main Function to Run the App
# ============================================

def main():
    # Title and Subtitle
    st.markdown('<h1 class="title">Direct TV SEO Movie Research Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>View movie details and insights.</p>", unsafe_allow_html=True)

    # Fetch movie data (using the cached approach)
    try:
        movie_df = get_movie_data()
    except Exception as e:
        st.error(f"Error loading movie data: {e}")
        return

    # Search functionality
    search_query = st.text_input("Search by Movie Name, Director, Actor, or Genre", "")

    # Sorting option
    sort_option = st.selectbox("Sort movies by:", ["Movie Name", "Trending Score"])
    if sort_option == "Trending Score":
        movie_df = movie_df.sort_values(by='Trending Score', ascending=False)
    else:
        movie_df = movie_df.sort_values(by='Movie Name')

    # Create columns for expand/collapse buttons
    col2, col3, cc = st.columns([0.5, 0.5, 5])

    # Expand/Collapse buttons
    with col2:
        if st.button("Expand All"):
            st.session_state['expand_all'] = True
    with col3:
        if st.button("Collapse All"):
            st.session_state['expand_all'] = False

    # Initialize session state for expand/collapse
    if 'expand_all' not in st.session_state:
        st.session_state['expand_all'] = False

    # Filter the DataFrame based on the search query
    if search_query:
        search_query_lower = search_query.lower()
        filtered_df = movie_df[
            movie_df.apply(lambda row:
                           search_query_lower in str(row['Movie Name']).lower() or
                           search_query_lower in str(row.get('Director', '')).lower() or
                           search_query_lower in str(row.get('Genres', '')).lower() or
                           search_query_lower in str(row.get('Actors', '')).lower(),
                           axis=1)
        ]
    else:
        filtered_df = movie_df

    # Display movies
    display_movies(filtered_df, st.session_state['expand_all'])

# ============================================
# Function to Display Movies with Enhanced Layout
# ============================================

def display_movies(filtered_df, expand_all):
    """
    Display movie information with expandable sections.
    """
    for i, (index, row) in enumerate(filtered_df.iterrows(), 1):
        # Fetch Trend Score
        trend_score = row.get('Trending Score', 'N/A')

        # Add green circle emoji and trend score to the expander label
        # Using emoji and text to simulate a green bubble with trend score
        expander_label = f"**{row.get('Movie Name', 'N/A')}** 🟢 {trend_score}"

        with st.expander(expander_label, expanded=expand_all):
            col1, col2 = st.columns([3, 3])

            with col1:
                # Director, Actors, Genres
                render_section("Director", row.get('Director', 'N/A'))
                render_section("Actors", row.get('Actors', 'N/A'))
                render_section("Genres", row.get('Genres', 'N/A'))

                # Synopsis
                render_section("Synopsis", row.get('Synopsis', 'No synopsis available.'))

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

                # Release Dates and Runtime
                render_section("Theater Release Date", row.get('Release Date (Theaters)', 'N/A'))
                render_section("Streaming Release Date", row.get('Release Date (Streaming)', 'N/A'))
                render_section("Runtime", row.get('Runtime', 'N/A'))

            with col2:
                # Sentiment Analysis
                render_section("Sentiment Analysis", row.get('Sentiment Analysis', 'No analysis available'))

            # SEO and Trend Recommendation
            render_recommendations(
                row.get('SEO Keywords', 'N/A'),
                row.get('Trend Recommendation', 'N/A')
            )

# ============================================
# Run the App
# ============================================

if __name__ == "__main__":
    main()
