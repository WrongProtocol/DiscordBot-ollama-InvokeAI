# Carmine Silano
# Mar 5, 2025
# Connects to our backend calendar to fetch projects and data

import requests
import os
import datetime
import calendar
import base64
from dotenv import load_dotenv

load_dotenv('.env')
# Define the base URL and date range parameters.
BASE_URL = os.getenv('CALENDAR_BASE_URL')
USER = os.getenv('CALENDAR_BASIC_AUTH_USER')
PASS = os.getenv('CALENDAR_BASIC_AUTH_PASS')

# Compute dynamic date range:
today = datetime.date.today()
first_day_current_month = today.replace(day=1)
start_date = first_day_current_month - datetime.timedelta(days=7)
last_day_current_month = today.replace(day=calendar.monthrange(today.year, today.month)[1])
end_date = last_day_current_month + datetime.timedelta(days=7)

# Format dates as YYYY-MM-DD
START_DATE = start_date.isoformat()
END_DATE = end_date.isoformat()

def fetch_projects(filter_type):
    """
    Fetches projects for a given filter (todo, done, or late) from the REST API.
    Returns a list of project dictionaries.
    """
    auth_str = f"{USER}:{PASS}"
    
    b64_auth_bytes = base64.b64encode(auth_str.encode("utf-8"))
    b64_auth_str = b64_auth_bytes.decode("utf-8")
    
    # Set the header with the encoded credentials.
    headers = {
        "Authorization": f"Basic {b64_auth_str}"
    }

    url = f"{BASE_URL}?filter={filter_type}&start={START_DATE}&end={END_DATE}"
    
    response = requests.get(url, headers=headers)

    if response.ok:
        #print("Request succeeded!")
        data = response.json()
        #print(data)
        response.raise_for_status()  # Raise an error if the request failed.
        return response.json()
    else:
        print("Request failed with status code:", response.status_code)
        return {}

def format_project(project, search=None):
    """
    Formats a single project's data into a human-readable string.
    The project title is processed to replace line breaks with a separator.
    """
    project["title"] = project["title"].strip()
    # Check for the search term in the title. If it's not there, bail.
    if search is not None:
        if search.lower() not in project["title"].lower():
            return ""
    
    # Replace newline characters in the title with " | " for clarity.
    formatted_title = project["title"].replace("\n", " | ")

    if project["title"] is None:
        return ""
    
    return (
        #f"ID: {project['id']}\n"
        f"Title: {formatted_title}\n"
        f"Date: {project['start']}\n"
        #f"End: {project['end']}\n"
        f"URL: {project['url']}\n"
    )

def get_projects(search=None):
    projects_to_do_raw = fetch_projects("todo")
    #projects_done_raw = fetch_projects("done")
    projects_late_raw = fetch_projects("late")
    
    projects_to_do = [format_project(p, search) for p in projects_to_do_raw]
    #projects_done = [format_project(p) for p in projects_done_raw]
    projects_late = [format_project(p, search) for p in projects_late_raw]
    
    buffer = []

    buffer.append("** Projects To Do **")
    todo_count = 0
    for project in projects_to_do:
        if project == "":
            continue
        buffer.append(project)
        #buffer.append("-" * 4)
        todo_count += 1
    
    if todo_count == 0:
        buffer.append("None")

    buffer.append("") 
    buffer.append("** Projects Late **")
    late_count = 0
    for project in projects_late:
        if project == "":
            continue
        buffer.append(project)
        #buffer.append("-" * 4)
        late_count += 1
    
    if late_count == 0:
        buffer.append("None! :)")

    return "\n".join(buffer)

if __name__ == "__main__":
    print(get_projects("Danny"))
