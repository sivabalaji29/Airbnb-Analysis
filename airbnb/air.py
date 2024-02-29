from pymongo import MongoClient
import pandas as pd
import streamlit as st
import plotly.express as px

myclient=MongoClient('mongodb+srv://sivabalaji10000:Siva1234@king.ni5plag.mongodb.net/?retryWrites=true&w=majority')
mydb=myclient['sample_airbnb']
mycollection=mydb['listingsAndReviews']

data=pd.DataFrame(list(mycollection.find()))
h=[]
for i in data['host']:
    h.append(i['host_location'])

host_location=[x.split(sep=",")[0] for x in h]

country = []
for i in data['address']:
    country.append(i['country'])
rating=[]
for i in data['review_scores']:
    rating.append(i.get('review_scores_rating','0'))
l=[]
for i in data["address"]:
    l.append(i['location']['coordinates'])
ll=pd.DataFrame(l,columns=['longitude','latitude'])

month_av=[]
for i in data['availability']:
    month_av.append(i['availability_30'])

year_av=[]
for i in data['availability']:
    year_av.append(i['availability_365'])

df=pd.DataFrame(data['_id'])
df['host']=data['name']
df['location']=host_location
df['country']=country
df['property_type']=data['property_type']
df['room_type']=data['room_type']
df['month']=data['last_scraped'].dt.month_name()
df['year']=data['last_scraped'].dt.year
df['accommodation']=data['accommodates'].astype(int)
df['review_count']=data['number_of_reviews'].astype(int)
df['price']=data['price'].astype(str).astype(float)
df['rating']=rating
df['bo_month']=data['last_review'].dt.month_name()
df['bo_year']=data['last_review'].dt.year
df['month_availability']=month_av
df['year_availability']=year_av
df['longitude']=ll['longitude']
df['latitude']=ll['latitude']
df['rating']=df['rating'].astype(int)

st.title(':blue[Airbnb Data Visualization]')
st.write( f'<h6 style="color:rgb(0,  102, 204, 255);">App Created by SIVABALAJI</h6>', unsafe_allow_html=True ) 

tab1,tab2,tab3,tab4,tab5= st.tabs(['Count','Price_Rating Analysis','Booking_pattern','Availability','geo_visualisation'])
with tab2:
    rating = pd.DataFrame(df[['country', 'property_type', 'room_type', 'rating']])
    mean_rating = rating.groupby(['country', 'property_type'])['rating'].mean().astype(int).reset_index()
    mean_rating = mean_rating.pivot(index='property_type', columns='country')['rating'].fillna(0)
    fig_p_rating = px.imshow(mean_rating, labels=dict(x="Country", y="property_type", color="rating"), x=mean_rating.columns,
                    y=mean_rating.index, aspect="auto", title='Avg Rating for property_type')

    rating = pd.DataFrame(df[['country', 'property_type', 'room_type', 'rating']])
    mean_rating = rating.groupby(['country', 'room_type'])['rating'].mean().astype(int).reset_index()
    mean_rating = mean_rating.pivot(index='room_type', columns='country')['rating'].fillna(0)
    fig_r_rating = px.imshow(mean_rating, labels=dict(x="Country", y="room_type", color="rating"), x=mean_rating.columns,
                    y=mean_rating.index, aspect="auto", title='Avg Rating for room_type')

    review = pd.DataFrame(df[['review_count', 'property_type', 'room_type', 'country']])
    review_count = review.groupby(['country', 'property_type'])['review_count'].count().sort_values(
        ascending=False).reset_index()
    review_count = review_count.pivot(index='property_type', columns='country')['review_count'].fillna(0)
    fig_p_review= px.imshow(review_count, labels=dict(x="Country", y="Property_type", color="review_count"),
                    x=review_count.columns, y=review_count.index, aspect="auto", title="Review_Count for Property_type")

    review = pd.DataFrame(df[['review_count', 'property_type', 'room_type', 'country']])
    review_count = review.groupby(['country', 'room_type'])['review_count'].count().sort_values(
        ascending=False).reset_index()
    review_count = review_count.pivot(index='room_type', columns='country')['review_count'].fillna(0)
    fig_r_review = px.imshow(review_count, labels=dict(x="Country", y="Room_type", color="review_count"), x=review_count.columns,
                    y=review_count.index, aspect="auto", title='Review_Count for Room_type')

    price = pd.DataFrame(df[['country', 'property_type', 'room_type', 'price']])
    price = price.groupby(['country', 'property_type'])['price'].mean().astype(int).sort_values(
        ascending=False).reset_index()
    price = price.pivot(index='property_type', columns='country')['price'].fillna(0)
    fig_p_price = px.imshow(price, labels=dict(x="Country", y="property_type", color="price"), x=price.columns, y=price.index,
                    aspect="auto", title='Avg Price for Property_type')

    price = pd.DataFrame(df[['country', 'property_type', 'room_type', 'price']])
    price = price.groupby(['country', 'room_type'])['price'].mean().astype(int).sort_values(
        ascending=False).reset_index()
    price = price.pivot(index='room_type', columns='country')['price'].fillna(0)
    fig_r_price = px.imshow(price, labels=dict(x="Country", y="room_type", color="price"), x=price.columns, y=price.index,
                    aspect="auto", title='Avg Price for room_type')

    price = pd.DataFrame(df[['country', 'property_type', 'room_type', 'price']])
    prp = pd.DataFrame(df[['property_type', 'room_type', 'price']])
    prpm = prp.groupby(["property_type", "room_type"])["price"].mean().astype(int).sort_values(
        ascending=False).reset_index()
    prph = prpm.pivot(index='property_type', columns='room_type')['price'].fillna(0)
    fig_pr_price = px.imshow(prph, labels=dict(x="Room_type", y="Property_type", color="Price"), x=prph.columns, y=prph.index,
                    aspect="auto", title='Avg price for different room and property_type')

    st.plotly_chart(fig_p_rating,use_container_width=True)
    st.plotly_chart(fig_r_rating, use_container_width=True)
    st.plotly_chart(fig_p_price, use_container_width=True)
    st.plotly_chart(fig_r_price, use_container_width=True)
    st.plotly_chart(fig_pr_price, use_container_width=True)

with tab1:
    pvc = df['property_type'].value_counts().rename_axis('property_type').reset_index(name='counts')
    fig_p_v = px.bar(pvc, x="property_type", y="counts", color="counts", title="Property_type_count", height=1000)

    rvc = df['room_type'].value_counts().rename_axis('room_type').reset_index(name='counts')

    fig_r_v= px.bar(rvc, x="room_type", y="counts", color="counts", title="Room_type_count")

    st.plotly_chart(fig_p_v, use_container_width=True)
    st.plotly_chart(fig_r_v, use_container_width=True)
with tab3:
    booking = pd.DataFrame(df[['host', 'bo_month']])
    booking_count = booking.groupby(['bo_month'])['host'].count().sort_values(ascending=False).reset_index()
    fig_bc_m= px.bar(booking_count, x="bo_month", y="host", color="host", title="Booking Analysis by Month", height=1000)

    booking = pd.DataFrame(df[['host', 'bo_year']])
    booking_count = booking.groupby(['bo_year'])['host'].count().reset_index()
    fig_bc_y = px.bar(booking_count, x="bo_year", y="host", color="host", title="Booking Analysis by Year")

    st.plotly_chart(fig_bc_m, use_container_width=True)
    st.plotly_chart(fig_bc_y, use_container_width=True)

with tab4:
    availability=pd.DataFrame(df[['country','month_availability']])
    availability_count=availability.groupby('country')['month_availability'].sum().reset_index()
    fig_avm=px.line(availability_count,x='country',y='month_availability',title='Availability per Month')

    availability = pd.DataFrame(df[['country', 'year_availability']])
    availability_count = availability.groupby('country')['year_availability'].sum().reset_index()
    fig_avy = px.line(availability_count, x='country', y='year_availability',title='Availability per year')
    st.plotly_chart(fig_avm, use_container_width=True)
    st.plotly_chart(fig_avy, use_container_width=True)


with tab5:
    scl = pd.DataFrame(df[['location', 'country', 'price', 'longitude', 'latitude']])

    fig = px.scatter_geo(scl, lat='latitude', lon='longitude', hover_name="location", color='country', text='price')
    fig.update_traces(marker=dict(size=20))

    map = pd.DataFrame(df[['country', 'location', 'property_type', 'room_type', 'longitude', 'latitude']])
    fig_1= px.choropleth(map, locations='country', locationmode='country names', hover_name='room_type',
                        color='property_type')
    st.plotly_chart(fig, use_container_width=True)
    st.plotly_chart(fig_1, use_container_width=True)