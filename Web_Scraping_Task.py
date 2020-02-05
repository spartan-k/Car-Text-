# -*- coding: utf-8 -*-


import pandas as pd
from selenium import webdriver

review_contents = []
driver_path = '/Users/noah/Downloads/chromedriver'
driver = webdriver.Chrome(executable_path= driver_path)

date = []
userid = []
comment =[]
for page_no in range(1,180):
    driver.get('https://forums.edmunds.com/discussion/2864/general/x/entry-level-luxury-performance-sedans/p'+str(page_no))
    ids = driver.find_elements_by_xpath("//*[contains(@id,'Comment_')]")
    comment_ids = []
    for i in ids:
        comment_ids.append(i.get_attribute('id'))

    for x in comment_ids:
        # Dates Column
        user_date = driver.find_elements_by_xpath('//*[@id="' + x +'"]/div/div[2]/div[2]/span[1]/a/time')[0]
        date.append(user_date.get_attribute('title'))
    
        # User ID Column
        userid_element = driver.find_elements_by_xpath('//*[@id="' + x +'"]/div/div[2]/div[1]/span[1]/a[2]')[0]
        userid.append(userid_element.text)
    
        # User Message Column
        user_message = driver.find_elements_by_xpath('//*[@id="' + x +'"]/div/div[3]/div/div[1]')[0]
        comment.append(user_message.text)

        #Adding date, userid and comment for each user in a dataframe  
        #comments = comments.append
        #comments.loc[len(comments)] = [date,userid,comment]
        #comment_info = pd.DataFrame({"Date": date, "user_id":userid, "comment":comment})
        #comments = comments.append(comment_info)

comments = pd.DataFrame({"Date": date,
                         "user_id":userid,
                         "comment": comment})

#comments.to_csv("/Users/noah/Documents/McGill/Winter Semester/Text Analytics/Assignment 2/test_run/works.csv", index = False)
driver.quit()

comments.to_csv("/Users/noah/Documents/McGill/Winter Semester/Text Analytics/Assignment 2/test_run/works.csv", index = False)