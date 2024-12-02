import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Generate timetable
def generate_timetable(start_time, subjects, durations, break_time):
    timetable = []
    current_time = datetime.strptime(start_time, "%H:%M")
    
    for subject, duration in zip(subjects, durations):
        end_time = current_time + timedelta(minutes=duration)
        timetable.append({"Subject": subject, "Start Time": current_time.strftime("%H:%M"), "End Time": end_time.strftime("%H:%M")})
        current_time = end_time
        
        # Add a break after each subject
        if break_time > 0:
            break_start = current_time
            break_end = current_time + timedelta(minutes=break_time)
            timetable.append({"Subject": "Break", "Start Time": break_start.strftime("%H:%M"), "End Time": break_end.strftime("%H:%M")})
            current_time = break_end
    
    return pd.DataFrame(timetable)

# Streamlit app
def main():
    st.title("📚 Student Daily Timetable Planner")
    st.write("Easily create your daily timetable by specifying subjects, study durations, and breaks.")
    
    # Input for timetable
    st.header("🕒 Input Timetable Details")
    start_time = st.time_input("Start Time:", value=datetime.strptime("08:00", "%H:%M").time())
    subjects = st.text_area("Enter Subjects (comma-separated):", "Math, Science, English")
    durations = st.text_area("Enter Durations (minutes, comma-separated):", "60, 45, 50")
    break_time = st.number_input("Break Duration (minutes):", min_value=0, step=5, value=10)

    # Generate timetable
    if st.button("Generate Timetable"):
        try:
            subject_list = [sub.strip() for sub in subjects.split(",")]
            duration_list = [int(dur.strip()) for dur in durations.split(",")]

            if len(subject_list) != len(duration_list):
                st.error("The number of subjects and durations must match!")
            else:
                df_timetable = generate_timetable(start_time.strftime("%H:%M"), subject_list, duration_list, break_time)
                st.success("✅ Timetable Created Successfully!")
                st.dataframe(df_timetable)
                
                # Option to download as CSV
                csv = df_timetable.to_csv(index=False).encode("utf-8")
                st.download_button(label="📥 Download Timetable as CSV", data=csv, file_name="timetable.csv", mime="text/csv")
        except Exception as e:
            st.error(f"Error: {e}")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center;">
            <p>Made with ❤️ for Students</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()

