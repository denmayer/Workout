import streamlit as st
from st_supabase_connection import SupabaseConnection, execute_query
import datetime

st.title("🎈 Workout App")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
# streamlit_app.py

# Initialize connection.
conn = st.connection(name="supabase",type=SupabaseConnection)


def add_exercise(exercise, set, reps, weight, completion_date):
    try:
        execute_query(conn.table("workout_tracking").insert({"exercise_name":exercise,"reps":reps, "set_number": set, "weight": weight, "completion_date": completion_date.strftime("%Y-%m-%d")}, count="None"), ttl='0')
    except Exception as e:
        st.error(f"An error occurred: {e}")



# Perform query.
workout_activities = execute_query(conn.table("workout_tracking").select("*"), ttl=0)

# Fetch data
workout_exercises = execute_query(conn.table("workout_exercises").select("name").order("name",desc=False), ttl=5)
data = [row['name'] for row in workout_exercises.data]

with st.form("workout_form"):
    st.write("Inside the form")
    exercise = st.selectbox(
        "Exercise",
        options=data
    )
    set = st.slider("Set",1,10, key="set")
    reps = st.slider("Reps",1,30, key="reps")
    weight = st.slider("Weight",1,max_value=300, key="weight")
    completion_date = st.date_input("Exercise Date", value="today", format="YYYY-MM-DD")
    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("exercise:", exercise, ", set:", set, ", reps:", reps, ", weight:", weight, ", date:", completion_date)
        if exercise and set:  # Basic validation
            add_exercise(exercise, set, reps, weight, completion_date)
        else:
            st.error("Please fill in all required fields.")

st.write("Outside the form")

# Print results.
# for row in workout_activities.data:
#     st.write(f"{row['exercise_name']} has a :{row['completion_date']}:")

st.table(workout_activities.data)
st.line_chart(workout_activities.data, x="completion_date", y="weight", color="exercise_name")