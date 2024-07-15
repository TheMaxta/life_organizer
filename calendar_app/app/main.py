import streamlit as st
import calendar
from datetime import datetime, timedelta
from calendar_app.models.calendar import Calendar
from calendar_app.models.actions import RoutineAction, UncommonAction, Frequency
from calendar_app.database import init_db
from calendar_app.utils.llm_integration import get_llm_guidance

def display_calendar(year, month, user_calendar):
    cal = calendar.monthcalendar(year, month)
    month_name = calendar.month_name[month]
    
    st.markdown(f"## {month_name} {year}")
    
    cols = st.columns(7)
    for i, day in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]):
        cols[i].markdown(f"**{day}**")
    
    for week in cal:
        cols = st.columns(7)
        for i, day in enumerate(week):
            if day == 0:
                cols[i].write("")
            else:
                date = datetime(year, month, day).date()
                actions = user_calendar.get_actions_for_date(date)
                if actions:
                    cols[i].markdown(f"**{day}**\n{len(actions)} actions")
                else:
                    cols[i].write(day)

def generate_time_options():
    times = []
    for hour in range(24):
        for minute in [0, 30]:
            time = datetime.strptime(f"{hour:02d}:{minute:02d}", "%H:%M").strftime("%I:%M %p")
            times.append(time)
    return times

def time_input(label, key):
    time_options = generate_time_options()
    selected_time = st.selectbox(label, time_options, key=key)
    return datetime.strptime(selected_time, "%I:%M %p").time()

def duration_input(label, key):
    hours = st.number_input(f"{label} (hours)", min_value=0, value=1, step=1, key=f"{key}_hours")
    minutes = st.selectbox(f"{label} (minutes)", [0, 30], key=f"{key}_minutes")
    return timedelta(hours=hours, minutes=minutes)


def display_updates(suggested_updates):
    st.subheader("Suggested Updates")
    for action in suggested_updates['actions']:
        st.write(f"Operation: {action['operation']}")
        st.write(f"Name: {action['name']}")
        st.write(f"Description: {action['description']}")
        st.write(f"Time: {action['start_time']} - {action['end_time']}")
        if action['type'] == 'RoutineAction':
            st.write(f"Days: {', '.join([calendar.day_name[d] for d in action['days']])}")
            st.write(f"Frequency: {action['frequency']}")
        else:
            st.write(f"Date: {action['date']}")
        st.write("---")

def apply_updates(calendar, suggested_updates):
    for action in suggested_updates['actions']:
        if action['operation'] == 'add':
            if action['type'] == 'RoutineAction':
                new_action = RoutineAction(
                    action['name'],
                    action['description'],
                    datetime.strptime(action['start_time'], "%H:%M").time(),
                    datetime.strptime(action['end_time'], "%H:%M").time(),
                    action['days'],
                    Frequency[action['frequency']]
                )
            else:
                new_action = UncommonAction(
                    action['name'],
                    action['description'],
                    datetime.strptime(action['start_time'], "%H:%M").time(),
                    datetime.strptime(action['end_time'], "%H:%M").time(),
                    datetime.strptime(action['date'], "%Y-%m-%d").date()
                )
            calendar.add_action(new_action)
        elif action['operation'] == 'update':
            # Implement update logic
            pass
        elif action['operation'] == 'delete':
            # Implement delete logic
            pass
    return calendar


def main():
    st.title("Personalized Calendar App")
    
    # Initialize the database
    init_db()


    # Create a new Calendar instance for this session
    if 'calendar' not in st.session_state:
        st.session_state.calendar = Calendar()
    

    today = datetime.now()
    display_calendar(today.year, today.month, st.session_state.calendar)

    tab1, tab2, tab3, tab4 = st.tabs(["Add Routine Action", "Add Uncommon Action", "View Actions", "Get AI Guidance"])

    with tab1:
        st.header("Add Routine Action")
        routine_name = st.text_input("Action Name", key="routine_name")
        routine_description = st.text_area("Description", key="routine_description")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            start_time = time_input("Start Time", "routine_start")
        with col2:
            duration = duration_input("Duration", "routine_duration")
        with col3:
            calculated_end_time = (datetime.combine(datetime.today(), start_time) + duration).time()
            end_time = time_input("End Time", "routine_end")
            st.write(f"Calculated End Time: {calculated_end_time.strftime('%I:%M %p')}")
        
        routine_days = st.multiselect("Days", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], key="routine_days")
        routine_frequency = st.selectbox("Frequency", ["Daily", "Weekly", "Monthly", "Yearly"], key="routine_frequency")

        if st.button("Add Routine Action"):
            days = [["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"].index(day) for day in routine_days]
            frequency = Frequency[routine_frequency.upper()]
            action = RoutineAction(routine_name, routine_description, start_time, end_time, days, frequency)
            st.session_state.calendar.add_action(action)
            st.success(f"Added routine action: {routine_name}")

    with tab2:
        st.header("Add Uncommon Action")
        uncommon_name = st.text_input("Uncommon Action Name", key="uncommon_name")
        uncommon_description = st.text_area("Uncommon Action Description", key="uncommon_description")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            start_time = time_input("Start Time", "uncommon_start")
        with col2:
            duration = duration_input("Duration", "uncommon_duration")
        with col3:
            calculated_end_time = (datetime.combine(datetime.today(), start_time) + duration).time()
            end_time = time_input("End Time", "uncommon_end")
            st.write(f"Calculated End Time: {calculated_end_time.strftime('%I:%M %p')}")
        
        uncommon_date = st.date_input("Date", key="uncommon_date")

        if st.button("Add Uncommon Action"):
            action = UncommonAction(uncommon_name, uncommon_description, start_time, end_time, uncommon_date)
            st.session_state.calendar.add_action(action)
            st.success(f"Added uncommon action: {uncommon_name}")

    with tab3:
        st.header("View Actions")
        view_date = st.date_input("Select Date to View", key="view_date")
        actions_for_date = st.session_state.calendar.get_actions_for_date(view_date)

        if actions_for_date:
            for action in actions_for_date:
                st.markdown(f"**{action.name}**")
                st.markdown(f"*{action.description}*")
                st.markdown(f"Time: {action.start_time.strftime('%I:%M %p')} - {action.end_time.strftime('%I:%M %p')}")
                st.markdown("---")
        else:
            st.write("No actions scheduled for this date.")

    with tab4:

        st.header("Get AI Guidance")
        user_input = st.text_area("Describe changes to your calendar")
        if st.button("Get Guidance"):
            current_calendar = st.session_state.calendar.to_json()
            suggested_updates = get_llm_guidance(user_input, current_calendar)
            
            if 'error' in suggested_updates:
                st.error(suggested_updates['error'])
            else:
                display_updates(suggested_updates)
                if st.button("Apply Changes"):
                    st.session_state.calendar = apply_updates(st.session_state.calendar, suggested_updates)
                    st.success("Calendar updated successfully!")

    # Close the database session when the app is done
    st.session_state.calendar.close()

if __name__ == "__main__":
    main()