import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
us_states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}
mcDonalds = {
    "Mcdonalds": "McDonalds",
    "McDonalds": "McDonalds",
    "Mcdonald's": "McDonalds",
    "McDonald's": "McDonalds",
    "McDonalds's": "McDonalds"
}
@st.cache(allow_output_mutation=True)
def load_data(file_name):
    data = pd.read_csv('fastfooddata.csv')
    data.replace({'name': mcDonalds}, inplace=True)
    return data

def top_five_cities(data):
    top_five_data = (data.groupby('city')['name'].count()).sort_values(ascending=False).head(5)
    x = top_five_data.keys()
    y = top_five_data.values.tolist()
    fig, ax = plt.subplots()
    ax.bar(x, y)
    ax.set_title("Top 5 Cities With the Most Fast Food Restaurants")
    ax.set_xlabel("City")
    ax.set_ylabel("Number of Restaurants")
    st.pyplot(fig)

def most_popular_by_state(data):
    states = data.groupby('province')['province'].nunique()
    state = st.sidebar.selectbox("Select a State:", states.keys())
    top_five_data = data[data.province == state]
    top_five_data = top_five_data.groupby('name')['name'].count().sort_values(ascending=False).head(5)
    fig, ax = plt.subplots()
    ax.bar(top_five_data.keys(), top_five_data.values.tolist())
    state_name = us_states[state]
    ax.set_title("Top 5 Restaurants With the Most Chains in "+state_name)
    ax.set_xlabel("Name of Restaurant")
    ax.set_ylabel("Number of Restaurants")
    st.pyplot(fig)

def most_states_with(data):
    restaurants = data.groupby('name')['name'].nunique()
    name = st.sidebar.selectbox("Select the Name of a Restaurant", restaurants.keys())
    top_five_states = data[data.name == name]
    top_five_states = top_five_states.groupby('province')['province'].count().sort_values(ascending=False).head(5)
    fig, ax = plt.subplots()
    states = top_five_states.keys()
    return_states = []
    for value in states:
        state_name = us_states[value]
        return_states.append(state_name)
    ax.bar(return_states, top_five_states.values.tolist())
    ax.set_title("Top 5 States With The Most" + name)
    ax.set_xlabel("State")
    ax.set_ylabel("Number of " + name + " Locations")
    st.pyplot(fig)




def main():
    data = load_data("C:\\fastfooddata.csv")
    choice = st.sidebar.selectbox("Choose a graph or map", ["Cities With the Most Fast Food Restaurants", "Most Popular Restaurants by State", "Top 5 States With The Most of any Restaurant", "Map of All Restaurants by City"])
    if choice == "Cities With the Most Fast Food Restaurants":
        top_five_cities(data)
    elif choice == "Most Popular Restaurants by State":
        most_popular_by_state(data)
    elif choice == "Top 5 States With The Most of any Restaurant":
        most_states_with(data)


main()
