import streamlit as st
import pandas as pd
import time
from datetime import datetime
import os

# Function to generate the current date and time
def get_current_date_and_time():
    ts = time.time()
    current_date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
    current_time = datetime.fromtimestamp(ts).strftime("%H:%M:%S")
    return current_date, current_time

# Function to display FizzBuzz based on the count
def display_fizzbuzz(count):
    st.subheader("FizzBuzz Counter")
    if count == 0:
        st.write("Count is zero")
    elif count % 3 == 0 and count % 5 == 0:
        st.write("FizzBuzz")
    elif count % 3 == 0:
        st.write("Fizz")
    elif count % 5 == 0:
        st.write("Buzz")
    else:
        st.write(f"Count: {count}")

# Function to read and display the attendance data
def display_attendance_data(date):
    st.subheader("Attendance Data")
    try:
        # Construct the file path with the date
        file_path = os.path.join("Attendance", f"Attendance_{date}.csv")
        df = pd.read_csv(file_path)

        # Check if the DataFrame is not empty
        if not df.empty:
            st.write("### Attendance Records")
            st.dataframe(df.style.highlight_max(axis=0), height=300)
        else:
            st.info("No attendance records found for today.")
    except FileNotFoundError:
        st.warning(f"Attendance file for {date} not found.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Main function to run the Streamlit app
def main():
    # Set page configuration
    st.set_page_config(page_title="Attendance Tracker", layout="centered", page_icon="📝")

    # Sidebar with auto-refresh control
    st.sidebar.title("Settings")
    refresh_interval = st.sidebar.slider("Auto-refresh interval (seconds)", 1, 10, 2)
    st.sidebar.write("This controls how often the page refreshes.")

    # Auto-refresh the app at the specified interval
    from streamlit_autorefresh import st_autorefresh
    count = st_autorefresh(interval=refresh_interval * 1000, limit=100, key="fizzbuzzcounter")

    # App title and description
    st.title("📊 Attendance Tracker with FizzBuzz Counter")
    st.markdown(
        """
        Welcome to the Attendance Tracker app! This app displays attendance records for today and a real-time FizzBuzz counter.
        The page auto-refreshes at a user-defined interval to ensure the latest data is shown.
        """
    )

    # Display FizzBuzz based on the count
    display_fizzbuzz(count)

    # Generate the current date and time
    current_date, current_time = get_current_date_and_time()
    st.sidebar.write(f"Current Date: {current_date}")
    st.sidebar.write(f"Current Time: {current_time}")

    # Display attendance data
    display_attendance_data(current_date)

    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("Developed by [Your Name](https://github.com/yourname)")

if __name__ == "__main__":
    main()
