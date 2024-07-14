import streamlit as st
from models.calendar import Calendar
from models.actions import RoutineAction, UncommonAction, Frequency
from utils.llm_integration import get_llm_guidance

def main():
    st.title("Personalized Calendar App")

    if 'calendar' not in st.session_state:
        st.session_state.calendar = Calendar()

    # Add Routine Action
    st.header("Add Routine Action")
    routine_name = st.text_input("Action Name")
    routine_description = st.text_area("Description")
    routine_duration = st.number_input("Duration (minutes)", min_value=1, value=30)
    routine_days = st.multiselect("Days", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    routine_frequency = st.selectbox("Frequency", ["Daily", "Weekly", "Monthly", "Yearly"])

    if st.button("Add Routine Action"):
        days = [["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"].index(day) for day in routine_days]
        frequency = Frequency[routine_frequency.upper()]
        action = RoutineAction(routine_name, routine_description, routine_duration, days, frequency)
        st.session_state.calendar.add_action(action)
        st.success(f"Added routine action: {routine_name}")

    # Add Uncommon Action
    st.header("Add Uncommon Action")
    uncommon_name = st.text_input("Uncommon Action Name")
    uncommon_description = st.text_area("Uncommon Action Description")
    uncommon_duration = st.number_input("Uncommon Action Duration (minutes)", min_value=1, value=60)
    uncommon_date = st.date_input("Date")

    if st.button("Add Uncommon Action"):
        action = UncommonAction(uncommon_name, uncommon_description, uncommon_duration, uncommon_date)
        st.session_state.calendar.add_action(action)
        st.success(f"Added uncommon action: {uncommon_name}")

    # View Calendar
    st.header("View Calendar")
    view_date = st.date_input("Select Date to View")
    actions_for_date = st.session_state.calendar.get_actions_for_date(view_date)

    if actions_for_date:
        for action in actions_for_date:
            st.markdown(f"**{action.name}**")
            st.markdown(f"*{action.description}*")
            st.markdown(f"Duration: {action.duration} minutes")
            st.markdown("---")
    else:
        st.write("No actions scheduled for this date.")

    # LLM Guidance
    st.header("Get AI Guidance")
    user_query = st.text_input("Ask for guidance based on your calendar")
    if st.button("Get Guidance"):
        calendar_json = st.session_state.calendar.to_json()
        try:
            guidance = get_llm_guidance(calendar_json, user_query)
            st.write(guidance)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()