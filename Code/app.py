import streamlit as st
import pickle
import pandas as pd

st.set_page_config(
     page_title ="College Recommendation System",
     page_icon ="icon.png",
     layout="centered")

collegedata=pickle.load(open('collegedata.pkl','rb'))

def recommad(userinput_state,userinput_Stream,userinput_cotype,userinput_fees):
 try:
      Filter=collegedata[((collegedata.State==userinput_state)&(collegedata.Stream==userinput_Stream))]
      if userinput_fees=='Lower Fees' :
            if userinput_cotype=='UG':
                df=Filter.sort_values(by=['UG_fee'],ascending=[True])
                recom_data=df[['College_Name','UG_fee',"Overall_Rating"]]
                recom_data['Overall_Rating'] = recom_data['Overall_Rating'].apply(lambda x: '{:,.1f}'.format(x))

            else:
                df=Filter.sort_values(by=['PG_fee'],ascending=[True])
                recom_data = df[['College_Name', 'PG_fee', "Overall_Rating"]]
                recom_data['Overall_Rating'] = recom_data['Overall_Rating'].apply(lambda x: '{:,.1f}'.format(x))

      else :
            df=Filter.sort_values(by=['Overall_Rating'],ascending=[False])
            if userinput_cotype == 'UG':
                recom_data = df[['College_Name', 'UG_fee', "Overall_Rating"]]
                recom_data['Overall_Rating'] = recom_data['Overall_Rating'].apply(lambda x: '{:,.1f}'.format(x))

            else:
                recom_data = df[['College_Name', 'PG_fee', "Overall_Rating"]]
                recom_data['Overall_Rating'] = recom_data['Overall_Rating'].apply(lambda x: '{:,.1f}'.format(x))

      recom_data = recom_data.head()
      return recom_data
 except:
    print('Something goes wronge...')
    st.warning('Something goes wronge...')


st.title('College Recommendation System')
st.markdown("##")
st.image("college1.webp")
st.markdown("##")

st.header('Prefered State :')
option_state = st.selectbox('Which state you belong?',(collegedata.State.sort_values(ascending=True).unique()))
st.write('You selected : ', option_state)

st.header("Stream type :")
option_stream = st.selectbox('Which stream you study?',(collegedata.Stream.sort_values(ascending=True).unique()))
st.write('You selected : ', option_stream)

st.header("Course type :")
course = st.radio("UG or PG ?",('UG','PG'))
if course == 'UG':
     st.write('You selected : UG.')
else:
     st.write("You selected : PG.")

st.header('Sort by :')
sort = st.radio(" Colleges sorted by higher ratings or lower fees?",('Higher Rating','Lower Fees'))
if sort == 'Higher Rating':
     st.write('You selected : Higher Rating.')
else:
     st.write("You selected : Lower Fees.")

if st.button('Find'):
    recommendation=recommad(option_state, option_stream, course, sort)

    if len(recommendation)==0:
        st.warning(" Ooops ! Data not found....")
        st.stop()
    else :
        list_index=[]
        for i in range(0,len(recommendation)):
            list_index.append(i+1)
        recommendation=recommendation.set_index([pd.Index(list_index)])
        with st.empty():
            st.write('')
        with st.empty():
            st.write('')

        col1,col2=st.columns([6,1])

        with col1 :
            st.table(recommendation)

        with col2 :
            st.markdown("##### #Websites")
            url_list = []
            for i in range(0, len(recommendation)):
                url_list.append("https://www.google.com/search?q=" + str(recommendation.iloc[i].College_Name).replace(" ", "+").replace( "(", "").replace(")", ""))

            for i in url_list:
                st.markdown("###### [ Know More ](%s)"% i)
else:
    st.warning("Button not clicked...")

st.markdown("##")
st.markdown("##")

with st.container():
    st.text(" Developed by Variya Divyesh M.",)
    st.markdown(" Contact Us : [divyeshvariya106@gmail.com](%s)"% ("mailto:divyeshvariya106@gmail.com"))