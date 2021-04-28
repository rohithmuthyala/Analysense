import pandas as pd
import streamlit as st
import time
import plotly.express as px
from PIL import Image

@st.cache(allow_output_mutation=True)
def load_data():
        df = pd.read_csv('https://raw.githubusercontent.com/rohithmuthyala/Analysense/main/marketing_campaigns.csv')
        df['Profit'] = df['Revenue']- df['Cost']
        return  df

def load_data_sum():
        df = load_data()
        tmp =df.groupby('Campaign')[['Visits','Revenue','Cost','Profit']].sum()
        tmp['Rev_per_Visits'] = tmp['Revenue'] / tmp['Visits']
        tmp['Cost_per_Visits']= tmp['Cost'] / tmp['Visits']
        tmp['Pro_per_Visits']= tmp['Profit'] / tmp['Visits']
        for c in tmp.columns:
            tmp[c] = tmp[c].map(lambda x:('%.2f')%x)
            tmp = tmp.reset_index()
            return tmp

        return tmp


def main():


    df = load_data()

    st.title("Marketing Campaign Report")
        
        header_html = "<img src='data:image/png;base64,{}' class='img-fluid'>".format(
    img_to_bytes("header.png")
)
st.markdown(
    header_html, unsafe_allow_html=True,
)

    # add sth into sidebar
    text = """
    ## Welcome ##
    ---------------------
    **Analysense Marketing Campaign Analysis**\n
    **-Understand what elements of the campaign worked well/ not so well.
      -Learn how the target audience responded to the campaign.
      -Review the ultimate effectiveness of the campaign versus objectives.**\n
    ---------------------
    """
    st.sidebar.markdown(text)

    #Checkbox
    st.sidebar.subheader("Overview")
    
    st.sidebar.checkbox("Performance of 3 campaigns")
    st.subheader("Performance of three campaigns")
    performance =load_data_sum()
    st.table(performance)

    st.sidebar.subheader("Explore Data")
    df = load_data()
    st.header('Overall Performance')
    status = st.sidebar.selectbox("Overall Perfomance:",["Overall Visits","Overall Profits"])
    if status == "Overall Visits":
        st.subheader("1. Overall Visits")
        fig= px.bar(performance,x ="Campaign",y= "Visits",template = "plotly_dark")
        st.plotly_chart(fig)

    else:
        st.subheader("2. Overall Profit")
        fig = px.bar(performance,x ="Campaign",y= "Profit",template = "plotly_dark")
        st.plotly_chart(fig)

  
    status = st.sidebar.radio("Select one :",("Visits Development","Profit Development","Cost Development","Visits Growth Rate","Profit Growth Rate"))
    if status == "Visits Development":
        st.subheader('3. The development of Visits during 30 weeks')
        fig =px.line(df,x= 'Week', y = 'Visits',color = 'Campaign',template = "plotly_dark")
        st.plotly_chart(fig)

    elif status == "Profit Development":
        st.subheader('4. The development of Profit during 30 weeks')
        fig=px.line(df,x= 'Week', y = 'Profit', color = 'Campaign',template = "plotly_dark")
        st.plotly_chart(fig)

    elif status == "Cost Development":
        st.subheader('5. The development of Cost during 30 weeks')
        fig=px.line(df,x= 'Week', y = 'Cost', color = 'Campaign',template = "plotly_dark")
        st.plotly_chart(fig)


    elif status == "Visits Growth Rate":
        df['diff1'] = df.groupby('Campaign')['Visits'].apply(lambda i:i.diff(1)) 
        df['Visits_Growth Rate %'] = df['diff1']/df['Visits'] *100

        st.subheader("6. The Visits Growth Rate")
        fig =px.scatter(df,x= 'Week', y = 'Visits_Growth Rate %', color = 'Campaign',template = "plotly_dark")
        st.plotly_chart(fig)
    else:
        df['diff1'] = df.groupby('Campaign')['Profit'].apply(lambda i:i.diff(1)) 
        df['Profit_Growth Rate %'] = df['diff1']/df['Profit'] 

        st.subheader("7. The Profit Growth Rate")
        fig =px.scatter(df,x= 'Week', y = 'Profit_Growth Rate %', color = 'Campaign',template = "plotly_dark")
        st.plotly_chart(fig)

    # add a button
    st.sidebar.subheader("Insights")
    text = """
    ### Conclusion: ###
    - **Campaign A** brings the most Visits and least Revenue, the profit from each visit is almost zero.
    - **Campagin B** brings 5188 visits and 7039 revevue,but the profit performance is the worst (negative) due to the expensive cost.
    - **Camgaign C** brings the least Visits but highest Revenue, even the cost is high as well, the profit margin is still good.
    ---------------------
    """
    if st.sidebar.button("Click me"):
        st.markdown(text)

    st.sidebar.subheader("About Author")
    text = """\
    - Analysense INC
    
      """
    st.sidebar.markdown(text)

   

if __name__ == "__main__":
    main()


