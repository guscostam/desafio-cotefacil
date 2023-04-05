from selenium import webdriver
import json

navegator = webdriver.Chrome()

print(navegator.get('http://quotes.toscrape.com/'))

authors = navegator.find_elements_by_class_name('author')

author_file = {}

for author in authors:
    if author.text == 'J.K. Rowling':
        author_file['name'] = author.text
        about_click = navegator.find_element_by_xpath('/html/body/div/div[2]/div[1]/div[2]/span[2]/a').click()
        author_file['birth_date'] = navegator.find_element_by_class_name('author-born-date').text
        author_file['birth_location'] = navegator.find_element_by_class_name('author-born-location').text
        author_file['description'] = navegator.find_element_by_class_name('author-description').text
        break

home_click = navegator.find_element_by_xpath('/html/body/div/div[1]/div[1]/h1/a').click()

quotes_file = []

while 'Next' in navegator.find_element_by_class_name('pager').text:
    tags_author = []
    text = ''
    for content in navegator.find_elements_by_class_name('quote'):
        if 'J.K. Rowling' in content.text:
            text = content.find_element_by_xpath('/html/body/div/div[2]/div[1]/div[6]/span[1]').text
            tag = str(content.find_element_by_class_name('tags').text)
            tags = tag.replace('Tags:', '')
            tags_author = tags.split()

    data = {
        'text': text,
        'tags': tags_author
    }

    quotes_file.append(data)

    next_page = navegator.find_element_by_css_selector('.next a').click()

final_file = {'author': author_file, 'quotes': quotes_file}
   
with open('dados.json', 'w') as arquivo:
    json.dump(final_file, arquivo)

arquivo.close()
