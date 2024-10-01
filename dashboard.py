import streamlit as st
import pandas as pd
from src.trends.TrendVisualizer import TrendVisualizer
from stlit.filters import filter_movie_data
from stlit.movie_data import get_movie_data
from stlit.trend_data import get_trend_data

def main():
    # Set page layout for the Streamlit app
    st.set_page_config(layout="wide")
    st.title("Direct TV SEO Movie Research Dashboard")
    st.markdown("View trending movies, their details, and Google Trends data side-by-side.")

    # Fetch movie data (cached)
    movie_df = get_movie_data()
    search_query = st.text_input("Search by Movie Name, Director, Actor, or Genre", "")


    # Create three columns with adjusted width to center the elements
    col2, col3, cc = st.columns([0.5, 0.5, 5])  # Adjusted the width for better centering

    with cc: 
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)



    # Center the "Expand All" button in the second column
    with col2:
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        expand_all = st.button("Expand All")
        st.markdown("</div>", unsafe_allow_html=True)

    # Center the "Collapse All" button in the third column
    with col3:
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        collapse_all = st.button("Collapse All")
        st.markdown("</div>", unsafe_allow_html=True)

    # Filter the DataFrame based on the search query
    if search_query:
        filtered_df = movie_df[
            movie_df.apply(lambda row: search_query.lower() in str(row['Movie Name']).lower() or
                                         search_query.lower() in str(row['Director']).lower() or
                                         search_query.lower() in str(row['Genres']).lower(), axis=1)
        ]
    else:
        filtered_df = movie_df

    # Fetch trends for the filtered movies (cached)
    movie_titles = filtered_df['Movie Name'].tolist()
    trend_figures = get_trend_data(movie_titles)  # Get the trend figures

    # Display movie details and trends
    display_movies_with_trends(filtered_df, trend_figures, expand_all, collapse_all)

# Function to display movies and their Google Trends data
def display_movies_with_trends(filtered_df, trend_figures, expand_all, collapse_all):
    """
    Display movie information side-by-side with the Google Trends chart.
    """

    # Keep track of whether rows should be expanded or collapsed
    expand_state = True if expand_all else False if collapse_all else True

    for i, (index, row) in enumerate(filtered_df.iterrows(), 1):  # Add numbering (1, 2, 3, ...)
        # Add a collapsible section for each movie
        with st.expander(f"{i}. {row['Movie Name']}", expanded=expand_state):  # Expanded by default if expand_all
            col1, col2 = st.columns([2, 3])

            # Movie Information in first column
            with col1:
                st.markdown(f"### {row['Movie Name']}")
                st.markdown(f"**Director**: {row['Director']}")
                st.markdown(
                    f"**Genres**: {', '.join(row['Genres']) if isinstance(row['Genres'], list) else row['Genres']}")

                # Add Synopsis
                st.markdown(
                    f"**Synopsis**: {row['Synopsis'] if row['Synopsis'] != 'N/A' else 'No synopsis available.'}")

                # Add Rating
                st.markdown(f"**Rating**: {row['Rating'] if row['Rating'] != 'N/A' else 'No rating available.'}")

                st.markdown(
                    f"**Theater Release Date**: {row['Release Date (Theaters)'].strftime('%Y-%m-%d') if pd.notnull(row['Release Date (Theaters)']) else 'N/A'}")
                st.markdown(
                    f"**Release Date (Streaming)**: {row['Release Date (Streaming)'].strftime('%Y-%m-%d') if pd.notnull(row['Release Date (Streaming)']) else 'N/A'}")

                # Add Runtime
                st.markdown(f"**Runtime**: {row['Runtime'] if row['Runtime'] != 'N/A' else 'No runtime available.'}")

                st.markdown(
                    f"**Sentiment Analysis**: *..........................Upcoming.........................................*")  # Placeholder for future sentiment analysis
                st.markdown(f"**Actors**: *...Upcoming...*")  # Placeholder for actors
                st.markdown(f"**Top Comment**: *...Upcoming...*")  # Placeholder for top comment

            # Trend Graph in the second column
            with col2:
                if trend_figures and i-1 < len(trend_figures):
                    st.plotly_chart(trend_figures[i-1], use_container_width=True)  # Display the graph inline
                else:
                    st.markdown("No trend data available for this movie.")

# Running the app
if __name__ == "__main__":
    main()
