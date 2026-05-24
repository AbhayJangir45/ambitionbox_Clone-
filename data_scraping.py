import requests
company_name = []
rating = []
about = []
location = []
review = []
salery = []
jobs = []
industry = []

for i in range (1,500):
    
    header = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0"
    }
    
    resp = requests.get(f"https://www.ambitionbox.com/list-of-companies?campaign=desktop_nav&page={i}", headers = header)
    content = resp.text
    
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(content)
    
    for a in soup.find_all("h2",class_="companyCardWrapper__companyName"):
        company_name.append(a.text.strip())

    for b in soup.find_all("div", class_="rating_star_container"):
        rating.append(b.text.strip())

    for i in soup.find_all("span", class_="companyCardWrapper__interLinking"):
        about.append(i.text.strip())

    for i in soup.find_all("span", class_="companyCardWrapper__interLinking"):
        text = i.text.strip()   # extract string
        parts = text.split("|")
        if len(parts) > 1:
            location.append(parts[1].split("+")[0])
        else:
            location.append("N/A")

    for i in soup.find_all("div", class_="companyCardWrapper__tertiaryInformation"):
        review.append(i.text.split()[0])

    for i in soup.find_all("div", class_="companyCardWrapper__tertiaryInformation"):
        salery.append(i.text.split()[1].split("s")[1])

    for i in soup.find_all("div", class_="companyCardWrapper__tertiaryInformation"):
        jobs.append(i.text.split()[3].split("s")[1].strip())

    for i in soup.find_all("span", class_="companyCardWrapper__interLinking"):
        parts = i.text.split("|")
        if len(parts) > 1:
            industry.append(parts[0].strip())
        else:
            industry.append("N/A")

import pandas as pd
# data = pd.DataFrame({
#     "Company_Names" : company_name,
#     "Location" : location,
#     "Jobs" : jobs,
#     "Salery" : salery,
#     "About" : about,
#     "Review" : review,
#     "Rating" : rating 
# })

r = zip(company_name,location,jobs,salery,about,review,rating)
data = pd.DataFrame(zip(company_name,jobs,salery,location,industry,about,review,rating),
                   columns = ["Company_Names","Jobs","Salery","Location","Industry","About","Review","Rating"])

data.to_csv("all_page_ambition_data.csv", index = False)