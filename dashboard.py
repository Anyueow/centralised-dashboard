import streamlit as st
import pandas as pd


def get_movie_data():
    from src.scraping.run_scraper import get_movie_data as fetch_movie_data

    return fetch_movie_data()


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
            col1, col2 = st.columns([2, 3])

            with col1:
                # Movie name and trending score
                movie_header_html = f"""
                <div style="display: flex; align-items: center;">
                    <h3 style="margin: 0;">{row['Movie Name']}</h3>
                    <div style="width: 50px; height: 50px; border-radius: 50%; background-color: #4CAF50; color: white; display: flex; align-items: center; justify-content: center; margin-left: 10px;">
                        <span>{row.get('Trending Score', 'N/A')}</span>
                    </div>
                </div>
                """
                st.markdown(movie_header_html, unsafe_allow_html=True)

                # Basic movie details
                st.markdown(f"**Director**: {row.get('Director', 'N/A')}")
                st.markdown(f"**Actors**: {row.get('Actors', 'N/A')}")
                st.markdown(f"**Genres**: {row.get('Genres', 'N/A')}")

                # Synopsis
                st.markdown(f"**Synopsis**: {row.get('Synopsis', 'No synopsis available.')}")

                # Ratings
                st.markdown("**Ratings:**")
                st.markdown(f"- **IMDb Rating**: {row.get('IMDb Rating', 'N/A')}")
                st.markdown(f"- **Rotten Tomatoes**: {row.get('Rotten Tomatoes Rating', 'N/A')}")
                st.markdown(f"- **Metacritic**: {row.get('Metacritic Rating', 'N/A')}")
                st.markdown(f"- **Metascore**: {row.get('Metascore', 'N/A')}")
                st.markdown(f"- **IMDb Votes**: {row.get('IMDb Votes', 'N/A')}")

                # Release Dates
                st.markdown(f"**Theater Release Date**: {row.get('Release Date (Theaters)', 'N/A')}")
                st.markdown(f"**Streaming Release Date**: {row.get('Release Date (Streaming)', 'N/A')}")

                # Runtime
                st.markdown(f"**Runtime**: {row.get('Runtime', 'N/A')}")

            with col2:
                # Sentiment Analysis
                st.markdown("**Sentiment Analysis:**")
                sentiment = row.get('Sentiment Analysis', 'No analysis available')
                st.markdown(f"{sentiment}")

            # SEO and Trend Recommendation
            st.markdown(
                """
                <div style='background-color: #f0f0f0; padding: 10px; margin-top: 20px;'>
                    <p><strong>SEO Keywords:</strong> Recommended keywords for promotion<br>
                    <strong>Trend Recommendation:</strong> Potential peak audience engagement period</p>
                </div>
                """, unsafe_allow_html=True
            )


# Run the app
if __name__ == "__main__":
    main()