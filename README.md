This code creates a user-friendly dashboard for managing customer data related to membership, renewal, and revenue. Here's a simplified breakdown:

Importing Libraries: The script imports necessary libraries like Streamlit (for creating the web app), Pandas (for data manipulation), Altair (for data visualization), Pyperclip (for clipboard operations), and the datetime module.

Loading Data: It reads data from an Excel file ('Elite.xlsx') into a Pandas DataFrame ('df'). The data is extracted from the 'Coach Austin' sheet, and the first 127 rows are loaded.

Variables: It defines variables 'selected_username' and 'profile_picture' (not used in this code) to store user data.

Session State: Initializes session state to store user notes using 'st.session_state'.

Date Calculation Function: Defines 'calculate_renewal_date' to compute renewal dates based on membership and subscription types.

Date Formatting Function: Defines 'format_date' to format dates as 'mm/dd/yyyy'.

User Profile Search: Defines 'roster_search' to search and display user profiles based on Name, Username, and Email.

Data Visualization Function: Defines 'create_membership_bar_chart' to count and return the number of members by membership type for charting.

Main Function: This is the entry point for the Streamlit app. It provides a sidebar menu with options for the user.

Menu Options:

"Main Menu": Displays key statistics like roster count, monthly revenue, coach rating, upcoming and past renewals, and a chart showing membership distribution.
"Roster Search": Allows users to search for profiles based on various criteria and displays selected profiles.
"Buttons": Provides buttons for copying instructions, links, and text snippets to the clipboard.
"About": Displays the loaded DataFrame as a table.
Script Execution: The code ensures that the 'main()' function is executed when the script is run directly.
In summary, this code creates a Streamlit web application that serves as a dashboard for Coach Austin to manage customer data, view important metrics, and access useful resources in an organized and user-friendly manner.
