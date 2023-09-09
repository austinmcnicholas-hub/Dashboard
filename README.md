# CoachDashboard
Dashboard for Customer Data such as Membership/Renewal/Revenue 

This Python code is a Streamlit web application that performs various tasks related to managing a roster of users with memberships. It primarily uses the Streamlit, Pandas, Altair, and Pyperclip libraries. Let's break down what the code does:

Data Loading: The code begins by loading data from an Excel file named 'Elite.xlsx' using Pandas' read_excel function. It reads a specific sheet named 'Coach Austin' and selects the first 127 rows. The data is stored in a DataFrame called df.

Roster Search: The code provides a user interface for searching the roster. Users can input criteria such as name, username, and email to filter the data. If there are matching records, they are displayed in a dropdown, and the selected username is stored globally.

Membership Analytics: The code offers insights into membership analytics through a sidebar menu. Users can select from options like 'Main Menu', 'Roster Search', 'Buttons', and 'About'. In the 'Main Menu' section, it displays statistics like the total roster count, average coach rating, and monthly revenue, along with a bar chart showing the distribution of membership types.

Buttons and Links: The 'Buttons' section provides clickable buttons with associated actions. These buttons include copying instructions, links, and videos to the clipboard for easy sharing. For example, there are buttons for copying instructions on scheduling, lesson links, surveys, and video links.

About Section: In the 'About' section, the code displays the DataFrame containing the roster data. This section is meant for informational purposes and allows users to view the entire dataset.

Session State: The code uses Streamlit's session_state to store user notes and selected usernames. It ensures that user-specific notes are preserved even when switching between different menu options.

In summary, this Streamlit application provides a user-friendly interface for managing and analyzing a roster of users with different memberships. Users can search for specific members, view analytics, access instructional content, and interact with the roster dataset.
