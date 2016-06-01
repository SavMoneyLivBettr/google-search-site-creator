# Website creator from Google Searches
# Created by Jacob Skowronek
# Email questions to jacobsskowronek@gmail.com


import requests
from bs4 import BeautifulSoup
from urlparse import urlparse
import datetime

def getSearchResults(query):
    ### Change this to change how many results are displayed ###
    resultsPerPage = 100
    # Replace spaces with + and perform Google search
    query = query.replace(" ", "+")
    url = "https://www.google.com/search?q=" + query + "&num=" + str(resultsPerPage + 1) + "&start=0"
    print(url)
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")
    return soup


def findResults(soup):
    resultsList = []
    # Find all results on page
    results = soup.find_all("div", {"class" : "g"})
    for result in results:
        # Get title
        titleAttr = result.find("h3")
        if titleAttr != None:
            title = titleAttr.text
            print(title)

            # Get description
            descriptionAttr = result.find("div", {"class" : "s"})
            if descriptionAttr != None:
                description = descriptionAttr.text

                # Get website URL
                urlAttr = descriptionAttr.find("cite")
                url = urlAttr.text
                if "http://" not in url and "https://" not in url:
                    url = "http://" + url
                print(url)

                # Get summary
                summaryAttr = descriptionAttr.find("span", {"class" : "st"})
                summary = summaryAttr.text
                print(summary)

                if titleAttr != None and url != None and summary != None:
                    # Get name
                    name = getWebsiteName(url)
                    # Get domain
                    domain = getDomainName(url)
                    # Get image
                    imageSoup = getSearchResults(title.replace(".", " ") + " image")
                    image = getImage(imageSoup)

                    # Append a tuple of the title, url, summary, image, and domain to resultsList
                    resultsList.append((domain, title, url, summary, image))
    return resultsList


def getImage(soup):
    images = soup.find_all("img", src=True)
    #Retrieve the first image
    if images != []:
        searchImage = images[0]["src"]
        if searchImage[0] == "/":
            searchImage = "http://www.google.com" + searchImage
        print(searchImage)

        return searchImage
    else:
        return ""


# name, title, url, summary, image,
def createPage(infoList, templateParts, fileName):
    newFile = open(fileName + ".html", "w")
    # Add header
    newFile.write(templateParts[0])

    for info in infoList:
        # Create body of new HTML page
        newBody = templateParts[1].\
            replace("WEBSITENAME", info[0]).\
            replace("WEBSITETITLE", info[1]).\
            replace("WEBSITEURL", info[2]).\
            replace("WEBSITEDESCRIPTION", info[3]).\
            replace("IMAGESOURCE", info[4]).\
            encode("utf-8")
        newFile.write(newBody)
    # Add footer
    newFile.write(templateParts[2])

    newFile.close()

def  getDomainName(url):
    # Use urlparse to get domain
    parsed_uri = urlparse(url)
    domain = "{uri.scheme}://{uri.netloc}/".format(uri=parsed_uri)
    return domain

def getWebsiteName(url):
    # Get name of site, for example, www.microsoft.com would be microsoft
    try:
        if "www." not in url:
            name = url.split("/")[2].split(".")[0]
        else:
            name = url.split(".")[1]
        return name
    except:
        return ""

def getUserInput():
    # Get user input, and repeat if none is given
    search = raw_input("Please enter what you would like to search: ")
    if search.replace(" ", "") != "":
        return search
    else:
        getUserInput()

def getTemplateParts():
    fileString = ""
    # Open template file and add to fileString
    ### Change me to the path to the template file ###
    templateFilePath = "template.html"
    file = open(templateFilePath, "r")
    fileString += file.read()
    # Split fileString into separate parts
    header = fileString.split("<!--Block-->")[0]
    footer = fileString.split("<!--Block-->")[2]
    block = fileString.split("<!--Block-->")[1]
    # Return parts to be assembled together in a new file at a later time
    return (header, block, footer)

def createFileName(search):
    # Get today's date, then return a filename combining search and today's date
    date = str(datetime.date.today())
    fileName = search + "_" + date
    return fileName

if __name__ == "__main__":
    search = getUserInput()
    searchSoup = getSearchResults(search)

    results = findResults(searchSoup)
    createPage(results, getTemplateParts(), createFileName(search))