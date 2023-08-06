from bs4 import BeautifulSoup
import requests
from pprint import pprint

class COVID:

    def __init__(self):
        pass

    #UPDATED ON 8/7/2020
    def get_covid_data(self): # GIVES YOU DATA ON YESTERDAYS COVID STATUS
        #This script will scrap data off the worldometers website to attain each states covid status
        #It targets the table that is on the website that renders the data of all 50 states

        url = 'https://www.worldometers.info/coronavirus/country/us/'

        data = requests.get(url) #get the data object from webpage of url

        content = data.content #get the content (src code) of the webpage -- This content is in byte format

        soup = BeautifulSoup(content,features="html.parser") #call an instance of bsoup, passing in the content
        print(type(soup)) #print the data type of soup

        all_states = soup.find_all('table',id="usa_table_countries_yesterday") #look for the element table with the specfic class name

        content = bytes(str(all_states[0]).replace('\n',''),'utf8') #convert the string into byte representation, #strip all of the new lines in the string

        soup = BeautifulSoup(content,features="html.parser") #pass the byte CONTENT to get the BeautifulSoup instance

        fixed_list = [] #init a empty list
        final_list = soup.find_all('td') #find all of the <td> elements within the table

        for i in final_list[:len(final_list)-96]: #iterate through the list add it to a new list .. replacing all the empty spots with 0
            if '[' not in i.text and i.text.strip() != '':
                fixed_list.append(i.text)
            else: #replace anything that has an empty space with '0'
                fixed_list.append('0')

        state_stats = [] #set a empty list to populate the state's current cases, new cases, death's and new deaths
        state_object = {} #dict to keep the state:[data...]
        counter = 0
        current_state = '' #keep track of the current state that is being proccessed

        for state in fixed_list:
            if counter == 1:
                current_state = state.strip()
            # append all the data from the table into to list
            elif counter in [2,3,4,5,6,7,8,9,10,11,12]:
                state_stats.append(state)
            elif counter == 13:
                state_stats.append(state)
                state_object[current_state] = state_stats
                state_stats = []
                counter = 0
                continue
            counter = counter + 1
        return state_object #returns back a dictionary of the STATES:[DATA]