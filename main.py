import streamlit as st
import pandas as pd
from streamlit import button
import matplotlib.pyplot as plt

import helper
import preprocessor
st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file", type=["txt", "csv"])

if uploaded_file is not None:
    # Read file as text or DataFrame
    if uploaded_file.name.endswith('.txt'):
        content = uploaded_file.read().decode('utf-8')  # decode bytes to string
        st.write("File Content:")
        df=preprocessor.preprocess(content)
        # st.dataframe(df)

        # // fetch unique user
        user = df['Sender'].unique().tolist()
        user.remove(" ")
        user.sort()
        user.insert(0,"Overall")

        selected_user=st.sidebar.selectbox("Show Analysis Wrt", user)

        # // adding button
        if st.sidebar.button("Show Analysis"):
            num,words,media,links=helper.fetch_stats(selected_user,df)
            st.title("Analysis Results")
            col=st.columns(4)
            col1=col[0]
            col2=col[1]
            col3=col[2]
            col4=col[3]
            with col1:
                st.header("Total Message")
                st.title(num)
            with col2:
                st.header('Total Words')

                st.title(words)
            with col3:
                st.header("Media Shared")
                st.title(media)
            with col4:
                st.header("Links Shared")
                st.title(links)

            # Monthly  timeline stats
            timeline=helper.monthly_stats(selected_user,df)
            st.title("Monthly Timeline")
            fig,ax=plt.subplots()
            ax.plot(timeline['time'], timeline['message'],color='green')
            plt.xticks(rotation='vertical')

            st.pyplot(fig)

            # daily timeline
            st.title("Daily Timeline")
            daily_timeline=helper.daily_timeline(selected_user,df)
            fig,ax=plt.subplots()
            ax.plot(daily_timeline['only_date'],daily_timeline['message'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

            # activity map
            st.title("Activity Map")

            col=st.columns(2)
            col1=col[0]
            col2=col[1]
            with col1:
                st.header("Most Busy Day")
                activity = helper.Activity_map(selected_user, df)
                fig,ax=plt.subplots()
                ax.barh(activity['Day_name'],activity['Messages'],color='green')

                st.pyplot(fig)
            with col2:
                st.header("Most Busy Month ")
                monthly_activity=helper.month_activity_map(selected_user,df)
                fig,ax=plt.subplots()
                ax.barh(monthly_activity.index,monthly_activity.values,color='orange')
                st.pyplot(fig)



















            if selected_user=='Overall':
                col=st.columns(2)

                col1=col[0]
                col2=col[1]
                x ,new_df= helper.most_busy_user(df)
                fig,ax=plt.subplots()





                with col1:

                    ax.barh(x.index,x.values,color='r')
                    plt.xticks(rotation=90)
                    st.header("Most Busy User")
                    st.pyplot(fig)
                with col2:
                    st.header("Most Busy Users %")
                    st.dataframe(new_df)


            # // create World cloud

            cloud=helper.Word_cloud(selected_user,df)
            fig,ax=plt.subplots()
            ax.imshow(cloud)
            st.header("Word Cloud")
            st.pyplot(fig)


    #          most common words

            most_common_df=helper.most_common_words(selected_user,df)


            fig,ax=plt.subplots()
            ax.barh(most_common_df[0],most_common_df[1])
            plt.xticks(rotation='vertical')
            st.title("Most Common Words")
            st.pyplot(fig)


    #      emoji
            emoji_df=helper.emojis_used(selected_user,df)
            sol=st.columns(2)
            sol1=sol[0]
            sol2=sol[1]
            with sol1:
                st.dataframe(emoji_df)

            with sol2:
                fig,ax=plt.subplots()
                ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct='%0.2f%%')
                st.pyplot(fig)

























    elif uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
        st.write("CSV Preview:")
        st.dataframe(df)



