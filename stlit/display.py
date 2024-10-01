# display.py
import streamlit as st

def display_movie_data_and_trends(filtered_df, trend_figures):
    """
    Display the movie details and corresponding trend data side-by-side using Streamlit columns.
    """
    for i, (index, row) in enumerate(filtered_df.iterrows()):
        col1, col2 = st.columns([2, 3])

        # Movie Details in first column
        with col1:
            st.markdown(f"### {row['Movie Name']}")
            st.markdown(f"**Director**: {row['Director']}")
            st.markdown(f"**Synopsis**: {row['Synopsis']}")
            st.markdown(f"**Theater Release Date**: {row['Release Date (Theaters)'].strftime('%Y-%m-%d') if pd.notnull(row['Release Date (Theaters)']) else 'N/A'}")
            st.markdown(f"**Release Date (Streaming)**: {row['Release Date (Streaming)'].strftime('%Y-%m-%d') if pd.notnull(row['Release Date (Streaming)']) else 'N/A'}")
            st.markdown(f"**Average Score**: {row['Average Score']}")
            st.markdown(f"**Genres**: {', '.join(row['Genres']) if isinstance(row['Genres'], list) else row['Genres']}")
            st.markdown(f"**Audience Score**: {row['Audience Score']}")
            st.markdown(f"**Critic Score**: {row['Critic Score']}")
            st.markdown(f"**Sentiment Analysis**: *...Feature Pending...*")

        # Trend Visualization in second column
        with col2:
            if i < len(trend_figures):
                # Display the plotly chart inline using Streamlit
                st.plotly_chart(trend_figures[i], use_container_width=True)
            else:
                st.markdown("No trend data available for this movie.")

        # Divider between movies
        st.markdown("---")