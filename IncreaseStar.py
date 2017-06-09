from selenium import webdriver
import threading
import time
import sqlite3
import requests
import os
# 刷star

github_url = "https://github.com"
github_login_url = "https://github.com/login"


project_url = "you_project_url"

user_name = "//input[@name='user[login]']"
user_email = "//input[@name='user[email]']"
user_password = "//input[@name='user[password]']"
sign_button = "//button[@class='btn btn-primary btn-large f4 btn-block']"




connect = sqlite3.connect("user.db")

def create_table():

    if len(connect.execute("SELECT name FROM sqlite_master where type='table' and name='COMPANY'").fetchall()) == 0:
        connect.execute("""
                            CREATE TABLE COMPANY (id INTEGER PRIMARY KEY NOT NULL ,
                            user_account  TEXT  NOT NULL,
                            user_email  TEXT  NOT NULL,
                            user_password  TEXT  NOT NULL)
                        """)

def close_table():
    connect.close()

def insert_row(user,email,password):
    connect.execute("INSERT INTO COMPANY (user_account,user_email,user_password) VALUES ('{0}','{1}','{2}')".format(user, email,password))
    connect.commit()

def select_table():
    cursor = connect.execute("SELECT user_account,user_email,user_password FROM COMPANY")
    return list(cursor)


def register_account(user,email,passord):
    bower = webdriver.Chrome()
    bower.implicitly_wait(10)
    bower.get(github_url)
    bower.find_element_by_xpath(user_name).send_keys(user)
    bower.find_element_by_xpath(user_email).send_keys(email)
    bower.find_element_by_xpath(user_password).send_keys(passord)
    bower.find_element_by_xpath(sign_button).click()
    print("account:{0}/{1}/{2}".format(user,email,passord))
    # Welcome to GitHub
    isSuccess = True
    if bower.find_element_by_xpath("//div[@class='setup-header setup-org']/h1").text == "Welcome to GitHub":
        insert_row(user,email,passord)
    else:
        isSuccess = False
    bower.quit()
    return isSuccess

def register_account_group(count):
    create_table()
    for index in range(1,count):
        user = "sirramex00{0}".format(index)
        email = "sirramex00{0}@maxsmak.com".format(index)
        pwd = "test123456"
        register_account(user,email,pwd)


def login_github(user,password):
    bower = webdriver.Chrome()
    bower.get(github_login_url)
    bower.implicitly_wait(10)
    bower.find_element_by_xpath("//input[@name='login']").send_keys(user)
    bower.find_element_by_xpath("//input[@name='password']").send_keys(password)
    bower.find_element_by_xpath("//input[@class='btn btn-primary btn-block']").click()

    return bower





def add_project_stars(bower,url):
    bower.get(url)
    time.sleep(5)
    bower.find_element_by_xpath("//button[@aria-label='Star this repository']").click()
    starCount = bower.find_element_by_xpath("//a[@class='social-count js-social-count']").text
    print("Star:{0}".format(starCount))
    return bower






if __name__ == "__main__":
    groupAcc = select_table()
    for acc in groupAcc[5:]:
        bow=login_github(acc[0],acc[2])
        add_project_stars(bow,project_url)
        bow.close()
    pass
