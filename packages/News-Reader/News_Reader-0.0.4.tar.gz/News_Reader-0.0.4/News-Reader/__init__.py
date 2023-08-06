"""
INDIAN NEWS READER
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This Is Program Called Indian News Resder Which IS Capable For
Showing And Reading Top 10(Default) Headlines - made by parth
"""
# -------------------------MODULES REQUIRED----------------------
from random import choice
import requests
from win32com.client import Dispatch
# Copyright (C) VPM Applications. All rights reserved.
# -------------PROGRAM BASE CLASS-----------------------
class IndianNewsReader:
    """
    This A Base Class For Our Program
    paran : User_name,page_size,
    credits - made by parth
    """
    def __init__(self=None,User_name="Stranger",page_size=10):
        self.name = User_name
        self.page_size = page_size

    des = f"This Is A Indian News reader Program Devloped By YourNameHere\n*Our FEATURES*\nFirstly,We Use Simple English\n2nd We Provide Top Headlines Sort By Your Choice\n3rd. Headlines are Bought From Popular Resources Like :- Time Of India,BBc News etc.\nWe Provide Many Options To Search Like by Keywords,By Category('Science,Technology' etc) and How Many Top Headlines You want To See (DEfault:- Top - 10) and many more....."
    __apikey = "XXXXXXXXXXXXXXX" #Your API KEY HERE
    __apiendpoint = " https://newsapi.org/v2/top-headlines?"
    def speak(self=None,string="You have Not Passed Any String Please Pass It!"):
        """
        This Function Which Helps In Txt to Speech conversion
        params : String
        return : None
        """
        speak = Dispatch("SAPI.SpVoice")
        speak.Speak(string)
    def Greet(self=None):
        """
        This Function Helps In Greeting User
        param:None
        return:None
        """
        print(f"Hi,{self.name} 😊")
        self.speak(f"Hi,{self.name}")
        print("Nice To Meet You")
        self.speak("Nice To Meet You")
    def Greet_No(self=None):
        """
        This Function Helps In Greeting User(☺,Which Can Be A Number (I Know It Is Stupid(But Dont Judge Me)))
        param:None
        return:None
        """
        ListOfPreetify = ["A Nice Number","A Beautifull Number","Yes! My favourite Number","Truly,I Like This Number"]
        chaplusi = choice(ListOfPreetify)
        print(f"Hi,{self.name} 😊")
        self.speak(f"Hi,{self.name}")
        print(f"{chaplusi}")
        self.speak(f"{chaplusi}")
    def LatestIndianNews(self = None):
        """
        This Function Helps In Giving Latest 
        and Top 10(default) News Headlines and its descriptions
        params:None
        return:None
        """
        params = {
            "country":"in",
            "apiKey" : self.__apikey,
            "pagesize" : self.page_size,
        }
        jdata = requests.get(self.__apiendpoint,params=params)
        final_data = jdata.json()
        article_list = final_data['articles']
        index = 0
        for article in article_list:
            index= index + 1
            print(f"[{index}]")
            self.speak(f"News {index}")
            source = article["source"]["name"]
            title  = article["title"]
            description  = article["description"]
            url =  article["url"]
            author = article["author"]
            publishtime = article["publishedAt"]
            print(f'''\t======{title}======\n
            {description}\n
            \t\t\t\t To Read Full Article Click Here:- {url}
            \t\t\t\t Source - {source}
            \t\t\t\t Author - {author}
            \t\t\t\t Published At - {publishtime}''')
            self.speak(f"{title}\n{description}\nAuthor - {author}")


    def SearchByKEywords(self = None):
        """
        This Function Helps To Show News Headlines According To The User-Given Keywords
        params:None
        return:None
        """
        while(True):
            try:
                print("😊 - Words From ' Indian News Reader' ")
                self.speak("In The Coming Input Statement You Have To Type Your Keywords or a Phrase And Also Take Care To Seperate Then By Commas")
                userkeywords = input("Type Your Keywords Here(seperated By Commas):- ").strip()
                
                break
            except Exception as e:
                print("An Error Occured Check Your Input")
                self.speak("An Error Occured Check Your Input")
                continue
        params =  {
            "country":"in",
            "apiKey" : self.__apikey,
            "pagesize" : self.page_size,
            "q": userkeywords
        }
        jdata = requests.get(self.__apiendpoint,params=params)
        final_data = jdata.json()
        article_list = final_data['articles']
        index = 0
        for article in article_list:
            index= index + 1
            print(f"[{index}]")
            self.speak(f"News {index}")
            source = article["source"]["name"]
            title  = article["title"]
            description  = article["description"]
            url =  article["url"]
            author = article["author"]
            publishtime = article["publishedAt"]
            print(f'''\t======{title}======\n
            {description}\n
            \t\t\t\t To Read Full Article Click Here:- {url}
            \t\t\t\t Source - {source}
            \t\t\t\t Author - {author}
            \t\t\t\t Published At - {publishtime}''')
            self.speak(f"{title}\n{description}\nAuthor - {author}")
        
        print(f"These Are The Top {index} Headlines Related To {userkeywords}")
        self.speak(f"These Are The Top {index} Headlines Related To {userkeywords}")
                    
        if index==0:
            print("404 News Not Found")
            self.speak("4 0 4 News Not Found!")
        
    def SearchByCatergory(self = None):
        """
        This Function Helps In To Show Headlines
        According To The User-Choosen Category
        params : None
        return : None
        """
        ListOfCategory = ["business","entertainment","general","health","science","sports","technology"]
        print('''Please Choose From The Bellow Options:- \n''')
        self.speak("Please Choose From The Bellow Options")
        index = 0
        for category in ListOfCategory:
            index = index + 1
            print(f"*{category}\n")
            self.speak(f"Category No. {index} {category}")
        print("😊 - Words From ' Indian News Reader' ")
        self.speak("In The Coming Input Statement You Have To Type Only From The Given Category")
        print("Pro Tip:- \"Dont Worry About Cases , Just Worry About Spaces\" - Indian News Reader")
        while(True):
            try:
                user_choosen_category = input("Type Which Category You Want To Choose:- ").lower().strip()
                if user_choosen_category in ListOfCategory:
                    params =  {
                    "country":"in",
                    "apiKey" : self.__apikey,
                    "pagesize" : self.page_size,
                    "category": user_choosen_category}
                    jdata = requests.get(self.__apiendpoint,params=params)
                    final_data = jdata.json()
                    article_list = final_data['articles']
                    index = 0
                    for article in article_list:
                        index= index + 1
                        print(f"[{index}]")
                        self.speak(f"News {index}")
                        source = article["source"]["name"]
                        title  = article["title"]
                        description  = article["description"]
                        url =  article["url"]
                        author = article["author"]
                        publishtime = article["publishedAt"]
                        print(f'''\t======{title}======\n
                        {description}\n
                        \t\t\t\t To Read Full Article Click Here:- {url}
                        \t\t\t\t Source - {source}
                        \t\t\t\t Author - {author}
                        \t\t\t\t Published At - {publishtime}''')
                        self.speak(f"{title}\n{description}\nAuthor - {author}")
                    if index==10:
                        print(f"These Are The Top {self.page_size} Headlines Related To {user_choosen_category} Category")
                        self.speak(f"These Are The Top {self.page_size} Headlines Related To {user_choosen_category} Category")
                        break
                    if index==0:
                        print("404 News Not Found")
                        self.speak("4 0 4 News Not Found!")
                else:
                    print("Please Type An Input Which Is Present In Options!")
                    self.speak("Please Type An Input Which Is Present In Options")
                    continue
                    
            except Exception as e:
                print("An Error Occured Check Your Input")
                self.speak("An Error Occured Check Your Input")
                continue
        
        
    def SearchByChannel(self = None):
        """
        This Function Helps In To Show Headlines
        According To The User-Specified Channel
        params : None
        return : None
        """
        print("😊 - Words From ' Indian News Reader' ")
        self.speak("In The Coming Input Statement You Have To Type The Name Of The Sources Which Means Channel's Name Seperated By Commas")
        print("Pro Tip:- \"Dont Worry About Cases , Just Worry About Spaces\" - Indian News Reader")
        while(True):
            try:
                user_specified_channel = input("Type From Which Channel/s You Want News(NOTE:SEPERATE BY COMMAS) (example:- bbc-news) :-  ").lower().strip()
                params =  {
                "apiKey" : self.__apikey,
                "pagesize" : self.page_size,
                "sources" : user_specified_channel}
                jdata = requests.get(self.__apiendpoint,params=params)
                final_data = jdata.json()
                article_list = final_data['articles']
                index = 0
                for article in article_list:
                        index= index + 1
                        print(f"[{index}]")
                        self.speak(f"News {index}")
                        source = article["source"]["name"]
                        title  = article["title"]
                        description  = article["description"]
                        url =  article["url"]
                        author = article["author"]
                        publishtime = article["publishedAt"]
                        print(f'''\t======{title}======\n
                        {description}\n
                        \t\t\t\t To Read Full Article Click Here:- {url}
                        \t\t\t\t Source - {source}
                        \t\t\t\t Author - {author}
                        \t\t\t\t Published At - {publishtime}''')
                        self.speak(f"{title}\n{description}\nAuthor - {author}")
                if index==10:
                        print(f"These Are The Top {index} Headlines From {user_specified_channel}")
                        self.speak(f"These Are The Top {index} Headlines From {user_specified_channel}")
                        break
                if index==0:
                        print("404 News Channel Not Found")
                        self.speak("4 0 4 News Not Found!")
                else:
                    print("Please Type An Input Which Is Present In Options!")
                    self.speak("Please Type An Input Which Is Present In Options")
                    continue
                    
            except Exception as e:
                print("An Error Occured Check Your Input")
                self.speak("An Error Occured Check Your Input")
                continue
if __name__=="__main__":
    # '''NOTE : ----| This | Is | A | Test | Code | Please Refer (main) For The MAin Program---- '''
    try:
        print("============WELCOME TO INDIAN NEWS READER============")
        name = input("Please Enter Your Name To Proceed:- ")
        if name=="":
            app = IndianNewsReader()
        else:
            app = IndianNewsReader(name)
        if name.isdigit():
            app.Greet_No()
        else:
            app.Greet()
        print('''
        Hi! This Is ZuuDuKo🤗🤗🤗🤗🤗🤗 , Your News Reader  ( And A Pure Indian😁)\n
        1. About Us 
        2. Get Started
        Press q to exit.
        ''')
        app.speak("Hi Once Again! This Is Zuduko ,Your News Reader! Press 1 To Know About Us Or Press 2 To Get Started Or Press q To Exit")
        while(True):
            try:
                userinput = input("Enter Your Input Here:- ").lower()
                if userinput=="1":
                    print(app.des)
                    app.speak(app.des)
                    break
                elif userinput=="2":
                    print('''\t\t\t1. Set No Of Headlines To Show
                    2. View News By Catergory(Various Options Available)
                    3. View News Related To Your Specified Keywords
                    4. View News From A Specific Channel
                    5. View Simple Top News Headlines (default-10)
                    or enter q to exit(Please Read it! Yourself)''')
                    app.speak("In The Coming Input Statement Type 1 to Set No. of headlines , 2 To view News By Catergory Where Various Options are Available , 3 To To View News Related To Your Specified Keywords  ,  4 To View News From A Specific Channel , 5 To View Simple Top News Headlines")
                    while True:
                        userinput1 = input("Enter your Input Here :- ")
                        if userinput1=="1":
                            while True:
                                try:
                                    no_of_headlines = int(input("Set No Of Headlines To Show:- "))
                                    app.page_size = no_of_headlines
                                    print("Data Changed!")
                                    app.speak("Data Changed!")
                                    break
                                except ValueError as e:
                                    print("Please Give An Integer As A Value!")
                                    app.speak("Please Give An Integer As A Value!")
                        elif userinput1=="2":
                            app.SearchByCatergory()
                        elif userinput1=="3":
                            app.SearchByKEywords()
                        elif userinput1=="4":
                            app.SearchByChannel()
                        elif userinput1=="5":
                            app.LatestIndianNews()
                        elif userinput1=="q":
                            exit()
                        else:
                            print("An Error Occured!")
                            app.speak("An Error Occured!")
                
                elif userinput=="q":
                    exit()
                else:
                    print("Please Type From The Above Options:- ")
                    app.speak("Please Type From The Above Options:- ")
                    continue
            except Exception as e:
                print("Error.......")
                app.speak("Error.......")
                continue
    except Exception as e:
        print("Error...")
    finally:
        print("Thanks For Using Indian News Reader😊😊😊😊!")
        app.speak("Thanks For Using Indian News Reader!")