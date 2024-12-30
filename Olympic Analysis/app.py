import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

# Header
st.markdown("<h2 style='font-size: 24px; color:green;'>Name of Olympian Over the Year upto 2016_</h2>", unsafe_allow_html=True)

# Load data
df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df, region_df)

# Sidebar
st.sidebar.title("Olympic Analysis")
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Name of Olympian', 'Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete-wise Analysis', 'New Feature')
)

# Display data for debugging
st.dataframe(df)

# Name of Olympian
if user_menu == 'Name of Olympian':

    st.markdown("<h3 style='color:green;'>Search for an Olympian</h3>", unsafe_allow_html=True)
    olympian_name = st.text_input("Enter Olympian's Name")

    if olympian_name:
        olympian_data = df[df['Name'].str.contains(olympian_name, case=False, na=False)]
        if not olympian_data.empty:
            st.markdown(f"<h4 style='color:green;'>Results for {olympian_name}:</h4>", unsafe_allow_html=True)
            st.dataframe(olympian_data)
        else:
            st.markdown(f"<p style='color:red;'>No results found for {olympian_name}</p>", unsafe_allow_html=True)

    olympians_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(olympians_over_time, x="Edition", y="Name")

    st.markdown("<h3 style='color:green;'>Number of Olympians Participating Each Year</h3>", unsafe_allow_html=True)
    st.plotly_chart(fig)

# Medal Tally
elif user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    if selected_year == 'Overall' and selected_country == ' Overall':
        st.markdown("<h2 style='color:green;'>Overall Tally</h2>", unsafe_allow_html=True)
    elif selected_year != 'Overall' and selected_country == 'Overall':
        st.markdown(f"<h2 style='color:green;'>Medal Tally in {selected_year} Olympics</h2>", unsafe_allow_html=True)
    elif selected_year == 'Overall' and selected_country != 'Overall':
        st.markdown(f"<h2 style='color:green;'>{selected_country} overall performance</h2>", unsafe_allow_html=True)
    elif selected_year != 'Overall' and selected_country != 'Overall':
        st.markdown(f"<h2 style='color:green;'>{selected_country} performance in {selected_year} Olympics</h2>", unsafe_allow_html=True)

    st.table(medal_tally)

# Overall Analysis
elif user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.markdown("<h2 style='font-size: 24px; color:green;'>Overall Analysis of Years</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x="Edition", y="region")
    st.markdown("<h2 style='font-size: 24px; color:green;'>Participating Nations over the years</h2>", unsafe_allow_html=True)
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x="Edition", y="Event")
    st.markdown("<h2 style='font-size: 24px; color:green;'>Events over the years</h2>", unsafe_allow_html=True)
    st.plotly_chart(fig)

    athlete_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athlete_over_time, x="Edition", y="Name")
    st.markdown("<h2 style='font-size: 24px; color:green;'>Athletes over the years</h2>", unsafe_allow_html=True)
    st.plotly_chart(fig)

    st.markdown("<h2 style='font-size: 24px; color:green;'>Number of events over the years [All Sports]</h2>", unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'), annot=True)
    st.pyplot(fig)

    st.markdown("<h2 style='font-size: 24px; color:green;'>Most successful athletes</h2>", unsafe_allow_html=True)
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select a Sport', sport_list)
    x = helper.most_successful(df, selected_sport)
    st.table(x)

# Country-wise Analysis
elif user_menu == 'Country-wise Analysis':
    st.sidebar.title("Country-wise Analysis")

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country', country_list, key='country_selectbox')

    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.markdown(f"<h2 style='color:green;'>{selected_country} Medal tally over the years</h2>", unsafe_allow_html=True)
    st.plotly_chart(fig)

    st.markdown(f"<h2 style='color:green;'>{selected_country} excels in the following sports</h2>", unsafe_allow_html=True)
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    st.markdown(f"<h2 style='color:green;'>Top most athletes of {selected_country}</h2>", unsafe_allow_html=True)
    top_df = helper.most_successful_countrywise(df, selected_country)
    st.table(top_df)

# Athlete-wise Analysis
elif user_menu == 'Athlete-wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    data = [x1, x2, x3, x4]
    labels = ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist']

    # Filter out empty datasets
    data, labels = zip(*[(d, l) for d, l in zip(data, labels) if len(d) > 0])

    fig = ff.create_distplot(data, labels, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1500, height=600)
    st.markdown("<h2 style='font-size: 24px; color:green;'>Distribution of Participators' Age</h2>", unsafe_allow_html=True)
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.markdown("<h2 style='font-size: 24px; color:green;'>Height vs Weight</h2>", unsafe_allow_html=True)
    selected_sport = st.selectbox('Select a Sport', sport_list, key='sport_selectbox')
    temp_df = helper.weight_v_height(df, selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(x=athlete_df['Weight'], y=athlete_df['Height'], hue=temp_df['Medal'], style=temp_df['Sex'], s=60)
    st.pyplot(fig)

    st.markdown("<h2 style='font-size: 24px; color:green;'>Men vs Women participating over the years</h2>", unsafe_allow_html=True)
    final = helper.men_vs_women(df)
    fig = px.line(final, x='Year', y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1500, height=600)
    st.plotly_chart(fig)

# New Feature
elif user_menu == 'New Feature':
    st.markdown("<h2 style='color:green;'>New Feature Coming Soon!</h2>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color:green;'>We are working on this feature. Stay tuned for exciting updates!</p>",
        unsafe_allow_html=True
    )
