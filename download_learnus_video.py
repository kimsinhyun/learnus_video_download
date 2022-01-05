#!/usr/bin/env python
# coding: utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import subprocess
import os
import sys
from tkinter import *
from tkinter import ttk

if getattr(sys, 'frozen', False):
    chromedriver_path = os.path.join(sys._MEIPASS, 'chromedriver.exe')
    driver = webdriver.Chrome(chromedriver_path)
else:
    driver = webdriver.Chrome('./chromedriver.exe')

def resource_path(relative_path):
    if hasattr(sys._MEIPASS,relative_path):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


# current_path = os.path.abspath('').replace('\\','/')
# options = webdriver.ChromeOptions()
# options.add_argument("--start-minimized")
# driver = webdriver.Chrome(current_path + '/chromedriver.exe',chrome_options=options)
def start_selenium():
    url = "https://www.learnus.org/login.php"
    driver.get(url)
    time.sleep(3)


def login(ID, password):
    input_id = driver.find_element_by_xpath('//*[@id="ssoLoginForm"]/div/div[1]/input[3]')
    input_pw = driver.find_element_by_xpath('//*[@id="ssoLoginForm"]/div/div[1]/input[4]')

    input_id.clear()
    input_pw.clear()

    input_id.send_keys(ID)
    input_pw.send_keys(password)

    login_btn = driver.find_element_by_xpath('//*[@id="ssoLoginForm"]/div/div[2]/input')
    login_btn.click()
    time.sleep(3)



def download_video(page_url, save_file):
    driver.get(page_url)
    time.sleep(3)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    index = soup.select('source')
    m3u8_index = index[0]['src']
    download_process(m3u8_index,save_file)

def download_process(m3u8_index,save_file):
    command =  "ffmpeg -y -i {} -bsf:a aac_adtstoasc -c copy {}".format(m3u8_index, os.path.join(os.getcwd(), save_file + '.mp4'))
    subprocess.call(command, shell=True)




# tkinter 객체 생성
def main(): 

    # print(os.listdir(os.getcwd()))

    window = Tk()

    # 사용자 id와 password를 저장하는 변수 생성
    student_id, password, video_link,save_name = StringVar(), StringVar(), StringVar(), StringVar()

    def start_download():
        start_selenium()
        login(str(student_id.get()), str(password.get()))
        download_video(str(video_link.get()), str(save_name.get()))
        
    # id와 password, 그리고 확인 버튼의 UI를 만드는 부분
    ttk.Label(window, text = "Student_id : ").grid(row = 0, column = 0, padx = 10, pady = 10)
    ttk.Label(window, text = "Password : ").grid(row = 1, column = 0, padx = 10, pady = 10)
    ttk.Label(window, text = "video Link : ").grid(row = 2, column = 0, padx = 10, pady = 10)
    ttk.Label(window, text = "save name : ").grid(row = 3, column = 0, padx = 10, pady = 10)

    ttk.Entry(window, textvariable = student_id).grid(row = 0, column = 1, padx = 10, pady = 10)
    ttk.Entry(window, textvariable = password).grid(row = 1, column = 1, padx = 10, pady = 10)
    ttk.Entry(window, textvariable = video_link).grid(row = 2, column = 1, padx = 10, pady = 10)
    ttk.Entry(window, textvariable = save_name).grid(row = 3, column = 1, padx = 10, pady = 10)

    ttk.Button(window, text = "start download", command = start_download).grid(row = 4, column = 1, padx = 10, pady = 10)
    window.mainloop()


if __name__ == '__main__':
    main()