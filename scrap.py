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

item_list = []

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

# Get Image URL
image = soup.find_all('div', {'class': 'mediaViewer-viewer'})[0]
for img_url in image.find_all('img'):
    print("\n{}".format(img_url['src']))

# Product Description
product_info = soup.find_all('div', {'class': 'tab-intro'})[0]
for full_desc in product_info.find_all('div', {'class': 'tab-column'}):
    for description in full_desc.find_all('span', {'itemprop': 'description'}):
        print(description.get_text())

# Get Item Number
item_info = soup.find_all('div', {'class': 'tab-column'})[2]
for item_ul in item_info.find_all('ul', {'class': 'material-details-list u-noListStyle u-flushLeft'}):
    for item_li in item_ul:
        item_list.append(item_li)

max_number_li = len(item_list)
print("\n{}".format(item_list[max_number_li-2].get_text()))

# Storing into csv file
try:
    with open("{}.csv".format(filename.lower()), 'w', newline='') as new_file:
        blank = None
        write = csv.writer(new_file)
        write.writerow(["Product Name: {}".format(head)])
        write.writerow([blank])
        write.writerow(["{}\n".format(url)])
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
        write.writerow(["\nImage URL: {}".format(img_url['src'])])
        write.writerow(["\n{}".format(description.get_text())])
        write.writerow(["\n{}".format(item_list[max_number_li-2].get_text())])
except NameError or IndexError:
    pass
