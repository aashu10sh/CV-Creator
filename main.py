from selenium import webdriver
import os
DRIVER_PATH = "../driver/geckodriver"
import fpdf
import requests

class Teacher():
	def __init__(self,name,position,info,education,experience,photo):
		self.name = name
		self.position = position
		self.info = info
		self.education = education
		self.experience = experience
		self.photo = photo

	def get_image(self)->str:
		print("Getting Image {}".format(self.photo))
		file_data = requests.get(self.photo).content
		# print(file_data)
		file_name = self.photo.split('/')[-1]
		with open(os.path.join(os.getcwd(),'photos',file_name),'wb') as photo_writer:
			photo_writer.write(file_data)
		return file_name

		 
	def get_data(self)->list:
		return [self.name,self.position,self.info,self.education,self.experience,self.photo]
	def print_data(self)->None:
		print(self.name,self.position,self.info,self.education,self.experience,self.photo)
	def out_file(self,)->str:
		pdf = fpdf.FPDF()
		pdf.add_page()
		pdf.set_font('Arial','B',16)
		pdf.text(x=10,y=20,txt=self.name)
		pdf.set_font('Arial','',8)
		pdf.text(x=10,y=25,txt=self.position)
		y_val = 100
		pdf.set_font('Arial','B',10)
		pdf.text(x=10,y=95,txt="My Skills Include")
		pdf.set_font('Arial','',8)
		for info in self.info:
			pdf.text(x=10,y=y_val,txt=info)
			y_val = y_val+5
		pdf.set_font('Arial','B',10)
		pdf.text(x=10,y=120,txt="Education")
		pdf.set_font('Arial','',7)
		pdf.text(x=10,y=125,txt=self.education)

		pdf.set_font('Arial','B',10)
		pdf.text(x=10,y=135,txt="Experience")
		pdf.set_font('Arial','',8)
		pdf.text(x=10,y=140,txt=self.experience)
		img = self.get_image()
		pdf.image(link='',x=10,y=30,w=40,h=40,type='JPG',name='./photos/'+img)

		pdf.output(r"./output/"+self.name+".pdf","F")




class GetInformation():
	def __init__(self,url:str)->None:
		self.url = url

	def driver_run(self):
		driver :selenium.webdriver.firefox.webdriver.WebDriver = webdriver.Firefox(executable_path=DRIVER_PATH)
		# print(type(driver))
		return driver

	def make_pdf(self,teacher:Teacher)->str:
		return teacher.out_file()


	def get_href_links(self)->list:
		link_xpath :str = "/html/body/div[3]/div/div/a"
		individual_links :list = []
		driver = self.driver_run()
		driver.get(self.url)
		links = driver.find_elements_by_xpath(link_xpath)
		for link in links:
			individual_links.append(link.get_attribute('href'))
		driver.close()
		return individual_links

	def write_links(self,links:list):
		self.links = links
		with open(os.path.join(os.getcwd(),'faculty_link.txt'),'w') as writer:
			data:str = "\n".join(links)
			writer.write(data)

	def get_data_for_cv(self):
		for link in self.links:
			driver = self.driver_run()
			driver.get(link)
			name_xpath :str = "/html/body/div[2]/div/div[2]/div/h4"
			position_xpath :str = "/html/body/div[2]/div/div[2]/div/h6[1]"
			info_xpath :str = "/html/body/div[2]/div/div[2]/div/ul[1]/li" #could be multiple
			education_xpath :str = "/html/body/div[3]/div/div[1]/table/tbody/tr[2]/td"
			experience_xpath :str = "/html/body/div[3]/div/div[2]/table/tbody/tr[2]/td"
			photo_xpath :str = "/html/body/div[2]/div/div[1]/img"
			teacher = Teacher(driver.find_element_by_xpath(name_xpath).text,driver.find_element_by_xpath(position_xpath).text,[x.text for x in driver.find_elements_by_xpath(info_xpath)],driver.find_element_by_xpath(education_xpath).text,driver.find_element_by_xpath(experience_xpath).text,driver.find_element_by_xpath(photo_xpath).get_attribute('src'))
			teacher.print_data()
			driver.close()
			self.make_pdf(teacher)
			
			






with open(os.path.join(os.getcwd(),'link.txt'),'r') as link_handler:
	data :str = link_handler.read()
info = GetInformation(data.strip())
info.write_links(info.get_href_links())
info.get_data_for_cv()