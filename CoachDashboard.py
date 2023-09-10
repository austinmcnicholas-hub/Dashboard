import streamlit as st
import pandas as pd
import altair as alt
import pyperclip
from datetime import datetime


# Load your Excel data 
df = pd.read_excel(
        io='Elite.xlsx',
        engine='openpyxl',
        sheet_name='Coach Austin',
        skiprows=[],
        nrows=127,
)


# Define a placeholder for the selected username and profile picture
selected_username = None
profile_picture = None

# Store user notes in session state
if 'user_notes' not in st.session_state:
    st.session_state.user_notes = {}

def calculate_renewal_date(start_date, membership_type):
    if membership_type == 'Legacy':
        # Calculate the renewal date as 3 months from the start date
        renewal_date = start_date + pd.DateOffset(months=3)
        return renewal_date.strftime('%m/%d/%Y')  # Format date as mm/dd/yyyy
    
    elif membership_type == "Pro":
        # Calculate the renewal date as 1 month from the start date
        renewal_date_pro = start_date + pd.DateOffset(months=1)
        return renewal_date_pro.strftime('%m/%d/%Y') # Format date as mm/dd/yyyy

    elif membership_type == "Elite Academy":
        # Calculate the renewal date as 1 month from the start date
        renewal_date_elite = start_date + pd.DateOffset(months=1)
        return renewal_date_elite.strftime('%m/%d/%Y') # Format date as mm/dd/yyyy
    
    else:
        return " "

def format_date(date):
    if pd.notna(date):
        return date.strftime('%m/%d/%Y')  # Format date as mm/dd/yyyy
    else:
        return ''

def roster_search(df):
    global selected_username  # Store the selected username globally
    st.subheader("Roster Search")

    # NAV Search Form
    with st.form(key='searchform'):
        nav1, nav2, nav3 = st.columns([3, 2, 2])

        with nav1:
            Name = st.text_input("Search Name")
        with nav2:
            Username = st.text_input("Search Username")
        with nav3:
            Email = st.text_input("Search Email")
            st.text("Search")
            submit_search = st.form_submit_button(label='Search')

    if submit_search:
        # Perform the search based on Name, Username, and Email
        filtered_df = df[
            (df['Name'].str.contains(Name, case=False)) &
            (df['Username'].str.contains(Username, case=False)) &
            (df['Email'].str.contains(Email, case=False))
        ]

        if not filtered_df.empty:
            # Display the filtered roster as a dropdown
            selected_username = st.selectbox("Select a Username:", filtered_df['Username'].tolist())

        else:
            st.warning("No matching records found.")
            selected_username = None

    if selected_username:
        st.subheader(f"Profile: {selected_username}")

        # Find the selected user's profile from the DataFrame
        selected_profile = df[df['Username'] == selected_username].iloc[0]

        # Display the profile information
        st.write(f"**Name:** {selected_profile['Name']}")
        st.write(f"**Email:** {selected_profile['Email']}")

        # Display the membership type
        st.write(f"**Membership Type:** {selected_profile['Membership']}")

        selected_start_date = selected_profile['Start_Date']
        if not pd.isna(selected_start_date):
            st.subheader("Renewal Date:")
            st.markdown(f"<p style='color:red;text-align:center;font-size:24px;'>🔥 {calculate_renewal_date(selected_start_date, selected_profile['Membership'])} 🔥</p>", unsafe_allow_html=True)

        # Display the user's start date as text
        if not pd.isna(selected_start_date):
            st.subheader("Start Date:")
            st.text(format_date(selected_start_date))

        # Allow users to view and edit notes for this profile
        notes_key = f"{selected_username}_notes"
        notes = st.text_area(f"Notes for {selected_username}", st.session_state.user_notes.get(notes_key, selected_profile['Notes']))

        # Update the session state with the user's notes
        st.session_state.user_notes[notes_key] = notes

def create_membership_bar_chart(df):
    # Count the number of members for each membership type
    membership_counts = df['Membership'].value_counts().reset_index()
    membership_counts.columns = ['Membership Type', 'Number of Members']

    return membership_counts

def main():
    menu = ["Main Menu", "Roster Search", "Buttons", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    selected_membership = st.sidebar.multiselect(
        "Filter by Membership:",
        options=df["Membership"].unique(),
        default=df["Membership"].unique()
    )

    if choice == "Main Menu":
        st.subheader(":baseball: Main Menu")
        st.markdown("##")

        # Filter DataFrame based on selected memberships
        df_selection = df[df["Membership"].isin(selected_membership)]

        # Calculate total_members
        total_members = df_selection.shape[0]

        # Calculate average rating
        average_rating = round(df_selection['Rating'].mean(), 1)

        # Calculate revenue (replace 'Your_Column_Name_Here' with the actual column name)
        revenue = df_selection['Payment_Per_Month'].sum()

        left_column, middle_column, right_column, right_column_dante = st.columns(4)
        with left_column:
            st.subheader(":100: Roster Count")
            st.subheader(str(total_members))
        with middle_column:
            st.subheader(":sparkling_heart: Coach Rating")
            st.write(f"{average_rating}", key="average_rating")
        with right_column:
            st.subheader(":money_mouth_face: Monthly Revenue")
            st.subheader(revenue)
        # Display the 5 most recent upcoming usernames with renewal dates in the right column
        with right_column_dante:
            st.subheader(":pencil: Renewals To Come")
            today = pd.Timestamp(datetime.today().date())  # Convert to Pandas Timestamp
            future_profiles = df_selection[df_selection['Renewal'] > today].sort_values(by='Renewal').head(5)
            
            if not future_profiles.empty:
                for index, row in future_profiles.iterrows():
                    st.write(f"{row['Username']} - {format_date(row['Renewal'])}")
            else:
                st.write("No upcoming renewals.")
            

        st.markdown("---")

        membership_data = create_membership_bar_chart(df_selection)

        # Create a bar chart using Altair
        chart = alt.Chart(membership_data).mark_bar().encode(
            x=alt.X('Membership Type:N', title='Membership Type'),
            y=alt.Y('Number of Members:Q', title='Number of Members'),
            color=alt.Color('Membership Type:N', legend=None)  # Assigns colors to each bar
        ).properties(
            width=600,
            height=400
        )

        # Display the chart using Streamlit
        st.altair_chart(chart)

    elif choice == "Roster Search":
        roster_search(df)  # Call the roster_search function

    elif choice == "Buttons":
        # Create a Button for Elite Directions to Schedule
        if st.button("WIN Reality Scheduling"):
            instructions = """
            
https://dashboard.winreality.com/app/win-elite/schedule
            
Directions to schedule your next WIN Elite Session
            1. Visit the WIN Dashboard and login to your account.
            2. Select your specific WIN profile you want to schedule sessions with in the top right.
            3. Navigate to the “Elite Coaches Sessions” under the WIN Elite section of your dashboard.
            4. Here you can see what session you are on, how many sessions you have left before your renewal date, and when your next session is.
            5. Schedule by clicking “Schedule Elite Session”, finding a time that works with you, and then clicking ‘confirm’.
            6. You can only schedule one session at a time.
            7. If you need to reschedule, click cancel and repeat steps 2-5.
            8. You can always schedule, cancel or reschedule by reaching out to me!
           
 Let me know if you have any difficulties running through this, and I’ll be happy to assist.
            """
            pyperclip.copy(instructions)
            st.success("Instructions copied to clipboard!")

        if st.button("GBB Hitting Lesson Link"):
            link = """
https://calendly.com/austin-mcnicholas/win-reality-gbb-hitting-lesson 
            """
            pyperclip.copy(link)
            st.success("Link Has Been Copied")

        if st.button("Slow and Early Load"):
            load = """
https://www.youtube.com/watch?v=NFjoMkBFrB0 
            """
            pyperclip.copy(load)
            st.success("Link Has Been Copied")

        if st.button("Personal Survey"):
            personal_survey = """
https://docs.google.com/forms/d/e/1FAIpQLSf-ARh2xeArN2CiWgCcxg23PWfnOp7X4jo7aWYReANTT9HpBw/viewform 
            """
            pyperclip.copy(personal_survey)
            st.success("Survey Has Been Copied")

        if st.button("GBB Survey"):
            gbb_survey = """
https://docs.google.com/forms/d/e/1FAIpQLSfMyUE9U1VQuNI9DJ359yLJ91QTq8u5Zzhz4OhYtjTGBti-bQ/viewform?usp=sf_link 
            """
            pyperclip.copy(gbb_survey)
            st.success("Survey Has Been Copied")

        if st.button("Palm Up"):
            palm = """
https://www.youtube.com/shorts/PHtXbYYqOJ0
            """
            pyperclip.copy(palm)
            st.success("Palm Up Video Has Been Copied")

        if st.button("GBB Reminder Text"):
            text = """
            Hey its Coach Austin from WIN Reality, just checking in... wanted to let you know the membership that you have chosen also includes 1 on 1 coaching with me! Below is the link to my calendar, if you have any questions shoot me an email or text! 

https://calendly.com/austin-mcnicholas/win-reality-gbb-hitting-lesson

- Coach Austin
Former Professional Baseball Player, University of Texas
            """
            pyperclip.copy(text)
            st.success("Copied Text")

            
    else:
        st.subheader("About")

        # Display the DataFrame on the "About" page
        st.subheader("DataFrame Display")
        st.dataframe(df)

if __name__ == '__main__':
    main()
