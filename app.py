import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


DATE_COLUMNS = ['start', 'end', '_submission_time']
DATA_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTKoYQrQUedW9pe9OR5N29XFAHvJBBrXIKmmG3E-nVRy-2ZPTSt1TjzwVe8KQq3Ng/pub?gid=1630645316&single=true&output=csv'


@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)

    def lowercase(x): return str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    for column in DATE_COLUMNS:
    	data[column] = pd.to_datetime(data[column])
    data['time_taken'] = data['end'] - data['start']
    return data


st.title('RSD Website Survey Analysis')
st.header('Analysis of RSD website usability survey conudcted on February 2021')


data_load_state = st.text('Loading data...')
data = load_data(1200)
data_load_state.text('Loading data... done!')
if st.checkbox('Show raw data'):
    st.write('Sampled raw data')
    st.write(data.sample(5))

final_data = data[data['duplicated_contact'] == 0]
duplicated_count = len(data) - len(final_data)
final_respondents = len(final_data)


st.write("Initially, there were %d respondents who participated in the survey but %d participated responded more than once. \
    Hence the analysis will only consider %d respondents." %(len(data), duplicated_count, final_respondents) )
# st.write(len(data))

st.markdown('---')
st.subheader('Average Time Taken to complete the survery')
seconds = final_data.time_taken.median().total_seconds()
minutes = (seconds % 3600) // 60
seconds = seconds % 60
st.write('{:.0f} minutes, {:.0f} seconds'.format(minutes, seconds))

template='simple_white'
hist_data = final_data[final_data.time_taken.astype('timedelta64[s]')/60 < 50].time_taken.astype('timedelta64[s]')

# fig = px.histogram(x=hist_data.values, y=hist_data.index, template='simple_white', color='gender')
fig = px.strip(final_data, x='time_taken', template=template, color='your current education level', log_x=True,)
fig.update_xaxes(title_text='Time (in seconds) in logscale')
fig.update_layout( legend_title="Education Level")
st.write(fig)


st.markdown('---')
st.subheader('Responses in timeseries')
st.write('The survey ran for 34 days with an average of 30 respondents per day.')
submission = final_data.groupby([final_data._submission_time.dt.date])._id.count()
fig = px.line(x=submission.index, y=submission.values, template=template)
fig.update_xaxes(title_text='Date')
fig.update_yaxes(title_text='Respondents')
st.write(fig)

st.write('From 1:00 AM to 7:00 AM was relatively idle hour with an average of 18 respondents otherwise the average response rate was 51 users per hour. ')
submission = final_data.groupby([final_data._submission_time.dt.hour])._id.count()
fig = px.bar(x=submission.index, y=submission.values, template=template)
fig.update_xaxes(title_text='Hour')
fig.update_yaxes(title_text='Respondents')
st.write(fig)


st.markdown('---')
st.subheader('How did you find the RSD website')
st.markdown('Most of the user either assessed RSD website thorugh Google (and other search engine) or typed the URL directly. Around 9 per cent landed on RSD website through social media like Facebook, Twitter or Instagram.')

def coo_graph(coo):
    if coo == 'All the countries':
        fig = px.histogram(final_data, x='how did you find our website today?', histfunc="sum", color="how did you find our website today?", category_orders={"how did you find our website today?":['I found you on Google (or another search engine)',
       'I typed the website address (URL) in directly',
       'Another UNHCR website', 'A link on Twitter / Facebook / Instagram',
       'Other', 'A link from WhatsApp / Viber / Telegram',
       'A link on another website']}, template=template)
        fig.update_xaxes(title_text='How did you find RSD website today')
        fig.update_yaxes(title_text='Respondents')
        fig.update_layout( legend_title="How did you find RSD website today?")
        st.write(fig)
    else:
        fig = px.histogram(final_data[final_data["what\'s your country of origin?"]==coo], x='how did you find our website today?', histfunc="sum", color="how did you find our website today?", category_orders={"how did you find our website today?":['I found you on Google (or another search engine)',
       'I typed the website address (URL) in directly',
       'Another UNHCR website', 'A link on Twitter / Facebook / Instagram',
       'Other', 'A link from WhatsApp / Viber / Telegram',
       'A link on another website']}, template=template)
        fig.update_xaxes(title_text='How did you find RSD website today')
        fig.update_yaxes(title_text='Respondents')
        fig.update_layout( legend_title="How did you find RSD website today?")
        st.write(fig)


sort_country = list(final_data['what\'s your country of origin?'].unique())
sort_country.append('All the countries')
sort_country = sorted(sort_country)
coo_to_filter = st.selectbox('Select nationality to find out how they accessed RSD site', sort_country)
coo_graph(coo_to_filter)


st.markdown('---')
st.subheader('What is your preferred language of commuication?')
st.markdown('**Arabic** is the most preferred language of communication among Eritrean, Iraqi, South Sudanese, Sudanese, Syrian and Yemeni. 30 per cent of the respondents\' preferred Somali, Tigrinya, Oromo, Amharic and other as a language of communication. Majority of these respondents were Eritrean, Ethiopian and Somali')

def lng_graph(coo):
    if coo == 'All the countries':
        fig = px.histogram(final_data,x='what is your preferred language of communication?', histfunc="sum", template=template)
        fig.update_xaxes(title_text='What is your preferred language of commuication?')
        fig.update_yaxes(title_text='Respondents')
        fig.update_layout( legend_title="What is your preferred language of commuication?")
        st.write(fig)
    else:
        fig = px.histogram(final_data[final_data["what\'s your country of origin?"]==coo],x='what is your preferred language of communication?', histfunc="sum", template=template)
        fig.update_xaxes(title_text='What is your preferred language of commuication?')
        fig.update_yaxes(title_text='Respondents')
        fig.update_layout( legend_title="What is your preferred language of commuication?")
        st.write(fig)

lng_country=sort_country 
lng_to_filter = st.selectbox('Select nationality to find out their language preference', lng_country)
lng_graph(lng_to_filter)


st.markdown('---')
st.subheader('How easy is RSD website to use? ')
st.markdown("Most the respondents find RSD site Very Easy or Easy to use. The reponse remains same among all the age groups.")
def easy_graph(age):
    if age == 'All age groups':
        fig = px.histogram(final_data,x='how easy is our website to use?', histfunc="sum", template=template, color='how easy is our website to use?', category_orders={'how easy is our website to use?':['Very easy', 'Easy', 'Neither easy nor difficult', 'Difficult', 'Very difficult']})
        fig.update_xaxes(title_text='How easy is RSD website to use? ')
        fig.update_yaxes(title_text='Respondents')
        fig.update_layout( legend_title="How easy is RSD website to use? ")
        st.write(fig)
    else:
        fig = px.histogram(final_data[final_data['your age'] == age],x='how easy is our website to use?', histfunc="sum", template=template, color='how easy is our website to use?', category_orders={'how easy is our website to use?':['Very easy', 'Easy', 'Neither easy nor difficult', 'Difficult', 'Very difficult']})
        fig.update_xaxes(title_text='How easy is RSD website to use? ')
        fig.update_yaxes(title_text='Respondents')
        fig.update_layout( legend_title="How easy is RSD website to use? ")
        st.write(fig)

sort_agegp = ['All age groups', 'Under 18', '18-24', '25-34', '35-44', '45-54', '55-64', '65+']
age_to_filter = st.selectbox('Select age group to find out how easy it to use RSD website', sort_agegp)
easy_graph(age_to_filter)



st.markdown("Respondents with **No formal education** and **Elementary school** equally found the website *Neither easy nor difficult to use*")
def easy_graph(education):
    if education == 'All education groups':
        fig = px.histogram(final_data,x='how easy is our website to use?', histfunc="sum", template=template, color='how easy is our website to use?', category_orders={'how easy is our website to use?':['Very easy', 'Easy', 'Neither easy nor difficult', 'Difficult', 'Very difficult']})
        fig.update_xaxes(title_text='How easy is RSD website to use? ')
        fig.update_yaxes(title_text='Respondents')
        fig.update_layout( legend_title="How easy is RSD website to use? ")
        st.write(fig)
    else:
        fig = px.histogram(final_data[final_data['your current education level'] == education],x='how easy is our website to use?', histfunc="sum", template=template, color='how easy is our website to use?', category_orders={'how easy is our website to use?':['Very easy', 'Easy', 'Neither easy nor difficult', 'Difficult', 'Very difficult']})
        fig.update_xaxes(title_text='How easy is RSD website to use? ')
        fig.update_yaxes(title_text='Respondents')
        fig.update_layout( legend_title="How easy is RSD website to use? ")
        st.write(fig)

sort_education = ['All education groups', 'No formal education', 'Elementary school','High school / college', "Bachelor's degree / technical college",  'Masters degree', 'PhD' ]
education_to_filter = st.selectbox('Select education group to find out how easy it to use RSD website', sort_education)
easy_graph(education_to_filter)


st.markdown('---')
st.subheader('How often do you use our website?')
st.markdown('Most of the respondents visited the site on a daily, weekly or monthly basis.')
def visit_graph(education):
    if education == 'All education groups':
        fig = px.histogram(final_data[final_data['how often do you use our website?'].notnull()],x='how often do you use our website?', histfunc="sum", template=template, color='how often do you use our website?', category_orders={'how often do you use our website?':['Often (daily)', 'Regularly (weekly)', 'Sometimes (monthly)', 'Rarely (every few months)', 'This is the first time']})
        fig.update_xaxes(title_text='How often do you use our website?')
        fig.update_yaxes(title_text='Respondents')
        fig.update_layout( legend_title="How often do you use our website?")
        st.write(fig)
    else:
        fig = px.histogram(final_data[final_data['your current education level'] == education],x='how often do you use our website?', histfunc="sum", template=template, color='how often do you use our website?', category_orders={'how often do you use our website?':['Often (daily)',  'Regularly (weekly)', 'Sometimes (monthly)', 'Rarely (every few months)', 'This is the first time']})
        fig.update_xaxes(title_text='How often do you use our website?')
        fig.update_yaxes(title_text='Respondents')
        fig.update_layout( legend_title="How often do you use our website?")
        st.write(fig)

sort_education = ['All education groups', 'No formal education', 'Elementary school','High school / college', "Bachelor's degree / technical college", 'Masters degree', 'PhD']
education_to_filter = st.selectbox('Select education group to find out how often they visit the site', sort_education)
visit_graph(education_to_filter)


st.markdown('21 per cent of the total respondents had visited the site the **first time**. Most of these respondents were from Sudan, Syria and South Sudan.')
def visit_coo_graph(coo):
    if coo == 'All the countries':
        fig = px.histogram(final_data,x='how often do you use our website?', histfunc="sum", template=template, color='how often do you use our website?', category_orders={'how often do you use our website?':['Often (daily)', 'Regularly (weekly)', 'Sometimes (monthly)', 'Rarely (every few months)', 'This is the first time']})
        fig.update_xaxes(title_text='How often do you use our website?')
        fig.update_yaxes(title_text='Respondents')
        fig.update_layout( legend_title="How often do you use our website?")
        st.write(fig)
    else:
        fig = px.histogram(final_data[final_data["what\'s your country of origin?"]==coo],x='how often do you use our website?', histfunc="sum", template=template, color='how often do you use our website?', category_orders={'how often do you use our website?':['Often (daily)',  'Regularly (weekly)', 'Sometimes (monthly)', 'Rarely (every few months)', 'This is the first time']})
        fig.update_xaxes(title_text='How often do you use our website?')
        fig.update_yaxes(title_text='Respondents')
        fig.update_layout( legend_title="How often do you use our website?")
        st.write(fig)


sort_visit_coo = sort_country 
visit_coo_to_filter = st.selectbox('Select nationality to find out how often they visit the site', sort_visit_coo)
visit_coo_graph(visit_coo_to_filter)


st.markdown('---')
st.subheader('Do you have your own smartphone')
st.markdown('Majority of the respondents had their own smartphones - mostly Android. 90 per cent either owned smartphone or shared smartphone with their family or frineds. 10 per cent of the respondents do not have their own smartphone. ')
def coo_smart_graph(coo):
    if coo == 'All the countries':
        piegraph_data = final_data.groupby('do you have your own smartphone?')['_id'].count()
        fig = px.pie(piegraph_data, values=piegraph_data.values, names=piegraph_data.index, template=template, color_discrete_map={'I have an Android smartphone': '#2ba02b', "I don't have access to a smartphone": '#d62827', 'I have an Apple/iOS smartphone': '#545c84', 'I share an Android smartphone with my family or friends' : '#7dc388', 'I share an Apple/iOS smartphone with my family or friends': '#808c9d'})
        st.write(fig)
    else:
        piegraph_data = final_data[final_data["what\'s your country of origin?"]==coo].groupby('do you have your own smartphone?')['_id'].count()
        fig = px.pie(piegraph_data, values=piegraph_data.values, names=piegraph_data.index, template=template, color_discrete_map={'I have an Android smartphone': '#2ba02b', "I don't have access to a smartphone": '#d62827', 'I have an Apple/iOS smartphone': '#545c84', 'I share an Android smartphone with my family or friends' : '#7dc388', 'I share an Apple/iOS smartphone with my family or friends': '#808c9d'})
        st.write(fig)
sort_visit_coo = sort_country 
visit_coo_to_filter = st.selectbox('Select nationality to find out whether they have their own smartphone', sort_visit_coo)
coo_smart_graph(visit_coo_to_filter)


st.markdown('---')
st.subheader('Do you have access to the internet vs owning smartphone')
st.markdown('60 per cent of the respondents had access to the internet and 40 per cent did not.')
sanky_graph = final_data.groupby(['do you always have access to the internet?','do you have your own smartphone?'])['_id'].count().to_frame().reset_index()
sanky_graph.columns=['source', 'target', 'value']
# sanky_graph.head()
# # label = ["ZERO", "ONE", "TWO", "THREE", "FOUR", "FIVE"]
# source = list(sanky_graph.source)
# target = list(sanky_graph.target)
# value = list(sanky_graph.value)
# # data to dict, dict to sankey
# link = dict(source = source, target = target, value = value)
# node = dict( pad=50, thickness=5)
# data = go.Sankey(link = link, node=node)
# # plot
# fig = go.Figure(data)
# st.write(fig)
fig = px.sunburst(sanky_graph, path=[
    'source', 'target'], values='value', width=800, height=600, template=template)
st.write(fig)