import streamlit as st
import pandas as pd
import altair as alt
import pyperclip
from datetime import datetime

# Load your Excel data 
df = pd.read_excel(
    io='',
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

def calculate_renewal_date(start_date, membership_type, sub_type, renewal):
    if  sub_type == "3 Months":
        # Check if the current renewal date has passed
        today = pd.Timestamp(datetime.today().date())
        #Check if the current legacy renewal date has passed
        if renewal <= today:
            #Calculate the new renewal date as 3 months from today
            return(renewal + pd.DateOffset(months=3)).strftime('%m/%d/%Y')
        else:
            return renewal.strftime('%m/%d/%y')       
        
    elif sub_type == 'Monthly':
        #Check if the current renewl date has passed
        today_monthly = pd.Timestamp(datetime.today().date())
        if renewal <= today_monthly:
            # Calculate the new renewal date as 1 month from today
            return (renewal + pd.DateOffset(months=1)).strftime('%m/%d/%Y')
        else:
            return renewal.strftime('%m/%d/%Y')

    elif membership_type == 'Legacy':
        # Calculate the renewal date as 3 months from the start date
        return (start_date + pd.DateOffset(months=3)).strftime('%m/%d/%Y')  # Format date as mm/dd/yyyy
    
    elif sub_type == 'Annual':
        # Calculate the renewal date as 12 months from the start date (for Annual sub_type)
        return (start_date + pd.DateOffset(years=1)).strftime('%m/%d/%Y')  # Format date as mm/dd/yyyy

    elif membership_type == "Pro":
        # Calculate the renewal date as 1 month from the start date
        return (start_date + pd.DateOffset(months=1)).strftime('%m/%d/%Y') # Format date as mm/dd/yyyy

    elif membership_type == "Elite Academy":
        # Calculate the renewal date as 1 month from the start date (monthly sub type)
        return (start_date + pd.DateOffset(months=1)).strftime('%m/%d/%Y') # Format date as mm/dd/yyyy
    
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
        # Find the selected user's profile from the DataFrame
        selected_profile = df[df['Username'] == selected_username].iloc[0]

        # Determine the color for the "Profile:" name based on the "Active" value
        name_color = "green" if selected_profile['Active'] == 'Yes' else "red"

        # Display the "Profile:" name with the determined color
        st.markdown(f"<h3 style='color:{name_color};'>Profile: {selected_username}</h3>", unsafe_allow_html=True)

        # Display the profile information
        st.write(f"**Name:** {selected_profile['Name']}")

        # Display the membership type
        st.write(f"**Membership Type:** {selected_profile['Membership']}")
        
        # Display the sub_type
        st.write(f"**Sub Type:** {selected_profile['Sub_Type']}")

        st.write(f"**Email:** {selected_profile['Email']}")

        # Additional Markdown sections for selected user's emails
        st.markdown(f"**Guest Email One:** {selected_profile['Guest_Email_One']}")
        st.markdown(f"**Guest Email Two:** {selected_profile['Guest_Email_Two']}")

        selected_start_date = selected_profile['Start_Date']
        selected_sub_type = selected_profile['Sub_Type']
        if not pd.isna(selected_start_date):
            st.subheader("Renewal Date:")
            st.markdown(f"<p style='color:red;text-align:center;font-size:24px;'>🔥 {calculate_renewal_date(selected_start_date, selected_profile['Membership'], selected_sub_type, selected_profile['Renewal'])} 🔥</p>", unsafe_allow_html=True)

        # Display the user's start date as text
        if not pd.isna(selected_start_date):
            st.subheader("Start Date:")
            st.text(format_date(selected_start_date))

        # Allow users to view and edit notes for this profile
        notes_key = f"{selected_username}_notes"
        notes = st.text_area(f"Notes for {selected_username}", st.session_state.user_notes.get(notes_key, selected_profile['Notes']))

        # Update the session state with the user's notes
        st.session_state.user_notes[notes_key] = notes

        # Add a feature to update data
        if st.button("Update Data"):
            # Update the selected user's data with the edited notes
            df.loc[df['Username'] == selected_username, 'Notes'] = notes

            # Save the updated DataFrame to the Excel file
            df.to_excel('', sheet_name='Coach Austin', index=False, engine='openpyxl')

def create_membership_bar_chart(df):
    # Count the number of active members for each membership type
    active_membership_counts = df[df['Active'] == 'Yes']['Membership'].value_counts().reset_index()
    active_membership_counts.columns = ['Membership Type', 'Number of Members']

    return active_membership_counts

def main():
    selected_username = None #Initialize selected_username

    menu = ["Main Menu", "Roster Search", "Buttons", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    selected_membership = st.sidebar.multiselect(
        "Filter by Membership:",
        options=df["Membership"].unique(),
        default=df["Membership"].unique()
    )

    if choice == "Main Menu":
        st.subheader(":baseball: Coach Austin Dashboard")
        st.markdown("##")

        # Filter the DataFrame to include only rows where 'Active' is 'Yes'
        df_main = df[df['Active'] == 'Yes']  # <--- Filter by 'Active' value

        # Filter DataFrame based on selected memberships
        df_selection = df[df["Membership"].isin(selected_membership)]

        # Calculate total_members
        total_members = df_main.shape[0]  # Use shape[0] to get the number of rows

        # Calculate average rating
        average_rating = round(df_selection['Rating'].mean(), 1)

        # Calculate revenue for selected active users
        revenue = df_selection[df_selection['Active'] == 'Yes']['Payment_Per_Month'].sum()

        left_column2, left_column1, middle_column, right_column1, right_column2 = st.columns(5)
        with left_column2:
            st.subheader("Active Roster")
            st.subheader(str(total_members))

        with left_column1:
            st.subheader(" Monthly Revenue")
            st.subheader(revenue)
       
        # Display the 3 most recent upcoming usernames with renewal dates in the right column
        with middle_column:
            st.subheader("New Renewals")
            today = pd.Timestamp(datetime.today().date())  # Convert to Pandas Timestamp
            future_profiles = df_selection[df_selection['Renewal'] > today].sort_values(by='Renewal').head(3)

            if not future_profiles.empty:
                for index, row in future_profiles.iterrows():
                    st.write(f"{row['Username']} - {format_date(row['Renewal'])}")
            else:
                st.write("No upcoming renewals.")

        # Display the most recent renewals that have already passed in right_column2
        with right_column1:
            st.subheader("Past Renewals")
            today_renewals = pd.Timestamp(datetime.today().date())
            past_renewals = df_selection[df_selection['Renewal'] < today_renewals].sort_values(by='Renewal', ascending=False).head(3)  # Sort by Renewal in descending order to get the most recent

            if not past_renewals.empty:
                for index, row in past_renewals.iterrows():
                    st.write(f"{row['Username']} - {format_date(row['Renewal'])}")
            else:
                st.write("No recent renewals.")

        with right_column2:
            st.subheader(" Coach Rating")
            st.write(f"{average_rating}", key="average_rating")


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
            # Find the selected user's profile from the DataFrame
            selected_profile = df[df['Username'] == selected_username].iloc[0]

            # Determine the color for the "Profile:" name based on the "Active" value
            name_color = "green" if selected_profile['Active'] == 'Yes' else "red"

            # Display the "Profile:" name with the determined color
            st.markdown(f"<h3 style='color:{name_color};'>Profile: {selected_username}</h3>",
                        unsafe_allow_html=True)

            # Display the profile information
            st.write(f"**Name:** {selected_profile['Name']}")

            # Display the membership type
            st.write(f"**Membership Type:** {selected_profile['Membership']}")

            # Display the sub_type
            st.write(f"**Sub Type:** {selected_profile['Sub_Type']}")

            st.write(f"**Email:** {selected_profile['Email']}")

            # Additional Markdown sections for selected user's emails
            st.markdown(f"**Guest Email One:** {selected_profile['Guest_Email_One']}")
            st.markdown(f"**Guest Email Two:** {selected_profile['Guest_Email_Two']}")

            selected_start_date = selected_profile['Start_Date']
            selected_sub_type = selected_profile['Sub_Type']
            
            if not pd.isna(selected_start_date):
                    st.subheader("Renewal Date:")
                    st.markdown(
                        f"<p style='color:red;text-align:center;font-size:24px;'>🔥 {calculate_renewal_date(selected_start_date, selected_profile['Membership'], selected_sub_type, selected_profile['Renewal'])} 🔥</p>",
                        unsafe_allow_html=True)

                # Display the user's start date as text
            if not pd.isna(selected_start_date):
                    st.subheader("Start Date:")
                    st.text(format_date(selected_start_date))


            # Wrap the user data editing section inside an expander
            with st.expander("User Notes"):
        
                # Allow users to view and edit notes for this profile
                notes_key = f"{selected_username}_notes"
                notes = st.text_area(f"Notes for {selected_username}",
                                     st.session_state.user_notes.get(notes_key, selected_profile['Notes']))

                # Update the session state with the user's notes
                st.session_state.user_notes[notes_key] = notes


    elif choice == "Buttons":

        if st.button("Slow and Early Load"):
            load = """
https://www.youtube.com/watch?v=NFjoMkBFrB0 
            """
            pyperclip.copy(load)
            st.success("Link Has Been Copied")

        if st.button("Personal Survey"):
            personal_survey = """
https://docs.google.com/forms/
            """
            pyperclip.copy(personal_survey)
            st.success("Survey Has Been Copied")

        

        if st.button("Palm Up"):
            palm = """
https://www.youtube.com/shorts/PHtXbYYqOJ0
            """
            pyperclip.copy(palm)
            st.success("Palm Up Video Has Been Copied")

    

        if st.button("Softball Slow and Early"):
            softball = """
https://www.youtube.com/shorts/JiGaEEKZgbE
            """
            pyperclip.copy(softball)
            st.success("Copied Softball Timing")

       

    else:
        st.subheader("About")

        # Display the DataFrame on the "About" page
        st.subheader("DataFrame Display")
        st.dataframe(df)

if __name__ == '__main__':
    main()
