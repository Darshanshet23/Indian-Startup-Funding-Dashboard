import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


st.set_page_config(layout='wide',page_title='Start Up Funding Analysis')

df = pd.read_csv('startup_cleaned.csv')
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

# Standardize case and remove extra spaces
df['startup'] = df['startup'].str.strip().str.lower()

# Remove URLs or non-alphabetic characters
df['startup'] = df['startup'].str.replace(r'http\S+|www.\S+', '', regex=True)

# Remove ".com" and unnecessary punctuation
df['startup'] = df['startup'].str.replace(r'\.com|\.$', '', regex=True)
df['startup'] = df['startup'].str.replace(r'[^a-zA-Z0-9\s&\-\']', '', regex=True)

# Drop empty names
df = df[df['startup'] != '']
def load_investor_details(investor):
    st.title(investor)
#     load recent 5 investments of selected investor
    last = df[df['investors name'].str.contains(investor)].head()[['date', 'startup', 'industry', 'city', 'round', 'amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last)

    col1, col2 = st.columns(2)
    with col1:
#     Biggest Investment
        big_series = df[df['investors name'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending = False).head()
        st.subheader('Biggest Investments')
        # st.dataframe(big_df)

        fig, ax = plt.subplots()
        ax.bar(big_series.index,big_series.values)

        st.pyplot(fig)

    with col2:
        vertical_series = df[df['investors name'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Sector Invested in')

        fig, ax = plt.subplots()
        ax.pie(vertical_series,labels=vertical_series.index,autopct="%0.01f%%")

        st.pyplot(fig)

    col3, col4 = st.columns(2)
    with col3:
        vertical_series1 = df[df['investors name'].str.contains(investor)].groupby('round')['amount'].sum().sort_values(
            ascending=False).head()
        st.subheader('Round of Investment')

        fig, ax = plt.subplots()
        ax.pie(vertical_series1, labels=vertical_series1.index, autopct="%0.01f%%")

        st.pyplot(fig)

    with col4:
        vertical_series2 = df[df['investors name'].str.contains(investor)].groupby('city')['amount'].sum().sort_values(
            ascending=False).head()
        st.subheader('City Invested in')

        fig, ax = plt.subplots()
        ax.pie(vertical_series2, labels=vertical_series2.index, autopct="%0.01f%%")

        st.pyplot(fig)

    col5, col6 = st.columns(2)
    with col5:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['year'] = df['date'].dt.year
        yoy_investment = df[df['investors name'].str.contains(investor)].groupby('year')['amount'].sum()

        st.subheader('yoy investment')

        fig, ax = plt.subplots()
        ax.plot(yoy_investment.index, yoy_investment.values)

        st.pyplot(fig)


    with col6:
        st.subheader("Similar Investors")

        # Get industries the selected investor has invested in
        investor_data = df[df['investors name'].str.contains(investor, case=False, na=False)]
        industries = investor_data['industry'].unique()

        # Find other investors in these industries
        similar_data = df[df['industry'].isin(industries)]
        similar_investors = similar_data['investors name'].value_counts().head(5)

        # Remove the selected investor from the list
        similar_investors = similar_investors.drop(investor, errors='ignore')

        # Plot the bar chart
        fig, ax = plt.subplots()
        ax.bar(similar_investors.index, similar_investors.values, color='skyblue')
        ax.set_xlabel("Investors")
        ax.set_ylabel("Shared Investments")
        ax.set_title("Top Similar Investors")

        # Rotate x-axis labels for better visibility
        plt.xticks(rotation=45)

        # Show the chart in Streamlit
        st.pyplot(fig)

def load_company_detais(company):
    st.title(company)
    insutry_belongs = df[df['startup'] == company]['industry'].values[0]

    sub_industry = df[df['startup'] == company]['subVertical'].values[0]

    location_of_company = df[df['startup'] == company]['city'].values[0]

    round_of_funding = df[df['startup'] == company]['round'].values[0]

    investor_name = df[df['startup'] == company]['investors name'].values[0]

    date_of_investment =  df[df['startup'] == company]['date'].iloc[0].strftime('%Y-%m-%d')


    st.metric('Located at', str(location_of_company))

    col1,col2= st.columns(2)
    with col1:

        st.metric('Industry', str(insutry_belongs))
    with col2:

        st.metric('Sub Industry', str(sub_industry))


    st.metric('Funding Stage', str(round_of_funding))

    col3,col4 = st.columns(2)

    with col3:
        st.metric('Funded Investor', str(investor_name))

    with col4:
        st.metric('Date', str(date_of_investment))





def load_overall_analysis():
    st.title('Overall Analysis')
    total = round(df['amount'].sum())

    max_funds = df.groupby('startup')['amount'].max().sort_values(ascending=False).values[0]

    avg_funds = round(df.groupby('startup')['amount'].sum().mean())

    num_startups = df['startup'].nunique()

    col1,col2,col3,col4 = st.columns(4)
    with col1:
        st.metric('Total', str(total) + ' Cr')
    with col2:
        st.metric('Max', str(max_funds) + ' Cr')
    with col3:
        st.metric('Max', str(avg_funds) + ' Cr')
    with col4:
        st.metric('Funded Startuos ', str(num_startups))

    st.header('MoM Graph')
    temp = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    temp['x_axis'] = temp['month'].astype(str) + '-' + temp['year'].astype(str)

    fig, ax = plt.subplots(figsize=(12, 6))  # Adjust figure size
    ax.plot(temp['x_axis'], temp['amount'], marker='o', linestyle='-')

    # Reduce labels (Show every Nth label)
    step = max(len(temp) // 10, 1)  # Adjust dynamically
    ax.set_xticks(temp['x_axis'][::step])
    ax.set_xticklabels(temp['x_axis'][::step], rotation=45, ha='right')

    st.pyplot(fig)

st.sidebar.title('Start Up Funding Analysis')

option = st.sidebar.selectbox('Select One',['Overall Analysis','Start Up','Investor'])


if option == 'Overall Analysis':
    bt0 = st.sidebar.button('Show Overall Analysis')
    if bt0:
        load_overall_analysis()

elif option == 'Start Up':
    selected_company = st.sidebar.selectbox('select start up',sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find Startup Details')
    if btn1:
        load_company_detais(selected_company)

else:
    selected_investor = st.sidebar.selectbox('select start up',sorted(set(df['investors name'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)