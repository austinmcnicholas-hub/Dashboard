import streamlit as st
import pandas as pd
import altair as alt
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
        st.subheader(f"Profile: {selected_username}")

        # Find the selected user's profile from the DataFrame
        selected_profile = df[df['Username'] == selected_username].iloc[0]

        # Display the profile information
        st.write(f"**Name:** {selected_profile['Name']}")
        st.write(f"**Email:** {selected_profile['Email']}")

        # Display the membership type
        st.write(f"**Membership Type:** {selected_profile['Membership']}")
        
        # Display the sub_type
        st.write(f"**Sub Type:** {selected_profile['Sub_Type']}")

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

def create_membership_bar_chart(df):
    # Count the number of members for each membership type
    membership_counts = df['Membership'].value_counts().reset_index()
    membership_counts.columns = ['Membership Type', 'Number of Members']

    return membership_counts

def main():
    menu = ["Main Menu", "Roster Search", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    selected_membership = st.sidebar.multiselect(
        "Filter by Membership:",
        options=df["Membership"].unique(),
        default=df["Membership"].unique()
    )

    if choice == "Main Menu":
        st.subheader(":baseball: Coach Austin Dashboard")
        st.markdown("##")

        # Filter DataFrame based on selected memberships
        df_selection = df[df["Membership"].isin(selected_membership)]

        # Calculate total_members
        total_members = df_selection.shape[0]

        # Calculate average rating
        average_rating = round(df_selection['Rating'].mean(), 1)

        # Calculate revenue (replace 'Your_Column_Name_Here' with the actual column name)
        revenue = df_selection['Payment_Per_Month'].sum()

        left_column2, left_column1, middle_column, right_column1, right_column2 = st.columns(5)
        with left_column2:
            st.subheader(" Roster Count")
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
        roster_search(df)  # Call the roster_search function


    else:
        st.subheader("About")

        # Display the DataFrame on the "About" page
        st.subheader("DataFrame Display")
        st.dataframe(df)

if __name__ == '__main__':
    main()
