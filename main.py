
from user_var import TEAMS_LINK
from send_connect import connect_page


try:
    connect_page(TEAMS_LINK)
except:
    print("Something went wrong. (Or your internet was too slow) Try running this again.")
