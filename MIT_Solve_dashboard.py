import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# To run this application on your localhost you must first cd into the directory
# containing MIT_Solve_dashboard.py and then in your terminal run 
# $ streamlit run MIT_Solve_dashboard.py
# which will open the dashboard in a new tab on your browser

# Title for page
st.title('Matching Page for MIT Solve')

# Below are place holders for the top 4 mentor matches
# More thought must go into what information we want to represent about them besides output score
# Need to figure out where to dynamically place output score to the left of mentor description and not within it

st.write("### Here is where the best mentor match will go ---------- OUTPUT SCORE: 96\n"
"the rest of the info we want to put will go here")

st.write("### Here is where the second best mentor match will go ---- OUTPUT SCORE: 87\n"
"the rest of the info we want to put will go here")

st.write("### Here is where the third best mentor match will go ---- OUTPUT SCORE: 82\n"
"the rest of the info we want to put will go here")

st.write("### Here is where the fourth best mentor match will go ---- OUTPUT SCORE: 76\n"
"the rest of the info we want to put will go here")

# This method turns any csv file into a panda dataframe
#@st.cache
def csv_to_df(csv_title):   
    created_df = pd.read_csv(csv_title)
    return created_df 

# Creates a variable that is the dataframe we will use for the graphing
total_score_df = csv_to_df('total_Score.csv')
#total_score_df.set_index("Unnamed: 0", inplace=True, drop=True)
# st.write(total_score_df)

# This creates the sidebbar on the left. It also allows the user to select any solver to see their results
# which will be labeled as the selected_solver
selected_solver = st.sidebar.selectbox(
    'Select a Solver',
     total_score_df.columns[1:])

# This creates the sidebbar on the left. It also allows the user to select any mentor to see their results
# which will be labeled as the selected_mentor
selected_mentor = st.sidebar.selectbox(
    'Select a Mentor',
     list(total_score_df['Unnamed: 0']))

# Creates the pylotly express bar chart that will be displayed
# TODO Want to make this look prettier
mentors = list(total_score_df['Unnamed: 0'])
bar_chart_to_display = px.bar(
  total_score_df, x=selected_solver, y=mentors,
  labels={selected_solver:'Total Score', 'y':'Mentor'}, 
  height=1000, width=1000,
  hover_name=mentors,
  hover_data={selected_solver:True} #Here we will put all data we want on hover
)
bar_chart_to_display.update_layout(yaxis={'categoryorder':'total ascending'})
st.write(bar_chart_to_display)

# This gets all mentors with the highest value including ties
st.write(total_score_df)
top_values = total_score_df[total_score_df[selected_solver] == total_score_df[selected_solver].max()]
#st.write(top_values['Unnamed: 0'])

# This gets all mentors with the top 4 values not including ties
ordered_df = total_score_df.sort_values(selected_solver, ascending=False)
top_four = ordered_df[:4]['Unnamed: 0']
#top_four = ordered_df[:4].index
#st.write(top_four)

# This gets all mentors top 4 including ties
st.title("Top Four Matches Including Ties")
top_four_with_ties = total_score_df.nlargest(4, selected_solver, "all")
st.write(top_four_with_ties)


# selected_row_for_chart = total_score_df[total_score_df['Org']==selected_solver]
# st.table(selected_row_for_chart)



# Display more information about the selected solver
solver_needs_df = csv_to_df("excel_to_csv/solver_team_data.csv")
selected_solver_row_info = solver_needs_df[solver_needs_df['Org']==selected_solver]
st.title("More information on " + selected_solver)
st.write(selected_solver_row_info)


# TODO click on bargraph/label and get display more info of mentor
# Display more information about the selected solver
mentor_data_df = csv_to_df("excel_to_csv/partner_data.csv")
selected_mentor_row_info = mentor_data_df[mentor_data_df['Org']==selected_mentor]
st.title("More information on " + selected_mentor)
st.write(selected_mentor_row_info)