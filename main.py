import glob
import os
from read_files import readPDF
from read_files import readExcel
import csv


bitcoin_wallet_regex = r'0x[bc1)|[13][a-zA-HJ-NP-Z0-9]{25,39}'
eth_wallet_regex = r'0x[a-fA-F0-9]{40}'
cardano_shelly_wallet_regex = r'\baddr1[a-z0-9]+'
cardano_byron_wallet_regex = r'((DdzFF[1-9A-HJ-NP-Za-km-z]{99})|(Ae[1-9A-HJ-NP-Za-km-z]{57}))'
regex_search = [(bitcoin_wallet_regex,"BTC"),(eth_wallet_regex,"ERC20"),(cardano_byron_wallet_regex,"ADA(LEGACY)"),(cardano_shelly_wallet_regex,"AD")]






directoryPath = os.getcwdb().decode()
pdfFiles =[]
#add pdf files into a list
for name in glob.glob(rf"{directoryPath}\**\*.pdf", recursive = True):
    print(name)
    pdfFiles.append(name)

#now iterate the list of pdf files

pdf_addresses ={}
for file in pdfFiles:
    for regex,title in regex_search:
        file_regex_matches = readPDF(file,title,regex)
        pdf_addresses.update(file_regex_matches)


#now we will iterate over excel files
excelFiles=[]
for name in glob.glob(rf"{directoryPath}\**\*.xlsx", recursive = True):
    print(name)
    excelFiles.append(name)
excel_addresses={}
for file in excelFiles:
    for regex, title in regex_search:
        file_regex_matches = readExcel(file, title, regex)
        excel_addresses.update(file_regex_matches)

# Assume that the dictionary is called "addresses"
with open('addressesPDF.csv', mode='w') as csv_file:
    fieldnames = ['Crypto Wallet Address','Coin Type', 'File It Was Found', 'Page', 'Number of Times Found In Page']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    for key, num_found in pdf_addresses.items():
        if len(key) == 3:
            wallet_address, file_name, num_page = key
        else:
            wallet_address, file_name, num_page, *_ = key
        writer.writerow({
            'Crypto Wallet Address': wallet_address,
            'Coin Type':num_found[0],
            'File It Was Found': file_name,
            'Page': num_page,
            'Number of Times Found In Page': num_found[1]
        })

# Write the dictionary data to a CSV file
with open('addressesEXCEL.csv', mode='w') as csv_file:
    fieldnames = ['Crypto Wallet Address', 'Coin Type','File It Was Found', 'Number of Times Found']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    for key, num_found in excel_addresses.items():
        wallet_address, file_name,coin_type = key
        writer.writerow({
            'Crypto Wallet Address': wallet_address,
            'Coin Type':coin_type,
            'File It Was Found': file_name,
            'Number of Times Found': num_found
        })