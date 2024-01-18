import pickle
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from Variables import *

options = webdriver.ChromeOptions();
options.add_experimental_option("detach", True);
driver = webdriver.Chrome(options=options);

# Login Process
driver.get('https://focusonforce.com/login/');
driver.find_element(By.NAME, "fofusername").send_keys(email);
driver.find_element(By.NAME, "fofpassword").send_keys(senha);
driver.find_element(By.NAME, "fofloginsubmit").click();

driver.find_element(By.NAME, "mo2fa_softtoken").send_keys(code);
driver.find_element(By.NAME, "miniorange_otp_token_submit").click();

pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))