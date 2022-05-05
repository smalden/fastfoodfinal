import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pydeck as pdk

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
    data = pd.read_csv(file_name)
    data.replace({'name': mcDonalds}, inplace=True)
    return data

def map_choice(data):
    city_choices = data.groupby('city')['name'].count().sort_values(ascending=False).head(15)
    city_view = st.sidebar.selectbox("Select a city to view: ", city_choices.keys())
    city_data = data[data.city == city_view]
    set_view_lat = city_data['latitude'].mean()
    set_view_long = city_data['longitude'].mean()
    names = city_data.groupby('name')['name'].count().sort_values(ascending=False)
    restaurants = st.sidebar.multiselect("Select up to 3 restaurants to display", names.keys())
    if st.sidebar.button("Generate Map") and len(restaurants)>=1 and len(restaurants)<=3:
        if len(restaurants) == 1:
            restaurant1 = city_data[city_data.name == restaurants[0]]
            map_make_1(set_view_lat, set_view_long, restaurants, restaurant1)
        elif len(restaurants) == 2:
            restaurant1 = city_data[city_data.name == restaurants[0]]
            restaurant2 = city_data[city_data.name == restaurants[1]]
            map_make_2(set_view_lat, set_view_long, restaurants, restaurant1, restaurant2)
        else:
            restaurant1 = city_data[city_data.name == restaurants[0]]
            restaurant2 = city_data[city_data.name == restaurants[1]]
            restaurant3 = city_data[city_data.name == restaurants[2]]
            map_make_3(set_view_lat, set_view_long, restaurants, restaurant1, restaurant2, restaurant3)

def map_make_2(set_view_lat, set_view_long, restaurants, restaurant1, restaurant2):
    layer1 = pdk.Layer(
                    'ScatterplotLayer',
                    data=restaurant1,
                    get_position='[longitude, latitude]',
                    get_color='[200, 30, 0, 160]',
                    get_radius=700
                    )
    layer2 = pdk.Layer(
                    'ScatterplotLayer',
                    data=restaurant2,
                    get_position='[longitude,latitude]',
                    get_color='[0, 200, 30, 160]',
                    get_radius=700
                    )
    st.pydeck_chart(
        pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=pdk.ViewState(
                latitude=set_view_lat,
                longitude=set_view_long,
                zoom=9
            ),
            layers=[layer1, layer2]
            )
        )



def map_make_3(set_view_lat, set_view_long, restaurants, restaurant1, restaurant2, restaurant3):
    layer1 = pdk.Layer(
                    'ScatterplotLayer',
                    data=restaurant1,
                    get_position='[longitude, latitude]',
                    get_color='[200, 30, 0, 160]',
                    get_radius=700
                    )
    layer2 = pdk.Layer(
                    'ScatterplotLayer',
                    data=restaurant2,
                    get_position='[longitude,latitude]',
                    get_color='[0, 200, 30, 160]',
                    get_radius=700
                    )
    layer3 = pdk.Layer(
                    'ScatterplotLayer',
                    data=restaurant3,
                    get_position='[longitude,latitude]',
                    get_color='[30, 0, 200, 160]',
                    get_radius=700
                )
    st.pydeck_chart(
        pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=pdk.ViewState(
                latitude=set_view_lat,
                longitude=set_view_long,
                zoom=9
            ),
            layers=[layer1, layer2, layer3]
        ))

def map_make_1(set_view_lat, set_view_long, restaurants, restaurant1):
    st.pydeck_chart(
        pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=pdk.ViewState(
                latitude=set_view_lat,
                longitude=set_view_long,
                zoom=9
            ), layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=restaurant1,
                get_position='[longitude, latitude]',
                get_color='[200, 30, 0, 160]',
                get_radius=700,
    )]))


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
    data = load_data("fastfooddata.csv")
    choice = st.sidebar.selectbox("Choose a graph or map", ["Cities With the Most Fast Food Restaurants", "Most Popular Restaurants by State", "Top 5 States With The Most of any Restaurant", "Map of All Restaurants by City"])
    if choice == "Cities With the Most Fast Food Restaurants":
        top_five_cities(data)
    elif choice == "Most Popular Restaurants by State":
        most_popular_by_state(data)
    elif choice == "Top 5 States With The Most of any Restaurant":
        most_states_with(data)
    elif choice == "Map of All Restaurants by City":
        map_choice(data)


main()

