import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import preprocessor, helper

# Set page configuration
st.set_page_config(page_title="Whatsapp Chat Analyser", page_icon="💬", layout="wide")

# Custom CSS for dark theme and styling
st.markdown("""
    <style>
    body {
        background-color: #121212;
        color: #FFFFFF;
    }
    .sidebar .sidebar-content {
        background-color: #1F1F1F;
    }
    .main .block-container {
        background-color: #1F1F1F;
    }
    .stButton>button {
        color: white;
        background-color: #007bff;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 18px;
        margin-top: 20px;
    }
    .title {
        font-size: 2.5em;
        color: #E50914;
        margin-bottom: 20px;
    }
    .header {
        font-size: 1.5em;
        color: #1DB954;
    }
    .subheader {
        font-size: 1.2em;
        color: #f39c12;
    }
    .stMarkdown {
        color: #FFFFFF;
    }
    .css-1aumxhk {
        margin-top: -80px;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("Navigation")
options = st.sidebar.radio("Go to", ["Home", "Analyse Chat"])

if options == "Home":
    st.markdown('<h1 class="title">Welcome to Whatsapp Chat Analyser</h1>', unsafe_allow_html=True)
    st.markdown("""
    <p>This app allows you to upload your WhatsApp chat history based on 24hr format txt file and gain insights through various analysis features. Below are the key features of this app:</p>
    <ul>
        <li><strong>Total Messages:</strong> See the total number of messages exchanged.</li>
        <li><strong>Total Words:</strong> Get a count of all the words used in the chat.</li>
        <li><strong>Media Shared:</strong> Find out how many media files (images, videos, etc.) were shared.</li>
        <li><strong>Links Shared:</strong> Check the number of links shared in the chat.</li>
        <li><strong>Monthly Timeline:</strong> View the activity over time on a monthly basis.</li>
        <li><strong>Daily Timeline:</strong> See the daily chat activity.</li>
        <li><strong>Activity Map:</strong> Analyze chat activity by day of the week and month.</li>
        <li><strong>Weekly Activity Map:</strong> Get a heatmap of the chat activity by day and hour.</li>
        <li><strong>Most Busy Users:</strong> Identify the most active users in the group.</li>
        <li><strong>Word Cloud:</strong> Visualize the most frequently used words.</li>
        <li><strong>Most Common Words:</strong> Discover the most common words used in the chat.</li>
        <li><strong>Emoji Analysis:</strong> Analyze the use of emojis in the chat.</li>
    </ul>
    <p>Use the sidebar to navigate to the analysis section and start exploring your chat data!</p>
    """, unsafe_allow_html=True)

elif options == "Analyse Chat":
    st.sidebar.title("Whatsapp Chat Analyser")

    uploaded_file = st.sidebar.file_uploader("Choose a file")
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8")

        df = preprocessor.preprocess(data)

        user_list = df['users'].unique().tolist()
        # user_list.remove('group_notification')
        user_list.sort()
        user_list.insert(0, "Overall")

        selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

        if st.sidebar.button("Show Analysis"):
            num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

            st.markdown('<h1 class="title">Top Statistics</h1>', unsafe_allow_html=True)

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown('<h2 class="header">Total Messages</h2>', unsafe_allow_html=True)
                st.markdown(f'<h3 class="subheader">{num_messages}</h3>', unsafe_allow_html=True)
            with col2:
                st.markdown('<h2 class="header">Total Words</h2>', unsafe_allow_html=True)
                st.markdown(f'<h3 class="subheader">{words}</h3>', unsafe_allow_html=True)
            with col3:
                st.markdown('<h2 class="header">Media Shared</h2>', unsafe_allow_html=True)
                st.markdown(f'<h3 class="subheader">{num_media_messages}</h3>', unsafe_allow_html=True)
            with col4:
                st.markdown('<h2 class="header">Links Shared</h2>', unsafe_allow_html=True)
                st.markdown(f'<h3 class="subheader">{num_links}</h3>', unsafe_allow_html=True)

            st.markdown('<h1 class="title">Monthly Timeline</h1>', unsafe_allow_html=True)
            timeline = helper.monthly_timeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(timeline['time'], timeline['message'], color='#1DB954')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

            st.markdown('<h1 class="title">Daily Timeline</h1>', unsafe_allow_html=True)
            daily_timeline = helper.daily_timeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='#E50914')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

            st.markdown('<h1 class="title">Activity Map</h1>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<h2 class="header">Most Busy Day</h2>', unsafe_allow_html=True)
                busy_day = helper.week_activity_map(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_day.index, busy_day.values, color='#f39c12')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.markdown('<h2 class="header">Most Busy Month</h2>', unsafe_allow_html=True)
                busy_month = helper.month_activity_map(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_month.index, busy_month.values, color='#9b59b6')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            st.markdown('<h1 class="title">Weekly Activity Map</h1>', unsafe_allow_html=True)
            user_heatmap = helper.activity_heatmap(selected_user, df)
            fig, ax = plt.subplots()
            ax = sns.heatmap(user_heatmap, cmap="YlGnBu")
            st.pyplot(fig)

            if selected_user == 'Overall':
                st.markdown('<h1 class="title">Most Busy Users</h1>', unsafe_allow_html=True)
                x, new_df = helper.most_busy_users(df)
                fig, ax = plt.subplots()
                col1, col2 = st.columns(2)
                with col1:
                    ax.bar(x.index, x.values, color='#3498db')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)
                with col2:
                    st.dataframe(new_df)

            st.markdown('<h1 class="title">Word Cloud</h1>', unsafe_allow_html=True)
            df_wc = helper.create_wordcloud(selected_user, df)
            fig, ax = plt.subplots()
            plt.imshow(df_wc)
            st.pyplot(fig)

            st.markdown('<h1 class="title">Most Common Words</h1>', unsafe_allow_html=True)
            most_common_df = helper.most_common_words(selected_user, df)
            fig, ax = plt.subplots()
            ax.barh(most_common_df[0], most_common_df[1], color='#2ecc71')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            st.dataframe(most_common_df)

            st.markdown('<h1 class="title">Emoji Analysis</h1>', unsafe_allow_html=True)
            emoji_df = helper.emoji_helper(selected_user, df)
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(emoji_df)
            with col2:
                fig, ax = plt.subplots()
                ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f", colors=sns.color_palette("pastel"))
                st.pyplot(fig)
