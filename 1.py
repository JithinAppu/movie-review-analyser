from sklearn.svm import LinearSVC
import matplotlib.pyplot as plt
import numpy as np
import wx
import os
import nltk
import sys
from nltk.corpus import stopwords
from nltk.corpus import sentiwordnet as swn
from nltk.corpus import wordnet as w


state=['Positive','Negative']
path=os.path.dirname(os.path.realpath(sys.argv[0]))
numberOffile=0

class Frame(wx.Frame) :

        def __init__(self,parent,id) :
                wx.Frame.__init__(self,parent,id,'Movie Review Analyser',size=(500,400))
		panel=wx.Panel(self)
		panel.SetBackgroundColour(wx.Colour(230,230,240))
		font = wx.Font(25, wx.DEFAULT, wx.MODERN, wx.FONTWEIGHT_BOLD)
		appname=wx.StaticText(panel, -1, "Movie Review Analyser",(42,50), (360,-1),wx.ALIGN_CENTER)
		appname.SetFont(font)
		#font.SetPointSize(00)
		appname.SetForegroundColour('blue')
		#font.SetPointSize(10)
		font = wx.Font(10, wx.DEFAULT, wx.MODERN, wx.FONTWEIGHT_BOLD)
		button1=wx.Button(panel,label="Training",pos=(90,200),size=(150,75))
		button1.SetBackgroundColour(wx.Colour(230,220,220))
		button1.SetFont(font)
		self.Bind(wx.EVT_BUTTON, self.training_window, button1)
		button2=wx.Button(panel,label="Testing",pos=(250,200),size=(150,75))
		button2.SetBackgroundColour(wx.Colour(230,220,220))
                button2.SetFont(font)
		#font.SetPointSize(15)
		self.Bind(wx.EVT_BUTTON, self.testing_window, button2)
		status_bar=self.CreateStatusBar()
		menubar=wx.MenuBar()
		first=wx.Menu()
		second=wx.Menu()
		first.Append(wx.NewId(),"New Window","This is new window")
		first.Append(wx.NewId(),"Open...","Open new window")
		menubar.Append(first,"File")
		menubar.Append(second,"Edit")
		self.SetMenuBar(menubar)



	def training_window(self,event):
		train_window=create_trainwindow(parent=None,id=-1)
		train_window.Show()
	

	def testing_window(self,event):
                test_window=create_testwindow(parent=None,id=-1)
                test_window.Show()




class create_trainwindow(wx.Frame):
	#global state[]
	global files_list
	global polarity
	global path
	global numberOffile
	#print polarity
	def __init__(self,parent,id):
		self.polarity=''
		self.file_list=[]
		self.path=[]
		self.numberOffile=0
		#state=['True','False']
		wx.Frame.__init__(self,parent,id,'Training',size=(500,600))
               	self.panel=wx.Panel(self)
               	self.panel.SetBackgroundColour(wx.Colour(230,230,240))
               	font = wx.Font(12, wx.DEFAULT, wx.DEFAULT, wx.FONTWEIGHT_NORMAL)
		button3=wx.Button(self.panel,label="Select File",pos=(170,30),size=(150,30))
		button3.SetFont(font)
		self.Bind(wx.EVT_BUTTON, self.show_addfile, button3)
		#fileSelect=wx.TextCtrl(panel,-1,pos=(200,77),size=(250,-1))
		self.select_file=wx.StaticText(self.panel, -3, "Select File",(42,75), (360,-1))
                self.select_file.SetFont(font)
		#self.file_choice=wx.Choice(self.panel,-1,pos=(150,70),size=(250,30))
		#self.file_choice.SetSelection(0)
		self.file_polarity=wx.StaticText(self.panel, -3, "Polarity",(42,150), (360,-1))
                self.file_polarity.SetFont(font)
		self.filePolarity=wx.TextCtrl(self.panel,-1,"",pos=(150,145),size=(250,-1))
		self.filePolarity.SetInsertionPoint(0)
		self.file_choice=wx.Choice(self.panel,-1,pos=(150,70),size=(250,30))
                self.file_choice.SetSelection(0)

		
		button4=wx.Button(self.panel,label="Extract Features",pos=(150,250),size=(200,30))
		button4.SetFont(font)
		self.Bind(wx.EVT_BUTTON,self.extract_feature_ok, button4)
		'''
		self.fileview=wx.TextCtrl(panel,-1,"",pos=(150,51),size=(250,-1))
		self.Bind(wx.EVT_BUTTON, self.file_)
		'''
		button5=wx.Button(self.panel,label="Start Training",pos=(150,350),size=(200,30))
                button5.SetFont(font)
                self.Bind(wx.EVT_BUTTON,self.start_training, button5)
		button6=wx.Button(self.panel,label="Feature Analysis",pos=(150,450),size=(200,30))
                button6.SetFont(font)
		self.Bind(wx.EVT_BUTTON,self.show_feature_analysis, button6)



		

		




	def show_feature_window(self):
		global feature_files
		global numberOffile
		self.number_files=numberOffile-1
		try:
			temp=self.show_features_frame.GetSize()
		except:
			self.feature_filess=[]
			self.temp_files=[]
			#print self.path
			#print self.number_files
			#print self.path[self.number_files]
			'''
			for i in self.path:
				for j in i[1:-1]:
					self.feature_filess.append(feature(j,i[0],i[-1]))
			feature_files=self.feature_filess
			'''
			
			self.temp_files=self.path[self.number_files]
			for j in self.temp_files[1:-1]:
				self.feature_filess.append(feature(j,self.temp_files[0],self.temp_files[-1]))
			feature_files=self.feature_filess
			
			#self.no+=1
			#print feature_files
		try:
			for f in feature_files:
				f.extract_feature()
				f.csv_files()
		except:
			pass
			
			


	def show_addfile(self,event):
		try:
			temp=self.new_file_frame.GetSize()
		except:
			self.new_file_frame=self.select_new_file_window(parent=None,id=1)
			self.new_file_frame.Show()
			self.new_file_frame.Bind(wx.EVT_CLOSE,self.addFile,self.new_file_frame)
	

	def addFile(self,event):
		try:
			global file_list1
			#print file_list1
			if len(file_list1)>=3 and len(file_list1[-1])>0 :
				self.numberOffile+=1
				self.path.append(file_list1)
				self.file_list.append(file_list1[1:-1])
				#print file_list
				self.polarity=file_list1[-1]
				self.filePolarity.SetValue(self.polarity)
				#a=self.file_list[self.filePolarity.GetValue()]
				#print self.file_list[self.filePolarity.GetSelection()]
				#print self.file_list[self.numberOffile-1]
				self.file_choice.SetItems(self.file_list[self.numberOffile-1])
				#self.select_file.SetItems()
				self.file_choice.SetSelection(0)
			self.new_file_frame.Destroy()
		except:
			self.new_file_frame.Destroy()


	def start_training(self,event):
		
		try:
			t = os.listdir(path+'/TrainingFiles')[0]
			#print t
			box=wx.MessageDialog(None,"Training will be continued...!!!???",'Alert',wx.YES_NO)
			ans=box.ShowModal()
			box.Destroy()
			if ans == wx.ID_YES:
				global tr
				tr = TrainTest()
				tr.train()
				box=wx.MessageDialog(None,"Training completed",'Alert',wx.OK)
				ans=box.ShowModal()
        	           	box.Destroy()
		
		except:
			box=wx.MessageDialog(None,"Extract feature first...",'Alert',wx.OK)
                        ans=box.ShowModal()
                        box.Destroy()
		
		'''
		t = os.listdir(path+'/TrainingFiles')[0]
                #print t
                box=wx.MessageDialog(None,"Training will be continued...!!!???",'Alert',wx.YES_NO)
                ans=box.ShowModal()
                box.Destroy()
                if ans == wx.ID_YES:
 	               global tr
                       tr = TrainTest()
                       tr.train()
                       box=wx.MessageDialog(None,"Training completed",'Alert',wx.OK)
                       ans=box.ShowModal()
                       box.Destroy()
		'''
	
	
	
	def show_feature_analysis(self,event):
		try:
			tmp = os.listdir(path+'/TrainingFiles')[0]
			self.features_analysis=feature_analysis_window(parent=None,id=1)
			self.features_analysis.Show()
		
		except:
			box=wx.MessageDialog(None,"Please extract features first.",'Alert',wx.OK)
			answer=box.ShowModal()
			box.Destroy()
		




	class select_new_file_window(wx.Frame):
		new_file=[]
		global numberOffile
		def __init__(self,parent,id):
			#global numberOffile
			wx.Frame.__init__(self,parent,id,'Select File',size=(575,250))
			self.panel=wx.Panel(self)
                	self.panel.SetBackgroundColour(wx.Colour(230,230,240))
                	font = wx.Font(12, wx.DEFAULT, wx.DEFAULT, wx.FONTWEIGHT_NORMAL)
			self.select_file1=wx.StaticText(self.panel, -3, "Select File",(42,50), (360,-1))
            	 	self.select_file1.SetFont(font)
			self.fileSelect1=wx.TextCtrl(self.panel,-1,"",pos=(150,45),size=(250,-1))
			self.fileSelect1.Bind(wx.EVT_BUTTON, self.file_select)
			button5=wx.Button(self.panel,label="Choose",pos=(420,45),size=(150,30))
                	button5.SetFont(font)
                	self.Bind(wx.EVT_BUTTON, self.file_select, button5)
			self.file_polarity1=wx.StaticText(self.panel, -3, "Polarity",(42,150), (360,-1))
                	self.file_polarity1.SetFont(font)
                	self.filePolarity1=wx.TextCtrl(self.panel,-1,"",pos=(150,145),size=(250,-1))
			self.filePolarity1.SetInsertionPoint(0)
			ok_button=wx.Button(self.panel,label="OK",pos=(215,200),size=(150,30))
			ok_button.SetFont(font)
			#self.Bind(wx.EVT_BUTTON,self.filereturn, ok_button)
			self.Bind(wx.EVT_BUTTON,self.polarityreturn, ok_button)




		def file_select(self,event):
			global numberOffile
			self.numberOffile=numberOffile
			filedialog = wx.FileDialog(self, message='Choose File', defaultDir=os.getcwd(),defaultFile='',wildcard='Text Files (*.txt)|*.txt',style=wx.OPEN|wx.CHANGE_DIR|wx.MULTIPLE)
			filedialog.ShowModal()
			filedialog.Destroy()
			name=""
			self.new_file=[]
			#path=filedialog.GetDirectory()
			self.new_file.append(filedialog.GetDirectory())
			for i in range(len(filedialog.GetFilenames())):
				name+=filedialog.GetFilenames()[i]
				name+=","
				#self.numberOffile+=1
				#path+=name
				#print path
				self.new_file.append(filedialog.GetFilenames()[i])
			self.fileSelect1.SetValue(name)
			#print path
			#self.view=open(name,"r").readlines()
			self.numberOffile+=1
			numberOffile=self.numberOffile
			#self.polarity=self.filePolarity.GetValue()
                	#print self.polarity

		
		
		
		def polarityreturn(self,event):
			self.new_file.append(self.filePolarity1.GetValue())
			global file_list1
			file_list1=self.new_file
			#print file_list1
			self.Close()
		
	
		
		'''
		def polarityreturn(self,event):
			global polarity
                        self.newpolarity=self.filePolarity1.GetValue()
                        polarity=self.newpolarity
			self.polarity=polarity
			#self.filePolarity.SetValue(polarity)
			#print polarity
                        self.Close()
		'''

	#def show_feature_window(self):




	


	def extract_feature_ok(self,event):
		
		if self.numberOffile==0:
			box=wx.MessageDialog(None,"Please insert a file",'Alert',wx.OK)
			ans=box.ShowModal()
			box.Destroy()
		else:
			box=wx.MessageDialog(None,"Start feature extraction...!!",'Alert',wx.YES_NO)
                        ans=box.ShowModal()
                        box.Destroy()
			if ans==wx.ID_YES:
				self.show_feature_window()





class feature_analysis_window(wx.Frame) :
	def __init__(self,parent,id):
		self.polarity_list=[]
		self.feature_name_list=[]
		#print "ljljgrjgrgrgjri"
		#print path
		self.draw_graph = DrawGraph()
		#print path
		files=os.listdir(path+"/TrainingFiles/")
		#print files
		for f in files:
			self.polarity_list.append(f[:-4])
		
		feats = open(path+"/TrainingFiles/"+files[0],"r").read().split("\n")[0].split(",")
		self.feature_name_list = feats[1:]
		self.feature_list=[]
		
		for f in files:
			t=[]
			feats = open(path+"/TrainingFiles/"+f,"r").read().split("\n")
			for feat in feats[1:-1]:
				tt=[]
				feat=feat.split(",")
				for ft in feat[1:-1]:
					tt.append(float(ft))
				t.append(tt)
			
			self.feature_list.append(t)
		#print self.polarity_list
		#print self.feature_name_list
		#print self.feature_list
		wx.Frame.__init__(self,parent,id,'Features Analysis',size=(600,600))
		self.panel=wx.Panel(self)
		self.panel.SetBackgroundColour(wx.Colour(230,230,240))
		font = wx.Font(10, wx.DEFAULT, wx.DEFAULT, wx.FONTWEIGHT_NORMAL)
                font.SetPointSize(10)
		font1 = wx.Font(10, wx.DEFAULT, wx.DEFAULT, wx.FONTWEIGHT_NORMAL)
                font1.SetPointSize(12)
		#self.Bind(wx.EVT_CLOSE, self.close_all)
		self.type1=wx.RadioButton(self.panel, -1, 'Polarity VS Feature analysis',pos=(120,20), style=wx.RB_GROUP)
		self.type1.SetFont(font)
		self.type2=wx.RadioButton(self.panel, -1, 'Polarities VS Feature analysis',pos=(120,55))
		self.type2.SetFont(font)
		self.Bind(wx.EVT_RADIOBUTTON, self.draw_new_graph, self.type2)
		self.Bind(wx.EVT_RADIOBUTTON, self.draw_new_graph, self.type1)
		self.polarity_name=wx.StaticText(self.panel,-1,"Polarity\t : ",pos=(50,105))
		self.polarity_name.SetFont(font1)
		self.polarity_choice=wx.Choice(self.panel,-1,pos=(185,105),size=(290,30),choices=self.polarity_list)
		self.polarity_choice.SetSelection(0)
		self.feature_name_text=wx.StaticText(self.panel,-1,"Feature Name\t : ",pos=(50,145))
		self.feature_name_text.SetFont(font1)
		self.feature_choice=wx.Choice(self.panel,-1,pos=(185,145),size=(290,30),choices=self.feature_name_list)
		self.feature_choice.SetSelection(0)
		
		self.Bind(wx.EVT_CHOICE, self.draw_new_graph, self.polarity_choice)
		self.Bind(wx.EVT_CHOICE, self.draw_new_graph, self.feature_choice)
		
		tt = self.feature_list[self.polarity_choice.GetSelection()]
		#print tt
		tt = np.array(tt)
		y_data = tt.T[self.feature_choice.GetSelection()]
		x_data=[]
		t=1
		for i in y_data:
			x_data.append(t)
			t+=1
		#print x_data
		self.draw_graph.draw_single_graph(x_data,y_data,'Files','feature_value',self.feature_name_list[self.feature_choice.GetSelection()])
		
		png = wx.Image(path+"/tempImg.png",wx.BITMAP_TYPE_ANY)
		png = png.Scale(400,300,wx.IMAGE_QUALITY_HIGH)
		png = png.ConvertToBitmap()
		self.graph_img = wx.StaticBitmap(self.panel,-1,png,(100,200),(png.GetWidth(),png.GetHeight()))
		self.graph_img.Bind(wx.EVT_LEFT_DOWN, self.show_graph_photo)
		



	def show_graph_photo(self,event):
		os.system("gnome-open "+path+"/tempImg.png")
	
	def draw_new_graph(self,event):
		if self.type1.GetValue() :
			self.enable_polarity_choices()
			tt = self.feature_list[self.polarity_choice.GetSelection()]
			tt = np.array(tt)
			y_data = tt.T[self.feature_choice.GetSelection()]
			x_data = []
			t = 1
			for i in y_data :
				x_data.append(t)
				t+=1
				
			self.draw_graph.draw_single_graph(x_data,y_data,'Files','feature_value',self.feature_name_list[self.feature_choice.GetSelection()])
			png = wx.Image(path+"/tempImg.png",wx.BITMAP_TYPE_ANY)
                	png = png.Scale(400,300,wx.IMAGE_QUALITY_HIGH)
                	png = png.ConvertToBitmap()
			self.graph_img.SetBitmap(png)
			
		
		elif self.type2.GetValue():
			self.disable_polarity_choices()
			tt = self.feature_list
			tt = np.array(tt)
			y_data = []
			x_data = []
			ttt=1
			#print tt
			for t in tt:
				t = np.array(t)
				y_data.append(float(sum(t.T[self.feature_choice.GetSelection()]))/float(len(t.T[self.polarity_choice.GetSelection()])))
				x_data.append(ttt)
				ttt+=1
			#print y_data
			self.draw_graph.draw_single_graph(x_data,y_data,'Polarity','feature_value',self.feature_name_list[self.feature_choice.GetSelection()])
			png = wx.Image(path+"/tempImg.png",wx.BITMAP_TYPE_ANY)
                        png = png.Scale(400,300,wx.IMAGE_QUALITY_HIGH)
                        png = png.ConvertToBitmap()
                        self.graph_img.SetBitmap(png)
			
			
			
			
			
	def  disable_polarity_choices(self) :
		self.polarity_choice.Disable()
	
	
	
	def enable_polarity_choices(self) :
		self.polarity_choice.Enable()
	
	
	





class create_testwindow(wx.Frame):
	def __init__(self,parent,id) :
               	wx.Frame.__init__(self,parent,id,'Test',size=(600,400))
               	self.panel=wx.Panel(self)
               	self.panel.SetBackgroundColour(wx.Colour(230,230,240))
         	font = wx.Font(10, wx.DEFAULT, wx.DEFAULT, wx.FONTWEIGHT_NORMAL)
		font.SetPointSize(12)
		button_file=wx.Button(self.panel,label="Select File",pos=(433,70),size=(150,30))
                button_file.SetFont(font)
		self.sel_file=wx.StaticText(self.panel, -3, "Select File",(42,75), (360,-1))
                self.sel_file.SetFont(font)
		self.fileSel1=wx.TextCtrl(self.panel,-1,"",pos=(150,72),size=(250,-1))
		self.Bind(wx.EVT_BUTTON, self.show_addonefile, button_file)
		button_test=wx.Button(self.panel,label="Start Test",pos=(170,250),size=(150,30))
                button_test.SetFont(font)
                self.Bind(wx.EVT_BUTTON, self.start_testing, button_test)

		




	def show_addonefile(self,event):
		self.new_file1=[]
		n=''
		filedialog = wx.FileDialog(self, message='Choose a File', defaultDir=os.getcwd(),defaultFile='',wildcard='Text Files (*.txt)|*.txt',style=wx.OPEN|wx.CHANGE_DIR)
                filedialog.ShowModal()
                filedialog.Destroy()
		n+=filedialog.GetDirectory()
		n+=filedialog.GetFilename()
		self.new_file1.append(filedialog.GetDirectory())
		self.new_file1.append(filedialog.GetFilename())
		self.fileSel1.SetValue(self.new_file1[1])


	
	def start_testing(self,event):
		file1=feature(self.new_file1[1],self.new_file1[0],'u')
		file1.extract_feature()
		#print file1.adj_pos_sum
		#print self.new_file1[1]
		self.test_data=[]
		self.test_data.append(float(file1.adj_pos_sum))
		self.test_data.append(float(file1.adj_neg_sum))
		self.test_data.append(float(file1.ad_pos_sum))
		self.test_data.append(float(file1.ad_neg_sum))
		self.test_data.append(float(file1.vr_pos_sum))
		self.test_data.append(float(file1.vr_neg_sum))
		#self.test_data.append(float(file1.nn_pos_sum))
		#self.test_data.append(float(file1.nn_neg_sum))
		#self.test_data.append(float(file1.count_not))
		#self.test_data.append(float(file1.count_good))
		#self.test_data.append(float(file1.count_bad))
		self.test_data.append(float(sum(file1.number_not))/float(len(file1.number_not)))
		self.test_data.append(float(sum(file1.number_good))/float(len(file1.number_good)))
		self.test_data.append(float(sum(file1.number_bad))/float(len(file1.number_bad)))
		#self.test_data.append(float(sum(file1.number_positive))/float(len(file1.number_positive)))
		#self.test_data.append(float(sum(file1.number_negative))/float(len(file1.number_negative)))
		'''global trainn
                trainn = TrainTest()'''

		tr.test(self.test_data)
		box=wx.MessageDialog(None,"The Polarity of the review is '"+tr.cr_polarity+"'.",'Message',wx.OK)
                ans=box.ShowModal()
                box.Destroy()

	
			





class feature():
	def __init__(self,filename1,path1,polarity1):
		self.filename=filename1
		self.pathh=path1
		self.polarityy=polarity1
		self.file1 = open(self.pathh+"/"+self.filename,"r")
		self.data =  self.file1.read().replace("\n"," ").lower()
		self.token = nltk.tokenize.word_tokenize(self.data)
		#print self.token
		#print "\n"


	def extract_feature(self):
		self.featuress=[]
		self.list1=self.token
		#print self.list1
		#Change n't into not
		for i in range(len(self.list1)):
                        if self.list1[i] == "n't":
                                self.list1[i]='not'
                self.featuress=self.list1


		
		#Count Number of NOT in each sentence(Newly added)
                self.list_new=self.list1
                self.number_not=[]
		count_not_sen=0
		index_count_not=0
		#print self.list_new
                for i in range(len(self.list_new)):
                	if self.list_new[i]=="not" or self.list_new[i]=="Not":
				count_not_sen=count_not_sen+1
				#print "if"
			if self.list_new[i]==".":
				#print "else"
				#print self.list_new[i-1]
				self.number_not.append(count_not_sen)
				index_count_not=index_count_not+1
				count_not_sen=0
				#print self.number_not
		#print self.number_not

		
		#Count Number of good in each sentence(Newly added)
                #self.list_new=self.list1
                self.number_good=[]
                count_good_sen=0
                index_count_good=0
                for i in range(len(self.list_new)):
                        if self.list_new[i]=="good" or self.list_new[i]=="Good":
                                count_good_sen=count_good_sen+1
                        if self.list_new[i]==".":
                                self.number_good.append(count_good_sen)
                                index_count_good=index_count_good+1
                                count_good_sen=0
		#print self.number_good


		#Count Number of bad in each sentence(Newly added)
                #self.list_new=self.list1
                self.number_bad=[]
                count_bad_sen=0
                index_count_bad=0
                for i in range(len(self.list_new)):
                        if self.list_new[i]=="bad" or self.list_new[i]=="Bad":
                                count_bad_sen=count_bad_sen+1
                        if self.list_new[i]==".":
                                self.number_bad.append(count_bad_sen)
                                index_count_bad=index_count_bad+1
                                count_bad_sen=0
		#print self.number_bad

					



		'''
		#Change adjectives after not
		remov=[]
                for i in range(len(self.list1)):
                        name_w=''
                        if self.list1[i] == 'not':
                                temp=self.list1[i+1]
                                name_w=temp
                                name_w+='.a.01'
				try:
                                	self.opposit=w.synset(name_w)
                                	self.opposite=self.opposit.lemmas()[0].antonyms()
                                	self.opposite=self.opposite[0].name()
	                        	self.list1[i+1]=self.opposite
                                	remov.append(i)
				except:
					pass
                for j in remov:
                        self.list1.remove(self.list1[j])
                self.featuress=self.list1
		#print self.featuress
		'''

		'''
		#Remove stop words
		self.list2=self.featuress
		for w in self.list2:
			if w in stopwords.words('english'):
				self.list2.remove(w)
		self.featuress=self.list2
		'''		

		#Remove nubers
		self.list3=self.featuress
		for d in self.list3:
                        if d.isdigit() == True:
                                self.list3.remove(d)
		self.featuress=self.list3
		
		#Postagging
		self.list4=self.featuress
		tagged_string=nltk.pos_tag(self.list4)
		self.featuress=tagged_string
		
		#Changing	
		self.list7=self.featuress
		remov1=[]
		for i in range(len(self.list7)):
                        name_w1=''
                        try:
                                if self.list7[i][0] == 'not' or self.list7[i][0] == 'nor' or self.list7[i][0] == 'no':
                                        #self.index=self.list6.index(i)
                                        #self.index+=1
                                        #print self.list6[i+1][1][0]
                                        temp=self.list7[i+1][0]
                                        name_w1=temp
                                        #print temp
                                        if self.list7[i+1][1] == 'JJ' or self.list7[i+1][1] == 'JJR' or self.list7[i+1][1] == 'JJS':
                                                #print self.list6[i+1]
                                                #print "Found"
                                                name_w1+='.a.01'
						try:
							#print "hgfchgehfefgefgefghu"
							self.opposit=w.synset(name_w1)
							self.opposite=self.opposit.lemmas()[0].antonyms()
							#print self.opposite
							if len(self.opposite) > 0 :
								#print len(self.opposite)
								self.opposite=self.opposite[0].name()
								temp1=(self.opposite,self.list7[i+1][1])
								self.list7[i+1]=temp1
								remov1.append(i)
							elif len(self.opposite) == 0 :
								if self.list7[i+2][1] == 'JJ' or self.list7[i+2][1] == 'JJR' or self.list7[i+2][1] == 'JJS':
									temp=self.list7[i+2][0]
                                					name_w1=temp
									#print temp
                                        				name_w1+='.a.01'
                                        				self.opposit=w.synset(name_w)
                                        				self.opposite=self.opposit.lemmas()[0].antonyms()
                                        				self.opposite=self.opposite[0].name()
                                        				temp1=(self.opposite,self.list7[i+2][1])
									#print temp1
                                        				self.list7[i+2]=temp1
                                        				#self.list6[i+1]=self.opposite
                                        				remov1.append(i)
						except:
							pass
					
					elif self.list7[i+2][1] == 'JJ' or self.list7[i+2][1] == 'JJR' or self.list7[i+2][1] == 'JJS':
						try:
							temp=self.list7[i+2][0]
                                			name_w1=temp
							#print self.list6[2][1]
							name_w1+='.a.01'
                                       			self.opposit=w.synset(name_w)
                                       			self.opposite=self.opposit.lemmas()[0].antonyms()
                                       			self.opposite=self.opposite[0].name()
							temp1=(self.opposite,self.list7[i+2][1])
							self.list7[i+2]=temp1
                                       			#self.list6[i+1]=self.opposite
                                    			remov1.append(i)
						except:
							pass

			except:
				pass
		self.featuress=self.list7			

		
		#Word counting
		self.list5=self.featuress
		remov=[]
		stem = nltk.stem.porter.PorterStemmer()
		for c in range(len(self.list5)):
			try:
				self.list5[c]=stem.stem(self.list5[c])
			except:
				remov.append(c)
				continue
		selected_words=[]
		for i in range(len(self.list5)):
			label=False

			for j in range(len(selected_words)):
				if selected_words[j][1]==self.list5[i]:
					label=True
					break

			if label:
				selected_words[j][0]+=1
				continue

			else:
				selected_words.append([1,self.list5[i]])
			
		self.featuress=selected_words
		
		#Find polarity value
		self.list6=self.featuress
		value_temp_pos=[]
		value_temp_neg=[]
		pos=0
		neg=0
		for i in range(len(self.list6)):
			name_word=self.list6[i][1][0]
			try:
				if self.list6[i][1][1] == 'JJ' or self.list6[i][1][1] == 'JJR' or self.list6[i][1][1] == 'JJS':
					sense=01
					try:
						name_word+='.a.0'
						name1=name_word
						while True:
							#print sense
							name_word+=str(sense)
							#print name_word
							value=swn.senti_synset(name_word)
							#print value.pos_score()
							value_pos=value.pos_score()
							#print value_pos
         		                               	value_neg=value.neg_score()
							value_temp_pos.append(value_pos)
							value_temp_neg.append(value_neg)
							#print value_temp_pos
							sense+=1
							name_word=name1
						#print value_temp_pos
					except:
						for val1 in value_temp_pos:
							pos+=val1
						for val2 in value_temp_neg:
							neg+=val2
						pos/=(sense-1)
						neg/=(sense-1)
						value_temp_pos=[]
                                                value_temp_neg=[]
			

					self.list6[i].append(pos)
					self.list6[i].append(neg)
				elif self.list6[i][1][1] == 'RB' or self.list6[i][1][1] == 'RBR' or self.list6[i][1][1] == 'RBS':
					sense=01
                                        try:
                                                name_word+='.r.0'
                                                name1=name_word
                                                while True:
                                                        name_word+=str(sense)
                                                        value=swn.senti_synset(name_word)
                                                        value_pos=value.pos_score()
                                                        value_neg=value.neg_score()
                                                        value_temp_pos.append(value_pos)
                                                        value_temp_neg.append(value_neg)
                                                        sense+=1
                                                        name_word=name1
                                        except:
                                                for val1 in value_temp_pos:
                                                        pos+=val1
                                                for val2 in value_temp_neg:
                                                        neg+=val2
                                                pos/=(sense-1)
                                                neg/=(sense-1)
						value_temp_pos=[]
						value_temp_neg=[]
					self.list6[i].append(pos)
                                	self.list6[i].append(neg)
				elif self.list6[i][1][1] == 'NN' or self.list6[i][1][1] == 'NNS' or self.list6[i][1][1] == 'NNP' or self.list6[i][1][1] == 'NNPS':
					sense=01
                                        try:
                                                name_word+='.n.0'
                                                name1=name_word
                                                while True:
                                                        name_word+=str(sense)
                                                        value=swn.senti_synset(name_word)
                                                        value_pos=value.pos_score()
                                                        value_neg=value.neg_score()
                                                        value_temp_pos.append(value_pos)
                                                        value_temp_neg.append(value_neg)
                                                        sense+=1
                                                        name_word=name1
                                        except:
                                                for val1 in value_temp_pos:
                                                        pos+=val1
                                                for val2 in value_temp_neg:
                                                        neg+=val2
                                                pos/=(sense-1)
                                                neg/=(sense-1)
                                                value_temp_pos=[]
                                                value_temp_neg=[]

					self.list6[i].append(pos)
                                	self.list6[i].append(neg)
				elif self.list6[i][1][1] == 'VB' or self.list6[i][1][1] == 'VBD' or self.list6[i][1][1] == 'VBG' or self.list6[i][1][1] == 'VBN' or self.list6[i][1][1] == 'VBP' or self.list6[i][1][1] == 'VBZ':
                                        sense=01
                                        try:
                                                name_word+='.v.0'
                                                name1=name_word
                                                while True:
                                                        name_word+=str(sense)
                                                        value=swn.senti_synset(name_word)
                                                        value_pos=value.pos_score()
                                                        value_neg=value.neg_score()
                                                        value_temp_pos.append(value_pos)
                                                        value_temp_neg.append(value_neg)
                                                        sense+=1
                                                        name_word=name1
                                        except:
                                                for val1 in value_temp_pos:
                                                        pos+=val1
                                                for val2 in value_temp_neg:
                                                        neg+=val2
                                                pos/=(sense-1)
                                                neg/=(sense-1)
                                                value_temp_pos=[]
                                                value_temp_neg=[]
                                        self.list6[i].append(pos)
                                        self.list6[i].append(neg)

			except:
				pos=0
                		neg=0
				self.list6[i].append(pos)
                                self.list6[i].append(neg)
		self.featuress=self.list6

		
		#saving features in to file Feature
		try:
			os.mkdir(path+"/Features/"+"/"+self.polarityy+"/")
		except:
			pass
		try:
			self.file_feature = open(path+"/Features/"+self.polarityy+"/"+self.filename,"a+")
		except:
			pass
		for k in self.featuress:
			self.file_feature.write(str(k))
			self.file_feature.write("\n")
		

		'''
		#Count Number of positive and negative in each 100 tokens(Newly added)
                #self.list_new=self.list1
		self.list8=self.featuress
                self.number_positive=[]
		self.number_negative=[]
                count_positive_sen=0
		count_negative_sen=0
                index_count=0
		#index_count_negative=0
                for i in range(len(self.list8)):
			print self.list8[i][1][0]
			try:
                        	if self.list8[i][2] > self.list8[i][3]:
                                	count_positive_sen=count_positive_sen+self.list8[i][0]
					#print self.list8[i][2]
					#print count_positive_sen
				if self.list8[i][2] < self.list8[i][3]:
                        	        count_negative_sen=count_negative_sen+self.list8[i][0]
				index_count=index_count+1
	
				if index_count==100  or i==len(self.data)-1 :
					#print count_positive_sen
					self.number_positive.append(count_positive_sen)
                        	        #index_count_positive=index_count_positive+1
                               	 	count_positive_sen=0
					self.number_negative.append(count_negative_sen)
                         	       	index_count=0
                         	       	count_negative_sen=0
			except:
				#print self.list8[i][1][0]
				continue
		#print "Positive"
                #print self.number_positive
		#print self.number_negative
		'''
		#print "fggf"
		#Count Positive & Negative Adjecives
		self.list8=self.featuress
		self.adj_pos_sum=0
		self.adj_neg_sum=0
		for i in range(len(self.list8)):
			try:
				if self.list8[i][1][1]=='JJ' or self.list8[i][1][1]=='JJS' or self.list8[i][1][1]=='JJS':
					self.adj_pos_sum+=(self.list8[i][0]*self.list8[i][2])
					self.adj_neg_sum+=(self.list8[i][0]*self.list8[i][3])
					
			except:
				pass
		#Count Positive & Negative Adverbs
		self.ad_pos_sum=0
		self.ad_neg_sum=0
		for i in range(len(self.list8)):
                        try:
				if self.list8[i][1][1] == 'RB' or self.list8[i][1][1] == 'RBR' or self.list8[i][1][1] == 'RBS':
					self.ad_pos_sum+=(self.list8[i][0]*self.list8[i][2])
					self.ad_neg_sum+=(self.list8[i][0]*self.list8[i][3])
			except:
				pass
		#Count Positive & Negative verbs
		self.vr_pos_sum=0
		self.vr_neg_sum=0
		for i in range(len(self.list8)):
                        try:
				if self.list8[i][1][1] == 'VB' or self.list8[i][1][1] == 'VBD' or self.list8[i][1][1] == 'VBG' or self.list8[i][1][1] == 'VBN' or self.list8[i][1][1] == 'VBP' or self.list8[i][1][1] == 'VBZ':
					self.vr_pos_sum+=(self.list8[i][0]*self.list8[i][2])
                                        self.vr_neg_sum+=(self.list8[i][0]*self.list8[i][3])
			except:
				pass
		
		'''
		#Count Positive & Negative nouns
		self.nn_pos_sum=0
		self.nn_neg_sum=0
		for i in range(len(self.list8)):
			try:
				if self.list8[i][1][1] == 'NN' or self.list8[i][1][1] == 'NNS' or self.list8[i][1][1] == 'NNP' or self.list8[i][1][1] == 'NNPS':
					self.nn_pos_sum+=(self.list8[i][0]*self.list8[i][2])
                                        self.nn_neg_sum+=(self.list8[i][0]*self.list8[i][3])
			except:
				pass
		'''
		'''
		#Count number of NOT
		self.count_not=0
		for i in range(len(self.list8)):
			if self.list8[i][1][0] == 'not':
				self.count_not+=self.list8[i][0]
		'''

		'''
		#Count number of GOOD
		self.count_good=0
		for i in range(len(self.list8)):
			if self.list8[i][1][0] == 'good':
				self.count_good+=self.list8[i][0]


		#Count number of BAD
                self.count_bad=0
                for i in range(len(self.list8)):
                        if self.list8[i][1][0] == 'bad':
                                self.count_bad+=self.list8[i][0]
		'''

			
		
		
	

	def csv_files(self):
		global path
		try:
			os.mkdir(path+"/TrainingFiles")
		except:
			pass
		try:
			file1=open(path+"/TrainingFiles/"+self.polarityy+".csv","r")
		except:
			file1=open(path+"/TrainingFiles/"+self.polarityy+".csv","a+")
			t = ","
			t += "Value of Positive Adjectives,"
			t += "Value of Negative Adjectives,"
			t += "Value of Positive Adverbs,"
			t += "Value of Negative Adverbs,"
			t += "Value of Positive Verbs,"
			t += "Value of Negative Verbs,"
			#t += "Value of Positive Nouns,"
			#t += "Value of Negative Nouns,"
			#t += "Count of NOT\n"
			#t += "Count of GOOD,"
			#t += "Count of BAD\n" 
			t += "Value of average Not,"
			t += "Value of average good," 
			t += "Value of average bad\n"
			#t += "Value of average positive per sentences,"
			#t += "Value of average negative per sentences\n"
			file1.write(t)
			file1.close()
		file1=open(path+"/TrainingFiles/"+self.polarityy+".csv","a+")
		t = self.filename
		t += ","
		t += str(self.adj_pos_sum)+","
		t += str(self.adj_neg_sum)+","
		t += str(self.ad_pos_sum)+","
		t += str(self.ad_neg_sum)+","
		t += str(self.vr_pos_sum)+","
		t += str(self.vr_neg_sum)+","
		#t += str(self.nn_pos_sum)+","
		#t += str(self.nn_neg_sum)+","
		#t += str(self.count_not)+","
		#t += str(self.count_good)+","
		#t += str(self.count_bad)+","
		t += str(float(sum(self.number_not))/float(len(self.number_not)))+","
		t += str(float(sum(self.number_good))/float(len(self.number_good)))+","
		t += str(float(sum(self.number_bad))/float(len(self.number_bad)))+","
		#t += str(float(sum(self.number_positive))/float(len(self.number_positive)))+","
		#t += str(float(sum(self.number_negative))/float(len(self.number_negative)))+","
		t += "\n"
		#print t
		file1.write(t)
		file1.close()



class DrawGraph() :
	def __init__(self) :
		pass

	def draw_single_graph(self,x_data,y_data,x_label,y_label,title) :
		try:
			plt.close()
		except:
			pass
		fig = plt.figure()
		axis = fig.add_subplot(111)
		axis.set_title(title)
		axis.set_xlabel(x_label)
		axis.set_ylabel(y_label)
		axis.grid(True)
		plt.xticks(x_data)
		plt.plot(x_data,y_data,marker='*',c = 'red')
		plt.savefig(path+'/tempImg.png')

	'''
	def save_graphs(self,graph_data) :
		if graph_data[0]:
			pp=PdfPages(graph_data[1]+'.pdf')
			for data in graph_data[2]:
				try:
					plt.close()
				except:
					pass
				
				fig = plt.figure()
                		axis = fig.add_subplot(111)
                		axis.set_title(title)
                		axis.set_xlabel(x_label)
                		axis.set_ylabel(y_label)
                		axis.grid(True)
                		plt.xticks(x_data)
                		plt.plot(x_data,y_data,marker='*',c = 'red')
                		plt.savefig(path+'/temp_img.png')
	'''





class TrainTest() :
	def __init__(self) :
		self.polarityyy=[]
		self.n=0
		self.y=[]
		self.p1=[]
		self.files = os.listdir(path+"/TrainingFiles")
		#print self.files
		''' 
		for i in self.files:
			self.polarityyy.append(i[:4])
			print self.polarityyy
		'''
		#self.p=['Positive','Negative']
		self.data=[]
		for i in self.files :
			self.p1.append(i[:-4])
			#print self.p1
			text1=open(path+"/TrainingFiles/"+i,"r").read().split("\n")
			#print text1[0]
			for j in text1[1:-1]:
				#print j
				trainn = []
				self.y.append(self.n)
				for k in j.split(",")[1:-1]:
					#print k
					trainn.append(float(k))
				self.data.append(trainn)
			self.n+=1
		#print self.data
		#print''' 


	def train(self):
		#print self.data
		#print self.y
		self.clfr = LinearSVC()
		self.clfr.fit(self.data,self.y)
		#print self.p1[clfr.predict(self.train_data[0])[0]]
	def test(self,test_data):
		#self.clfr = LinearSVC()
		#print self.p1
		self.cr_polarity=self.p1[self.clfr.predict(test_data)[0]]
				
		
		
		





if __name__=='__main__' :
        app=wx.PySimpleApp()
        frame=Frame(parent=None,id=-1)
        frame.Show()
	app.MainLoop()

