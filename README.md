# CoachDashboard
Dashboard for Customer Data such as Membership/Renewal/Revenue 

This Python script is a Streamlit web application that provides a dashboard for Coach Austin. Let's break down what this code does step by step:

It imports necessary libraries such as Streamlit (streamlit), Pandas (pandas), Altair (altair), Pyperclip (pyperclip), and the datetime module.

It loads data from an Excel file named 'Elite.xlsx' into a Pandas DataFrame (df) using pd.read_excel. The data is read from the sheet named 'Coach Austin' and the first 127 rows (excluding any skipped rows) are loaded into the DataFrame.

It defines a placeholder variable selected_username and profile_picture to store selected user data and profile pictures (not used in the provided code).

It initializes a session state to store user notes using st.session_state.

It defines a function calculate_renewal_date that calculates the renewal date based on various conditions such as membership type, subscription type, and current renewal date.

It defines a function format_date to format dates as 'mm/dd/yyyy'.

It defines a function roster_search to search and display user profiles based on Name, Username, and Email input.

It defines a function create_membership_bar_chart that counts the number of members for each membership type and returns this data for plotting.

The main function is the entry point for the Streamlit app and is executed when the script is run.

It provides a sidebar menu with options: "Main Menu," "Roster Search," "Buttons," and "About."

In the "Main Menu" option, it displays information such as the roster count, monthly revenue, coach rating, upcoming renewals, past renewals, and a bar chart showing the distribution of members by membership type.

In the "Roster Search" option, it allows users to search for profiles based on Name, Username, and Email, and displays selected profile information along with renewal and start dates.

In the "Buttons" option, it provides buttons with various functionalities, including copying instructions, links, and text snippets to the clipboard.

In the "About" option, it displays the loaded DataFrame as a table.

The if __name__ == '__main__': block ensures that the main() function is executed when the script is run directly.

Overall, this code creates a Streamlit web app with a user-friendly interface for Coach Austin to manage user profiles, view important statistics, and access useful resources.
