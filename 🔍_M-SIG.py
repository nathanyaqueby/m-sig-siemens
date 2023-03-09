import pandas as pd
from bs4 import BeautifulSoup
import requests as r
import streamlit as st

from GoogleNews import GoogleNews
import warnings
warnings.filterwarnings('ignore')
from gnews import GNews

user_agent = 'Mozilla/5.0'

st.set_page_config(
    page_title="🔍 M-SIG: Sustainable Information Grabber",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/nathanyaqueby/m-sig-siemens',
        'Report a bug': "https://github.com/nathanyaqueby/m-sig-siemens",
        'About': "An all-in-one place digital platform that would help equip MSMEs with the power of extracting useful sustainability information with regards to regulations, best practices, technology, or financing in sustainability through the help of NLP and deep learning models."
    }
)

st.markdown('<h1 style=padding-bottom: 20px;">🔍 M-SIG: Sustainable Information Grabber</h1>', unsafe_allow_html=True)
st.markdown("Welcome to *_M-SIG_*! Here, you can:")
st.markdown("- Write a query to search for news articles on the topic of your choice")
st.markdown("- Analyze agricultural production in multiple countries.")
st.markdown("- Read more about our project on [GitHub](https://github.com/nathanyaqueby/m-sig-siemens).")

st.markdown('''
<style>
[data-testid="stMarkdownContainer"] ul{
    padding-left:40px;
}
</style>
''', unsafe_allow_html=True)

query = st.text_input('Insert your query here', help='Enter the search string and hit Enter/Return')
query = query.replace(" ", "+") #replacing the spaces in query result with + sign

# googlenews = GoogleNews()
# google_news = GNews()
# googlenews.enableException(True)
# googlenews = GoogleNews(lang='en', region='IN')
# googlenews.max_results=7

# sidebar
with st.sidebar.form(key='Form1'):
    st.title("🌏 Energy efficiency")
    st.image("charts sig/1.png", width=250)
    st.markdown("Energy efficiency is the goal of reducing the amount of energy required to provide products and services. "
                "Energy efficiency is also a resource that can be used to provide other services, such as providing "
                "electricity during times of peak demand.")
    
    st.title("🌏 Gas emisions")
    st.image("charts sig/2.png", width=250)
    st.markdown("Gas emissions are the gases that are released into the atmosphere by human activities. "
                "These gases are released into the atmosphere by burning fossil fuels, "
                "such as coal, oil, and natural gas, and by deforestation.")

    generator = st.form_submit_button(label='Download the report')	

if query: #Activates the code below on hitting Enter/Return in the search textbox
    try:#Exception handling 
        req = r.get(f"https://www.bing.com/search?q={query}",
                    headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"})
        result_str = '<html><table style="border: none;">' #Initializing the HTML code for displaying search results
        
        if req.status_code == 200: #Status code 200 indicates a successful request
            bs = BeautifulSoup(req.content, features="html.parser") #converting the content/text returned by request to a BeautifulSoup object
            search_result = bs.find_all("li", class_="b_algo") #'b_algo' is the class of the list object which represents a single result
            search_result = [str(i).replace("<strong>","") for i in search_result] #removing the <strong> tag
            search_result = [str(i).replace("</strong>","") for i in search_result] #removing the </strong> tag
            result_df = pd.DataFrame() #Initializing the data frame that stores the results
            
            for n,i in enumerate(search_result): #iterating through the search results
                individual_search_result = BeautifulSoup(i, features="html.parser") #converting individual search result into a BeautifulSoup object
                h2 = individual_search_result.find('h2') #Finding the title of the individual search result
                href = h2.find('a').get('href') #title's URL of the individual search result
                cite = f'{href[:50]}...' if len(href) >= 50 else href # cite with first 20 chars of the URL
                url_txt = h2.find('a').text #title's text of the individual search result

                #In a few cases few individual search results doesn't have a description. In such cases the description would be blank
                description = "" if individual_search_result.find('p') is None else individual_search_result.find('p').text
                #Appending the result data frame after processing each individual search result
                result_df = result_df.append(pd.DataFrame({"Title": url_txt, "URL": href, "Description": description}, index=[n]))
                count_str = f'<b style="font-size:20px;">Google News search returned {len(result_df)} results</b>'
                ########################################################
                ######### HTML code to display search results ##########
                ########################################################
                result_str += f'<tr style="border: none;"><h3><a href="{href}" target="_blank">{url_txt}</a></h3></tr>'+\
                f'<tr style="border: none;"><strong style="color:green;">{cite}</strong></tr>'+\
                f'<br><tr style="border: none;">{description}</tr>'+\
                f'<tr style="border: none;"><td style="border: none;"></td></tr>'
            result_str += '</table></html>'
            
        #if the status code of the request isn't 200, then an error message is displayed along with an empty data frame        
        else:
            result_df = pd.DataFrame({"Title": "", "URL": "", "Description": ""}, index=[0])
            result_str = '<html></html>'
            count_str = '<b style="font-size:20px;">Looks like an error!!</b>'
            
    #if an exception is raised, then an error message is displayed along with an empty data frame
    except:
        result_df = pd.DataFrame({"Title": "", "URL": "", "Description": ""}, index=[0])
        result_str = '<html></html>'
        count_str = '<b style="font-size:20px;">Looks like an error!!</b>'
    
    st.markdown(f'{count_str}', unsafe_allow_html=True)
    st.markdown(f'{result_str}', unsafe_allow_html=True)
    st.markdown('<h3>Dataframe of the above search result</h3>', unsafe_allow_html=True)
    st.dataframe(result_df)


### Google News
# if query: #Activates the code below on hitting Enter/Return in the search textbox

#     googlenews.get_news(f'{query}')
#     result_list=googlenews.results()

#     for i in range(0, len(result_list)):
#         html = r.get(f"http://{result_list[i]['link']}", headers={'User-Agent': user_agent}).content
#         soup = BeautifulSoup(html, 'html.parser')
#         search_result = soup.find_all("li", class_="b_algo") #'b_algo' is the class of the list object which represents a single result
#         search_result = [str(i).replace("<strong>","") for i in search_result] #removing the <strong> tag
#         search_result = [str(i).replace("</strong>","") for i in search_result] #removing the </strong> tag
        
#         result_list[i]["description"] = "" if soup.find('p') is None else soup.find('p').text
#         result_list[i]["img"] = soup.find('img')['src'] if soup.find('img') else ""

#     result_df = pd.DataFrame(result_list)

#     # Displaying the results in a table
#     st.markdown('<h3>Google News Search Results</h3>', unsafe_allow_html=True)

#     result_str = '<html><table style="border: none;">'  # Initializing the HTML code for displaying search results

#     for n,i in enumerate(result_list): # iterating through the search results
#         # individual_search_result = BeautifulSoup(search_result[n], features="html.parser") # converting individual search result into a BeautifulSoup
#         # In a few cases few individual search results doesn't have a description. In such cases the description would be blank
#         # description = "" if individual_search_result.find('p') is None else individual_search_result.find('p').text
#         # i["description"] = "" if individual_search_result.find('p') is None else individual_search_result.find('p').text

#         count_str = f'<b style="font-size:20px;">Search returned {len(result_list)} results</b>'

#         ########################################################
#         ######### HTML code to display search results ##########
#         ########################################################

#         result_str += f'<tr style="border: none;"><h3><a href="http://{i["link"]}" target="_blank">{i["title"]}</a></h3></tr>'+\
#         f'<tr style="border: none;"><img src="{i["img"]}" width="10"/></tr>'+\
#         f'<tr style="border: none;"><strong style="color:green;">{i["media"]}</strong></tr>'+\
#         f'<tr style="border: none;"><p>{i["description"]}</p></tr>'+\
#         f'<tr style="border: none;"><td style="border: none;"></td></tr>'
#     result_str += '</table></html>'

#     st.markdown(f'{count_str}', unsafe_allow_html=True)
#     st.markdown(f'{result_str}', unsafe_allow_html=True)
#     st.dataframe(result_df)