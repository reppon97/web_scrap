from bs4 import BeautifulSoup
import requests
import csv
import argparse

parser = argparse.ArgumentParser(description="Paste the URL")
parser.add_argument('action', help='Paste the https://www.roomandboard.com/ product url to get data')
args = parser.parse_args()

url = args.action
page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')

# Product name parse
h1 = soup.find_all('div', {'class': 'constrain'})[0]
head = h1.find_all('span', {'class': 'active'})[0].get_text()
filename = head.replace(" ", "_")
print("Product Name: {}\n".format(head))

# Get Size
try:
    sizes = soup.find_all('div', {'class': 'selector-value-details'})
    for size in sizes:
        print("Size: {}".format(size.get_text()))
except IndexError:
    pass

# Get Specifications
try:
    ul_specs = soup.find_all('ul', {'class': 'fieldset-inner-container'})
    for specs in ul_specs:
        for li in specs.find_all('li'):
            for button in li.find_all('button'):
                title = button['title']
                print("Specs: {}".format(title))
except IndexError:
    pass

# Get Overhang
try:
    s_overhang = soup.find_all('div', {'class': 'selector-value radio-value selected'})[0].get_text()
    print("\nOverhang: {}".format(s_overhang))
    for overhang in soup.find_all('div', {'class': 'selector-value radio-value'}):
        print("Overhang: {}".format(overhang.get_text()))
except IndexError:
    pass

# Get Price
price = soup.find_all('div', {'class': 'summary-price'})[0].get_text()
print("\n{}".format(price))

# Storing into csv file
try:
    with open("{}.csv".format(filename.lower()), 'w', newline='') as new_file:
        blank = None
        write = csv.writer(new_file)
        write.writerow(["Product Name: {}".format(head)])
        write.writerow([blank])
        for specs in ul_specs:
            for li in specs.find_all('li'):
                for button in li.find_all('button'):
                    title = button['title']
                    write.writerow(["Specs: {}".format(title)])
        write.writerow([blank])

        try:
            write.writerow(["Overhang: {}".format(s_overhang)])
            for overhang in soup.find_all('div', {'class': 'selector-value radio-value'}):
                write.writerow(["Overhang: {}".format(overhang.get_text())])
        except NameError or IndexError:
            pass

        write.writerow(["\n{}".format(price)])
except NameError or IndexError:
    pass
