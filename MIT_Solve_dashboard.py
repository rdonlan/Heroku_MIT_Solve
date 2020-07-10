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


# This method turns any csv file into a panda dataframe
#@st.cache
def csv_to_df(csv_title):   
    created_df = pd.read_csv(csv_title)
    return created_df 

# Creates a variable that is the dataframe we will use for the graphing
total_score_df = csv_to_df('total_Score.csv')
#total_score_df.set_index("Unnamed: 0", inplace=True, drop=True)
# st.write(total_score_df)

# Make sidebar gith aligned
html = """
  <style>
    .reportview-container {
      flex-direction: row-reverse;
    }

    header > .toolbar {
      flex-direction: row-reverse;
      left: 1rem;
      right: auto;
    }

    .sidebar .sidebar-collapse-control,
    .sidebar.--collapsed .sidebar-collapse-control {
      left: auto;
      right: 0.5rem;
    }

    .sidebar .sidebar-content {
      transition: margin-right .3s, box-shadow .3s;
    }

    .sidebar.--collapsed .sidebar-content {
      margin-left: auto;
      margin-right: -21rem;
    }

    @media (max-width: 991.98px) {
      .sidebar .sidebar-content {
        margin-left: auto;
      }
    }
  </style>
"""
st.markdown(html, unsafe_allow_html=True)





# This creates the sidebbar on the left. It also allows the user to select any solver to see their results
# which will be labeled as the selected_solver
st.sidebar.markdown('### Select a Solver to see Their Best Potential Matches')
selected_solver = st.sidebar.selectbox(
    'Solver: ',
     total_score_df.columns[1:])


# This creates the sidebbar on the left. It also allows the user to select any mentor to see their results
# which will be labeled as the selected_mentor
st.sidebar.markdown('### Select a Mentor to see how their information matches up to ' + selected_solver)
selected_mentor = st.sidebar.selectbox(
    'Mentor: ',
     list(total_score_df['Unnamed: 0']))


# This gets top 3 scores mentors that have those scores
st.markdown("## Top Mentor Pair Suggestions for " + selected_solver)
top_three_with_ties = total_score_df.nlargest(3, selected_solver, "all")
labeled_top_three_with_ties = top_three_with_ties[['Unnamed: 0', selected_solver]].set_index("Unnamed: 0")
#st.write(labeled_top_three_with_ties)

# This look ranks the top mentors based on the top 3 scores
previous_score_value = 1000
tied_mentors = []
max_counter = len(labeled_top_three_with_ties)
counter = 1
for mentor in labeled_top_three_with_ties.index:
  total_output_value = labeled_top_three_with_ties[selected_solver][mentor]
  if (previous_score_value == 1000):
    previous_score_value = total_output_value
    tied_mentors.append(mentor)
    counter += 1
  elif ((previous_score_value > total_output_value) and previous_score_value != 1000) or (counter == max_counter):#
    msg = "Output value of " + str(previous_score_value) + ": "
    for mentor_company in tied_mentors:
      msg += str(mentor_company)
      msg += "   ,   "
    st.markdown("#### " +  msg)
    tied_mentors = []
    tied_mentors.append(mentor)
    previous_score_value = total_output_value
    counter += 1
  elif (previous_score_value == total_output_value):
    tied_mentors.append(mentor)
    counter += 1
  


# This gets all mentors top 4 including ties
# st.title("Top Four Matches Including Ties")
top_four_with_ties = total_score_df.nlargest(4, selected_solver, "all")
labeled_top_four_with_ties = top_four_with_ties[['Unnamed: 0', selected_solver]].set_index("Unnamed: 0")

# This for loop ranks the top 4 mentors with numbers on the left hand side
# ranking = 0
# ties = 0
# previous_value = 0
# for mentor in labeled_top_four_with_ties.index:
#   total_output_value = labeled_top_four_with_ties[selected_solver][mentor]
#   if (previous_value == total_output_value):
#     ties += 1
#   else:
#     ranking += ties
#     ties = 0
#     ranking+=1
#     previous_value = total_output_value
#   st.write(str(ranking) + ".   Mentor: " + mentor + " OUTPUT SCORE: " + str(total_output_value))
  
  
  #print(labeled_top_four_with_ties[selected_solver][mentor])



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

# Format the chart
bar_chart_to_display.update_layout(
    autosize=False,
    width=900,
    height=1000,
    margin=dict(
        l=50,
        r=50,
        b=100,
        t=100,
        pad=4
    )
    #paper_bgcolor="LightSteelBlue",
)

st.write(bar_chart_to_display)

# This gets all mentors with the highest value including ties
#st.write(total_score_df.set_index("Unnamed: 0"))
top_values = total_score_df[total_score_df[selected_solver] == total_score_df[selected_solver].max()]
#st.write(top_values['Unnamed: 0'])

# This gets all mentors with the top 4 values not including ties
ordered_df = total_score_df.sort_values(selected_solver, ascending=False)
top_four = ordered_df[:4]['Unnamed: 0']
#top_four = ordered_df[:4].index
#st.write(top_four)




# selected_row_for_chart = total_score_df[total_score_df['Org']==selected_solver]
# st.table(selected_row_for_chart)



# Display more information about the selected solver
solver_needs_df = csv_to_df("excel_to_csv/solver_team_data.csv")
selected_solver_row_info = solver_needs_df[solver_needs_df['Org']==selected_solver].dropna(axis='columns')
st.title("Information on " + selected_solver)
st.table(selected_solver_row_info.set_index("Org"))


# TODO click on bargraph/label and get display more info of mentor
# Display more information about the selected solver
mentor_data_df = csv_to_df("excel_to_csv/partner_data.csv")
selected_mentor_row_info = mentor_data_df[mentor_data_df['Org']==selected_mentor]
st.title("Information on " + selected_mentor)
st.table(selected_mentor_row_info.set_index("Org"))


def updated_mentor_info(trace, points, selector):
  selected_mentor_row_info = mentor_data_df[mentor_data_df['Org']==points]
  st.title("Information on " + points)
  st.table(selected_mentor_row_info.set_index("Org"))

#bar_chart_to_display.on_click(updated_mentor_info)

