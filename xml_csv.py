import os
import csv
import requests
from fake_useragent import UserAgent
import xml.etree.ElementTree as ET

ua = UserAgent()
headers = {'User-Agent': ua.random}

# List of XML links
xml_links = [
   "https://www.sec.gov/Archives/edgar/data/0001841356/000184135624000176/primary_doc.xml",
"https://www.sec.gov/Archives/edgar/data/0001841356/000184135624000175/primary_doc.xml",
"https://www.sec.gov/Archives/edgar/data/0001841356/000184135624000174/primary_doc.xml",
"https://www.sec.gov/Archives/edgar/data/0001841356/000184135624000173/primary_doc.xml"
    # Add more links as needed
]

# Create a CSV file for output
csv_file = open("output.csv", "w", newline="")
csv_writer = csv.writer(csv_file)

# Write header row to the CSV file
csv_writer.writerow(["fileName", "federalExemptionsExclusions", "dateOfFirstSale", "descriptionOfOtherType",
                    "minimumInvestmentAccepted", "totalAmountSold", "hasNonAccreditedInvestors", "totalNumberAlreadyInvested"])

# Loop through the XML links and download the XML content
for i, xml_link in enumerate(xml_links, start=1):
    try:
        # Make an HTTP request to the XML link
        response = requests.get(xml_link, headers=headers)

        if response.status_code == 200:
            # Extract the second number from the XML link as the filename
            filename_parts = xml_link.split('/')
            second_number = filename_parts[7]
            filename = f"{second_number}.xml"

            # Save the XML content to a file
            with open(filename, "wb") as xml_file:
                xml_file.write(response.content)

            print(f"Saved {filename}")

            try:
                # Parse the XML content
                tree = ET.parse(filename)
                root = tree.getroot()

                # Extract the desired information
                fileName = filename
                federalExemptionsExclusions = root.find(".//federalExemptionsExclusions/item").text
                dateOfFirstSale = root.find(".//dateOfFirstSale/value").text
                descriptionOfOtherType = root.find(".//typesOfSecuritiesOffered/descriptionOfOtherType").text
                minimumInvestmentAccepted = root.find(".//minimumInvestmentAccepted").text
                totalAmountSold = root.find(".//offeringSalesAmounts/totalAmountSold").text
                hasNonAccreditedInvestors = root.find(".//investors/hasNonAccreditedInvestors").text
                totalNumberAlreadyInvested = root.find(".//investors/totalNumberAlreadyInvested").text
                signatureDate = root.find(".//signatureDate").text

                # Write the extracted data to the CSV file
                csv_writer.writerow([fileName, federalExemptionsExclusions, dateOfFirstSale, descriptionOfOtherType,
                                     minimumInvestmentAccepted, totalAmountSold, hasNonAccreditedInvestors,
                                     totalNumberAlreadyInvested, signatureDate])
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

        else:
            print(f"Failed to fetch data from {xml_link}. Status code: {response.status_code}")

    except Exception as e:
        print(f"Error processing {xml_link}: {str(e)}")

# Close the CSV file
csv_file.close()

print("csv file ready!")

# Delete the downloaded XML files
for filename in os.listdir():
    if filename.endswith(".xml"):
        os.remove(filename)

print("Deleted all downloaded XML files.")