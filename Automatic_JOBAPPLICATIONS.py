import os
import config_data
from together import Together
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementNotInteractableException



dota2_heroes = [
    "Anti-Mage", "Axe", "Bane", "Bloodseeker", "Crystal Maiden", 
    "Drow Ranger", "Earthshaker", "Juggernaut", "Mirana", "Morphling", 
    "Shadow Fiend", "Phantom Lancer", "Puck", "Pudge", "Razor", 
    "Sand King", "Storm Spirit", "Sven", "Tiny", "Vengeful Spirit", 
    "Windranger", "Zeus", "Kunkka", "Lina", "Lion", "Shadow Shaman", 
    "Slardar", "Tidehunter", "Witch Doctor", "Lifestealer", "Night Stalker",
    "Riki", "Enchantress", "Huskar", "Jakiro", "Omniknight", 
    "Bounty Hunter", "Silencer", "Wraith King", "Death Prophet", 
    "Phantom Assassin", "Pugna", "Templar Assassin", "Viper", "Luna",
    "Dragon Knight", "Dazzle", "Clockwerk", "Leshrac", "Nature's Prophet", 
    "Nyx Assassin", "Visage", "Slark", "Medusa", "Troll Warlord", 
    "Centaur Warrunner", "Magnus", "Timbersaw", "Bristleback", 
    "Tusk", "Skywrath Mage", "Abaddon", "Elder Titan", "Legion Commander",
    "Phoenix", "Terrorblade", "Techies", "Oracle", "Winter Wyvern", 
    "Arc Warden", "Monkey King", "Dark Willow", "Pangolier", "Grimstroke",
    "Hoodwink", "Void Spirit", "Snapfire", "Mars", "Dawnbreaker", 
    "Primal Beast", "Marci", "Muerta"
]


# response = client.chat.completions.create(
#     model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
#     messages=[{
#                 "role": "user",
#                 "content": "hey"
#         }],
#     max_tokens=512,
#     temperature=0.7,
#     top_p=0.7,
#     top_k=50,
#     repetition_penalty=1,
#     stop=["<|eot_id|>","<|eom_id|>"],
#     stream=False
# )
# print(response.choices[0].message.content)

#INITIALIZE DRIVER
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(executable_path="/Users/venkateshwarreddy/Desktop/V/webdrivers/chromedriver", options=chrome_options)



my_data = ["First Name","Last Name","Phone Number","Address","Willing to relocate","resume upload","military or veteran","disability","Email"]
#my_data_dict = {"First Name":"Venkateshwar Reddy", "Last Name":"Darmanola","Phone Number":"4698618663","Address":"13541 Chalet Ave, Frisco","State":"Texas" , "Email":"venkat.re47@gmail.com"}
my_data_str = my_data[0]
for d in my_data:
    my_data_str+=f", {d}"


driver.get("job website link")

total_height = driver.execute_script("return document.body.scrollHeight")
driver.set_window_size(1920, total_height)
time.sleep(5)
driver.get_screenshot_as_file('screenshot.png')
print(1)
wait = WebDriverWait(driver, 10)
html_source = driver.page_source

#find all input fields
input_fields = driver.find_elements(By.TAG_NAME, "input")
ips = []


#find all text input fields
text_inputs = []
for ip in input_fields:
    if ip.get_attribute("type")=="text":
        ips.append(ip.get_attribute("outerHTML"))
        text_inputs.append(ip)
    print(ips)
#print((html_source[:500]))
time.sleep(1)




import google.generativeai as genai
import PIL.Image
GOOGLE_API_KEY="Your google api key"
genai.configure(api_key=GOOGLE_API_KEY)
# for m in genai.list_models():
#   if 'generateContent' in m.supported_generation_methods:
#     print(m.name)


# model = genai.GenerativeModel('gemini-pro')
# response = model.generate_content("What is life to you")
# print(response.text)
    
prompt = "list all the required text inputs in a single line, comma separated, to successfully submit the job application."

img = PIL.Image.open('screenshot.png')
model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content([prompt, img])

required_fields = response.text.split(',')

print(required_fields)

#FILL TRASH DATA
for i in range(len(text_inputs)):
    try:
        text_inputs[i].send_keys(dota2_heroes[i])
    except ElementNotInteractableException:
        print("Element not interactable!")

time.sleep(2)
driver.get_screenshot_as_file('screenshot1.png')
img1 =  PIL.Image.open('screenshot1.png')


hero_responses = []
required_fields_dict ={}
for field in required_fields:
    print(f"field is{field}")
    data = config_data.response_data_mapper(field)
    if  data != None:
        required_fields_dict[field] = data
        prompt = f"what is the text content inside {field}?"
        response = model.generate_content([prompt, img1])
        print("text is ", response.text)
        for i in range(len(dota2_heroes)):
            if dota2_heroes[i] in response.text:
                print("data is",data)
                text_inputs[i].clear()
                text_inputs[i].send_keys(data)
                break
        driver.get_screenshot_as_file(f'screenshot_{field}.png')
    
    #hero_responses.append(response.text)


# for i in range(len(dota2_heroes)):
#     if dota2_heroes[i] in hero_responses:




exit()

#FILLING REQUIRED FIELDS:

c=0
for i in range(len(ips)):
    response = model.generate_content(f"the html content is, {html_source} \n The element {ips[i]} is best related to which one of the following? \n {my_data_str}, None of the above \n answer in one word")
    print(response.text)
    # response = client.chat.completions.create(
    #     model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
    #     messages=[{
    #                 "role": "user",
    #                 "content": f"the html content is, {html_source} \n The element {input_fields[0].get_attribute("outerHTML")} is best related to which one of the following? \n {my_data_str}"

    #         }],
    #     max_tokens=512,
    #     temperature=0.7,
    #     top_p=0.7,
    #     top_k=50,
    #     repetition_penalty=1,
    #     stop=["<|eot_id|>","<|eom_id|>"],
    #     stream=False
    # )
    # print(response.choices[0].message.content)


    if "None" not in response.text:
        for key in my_data_dict.keys():
            print(key)
            if key in response.text:
                print("found")
                input_fields[i].send_keys(my_data_dict[key])
                break

    driver.get_screenshot_as_file(f'fname{i}.png')
    time.sleep(2)


