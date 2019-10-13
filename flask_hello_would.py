from flask import Flask, request, redirect
from flask import render_template
from ast import literal_eval
from uszipcode import SearchEngine
# from crypto import crypto
from firebase import firebase #nick fucked line 6
firebase = firebase.FirebaseApplication('https://language-2ef38.firebaseio.com/')
# thing = firebase.get("LanguageData",None)
submitt = False
response_variables = {}
app = Flask(__name__)

# Input("Kyan", ["Hebrew, English"],["Spanish"])
# print(database)

locations_database = {}
nonlocations_database = {}
class Player1():
    def __init__(self, name,known, unknown,  location, email, phoneNumber):
        self.name = name
        self.known = known
        self.unknown = unknown
        self.matches = []
        self.matchName = {}
        self.matchNames = []
        self.email = email
        self.phoneNumber = phoneNumber
        search = SearchEngine(simple_zipcode=True)
        zipcode = search.by_zipcode(location)
        self.location  = zipcode.values()[7:9]   

        dictionary = []
        dictionary.append(self.name)
        dictionary.append(self.known)
        dictionary.append(self.unknown)
        dictionary.append(self.location)
        dictionary.append(self.email)
        dictionary.append(self.phoneNumber)
        dictionary.append(self.matches)     
        firebase.post("/LanguageData1",dictionary)

    def match_people(self):
        for person in firebase.get("LanguageData1",None):
            dude = firebase.get("LanguageData1/"+person,None)
            print(dude[0])
            common_language = False
            boolean_l_k = False 
            boolean_k_l = False
            matched = False
            close = False
            languages_known = dude[1]
            languages_unknown = dude[2]

            if ((dude[3][0] - self.location[0])**2 + (dude[3][1] - self.location[1])**2)**(1/2) < 1:
                close = True

            for lang1 in languages_known: # makes sure that they both know same langugage
                for lang2 in self.known:
                    if lang1 == lang2:
                        common_language = True 
            
            
            for lang1 in languages_unknown: #Makes sure the target person knows the language that our person wants to know
                for lang2 in self.known:
                    if lang1 == lang2:
                        boolean_k_l = True 
                
            for lang1 in languages_known: #checks for reverse
                for lang2 in self.unknown:
                    if lang1 == lang2:
                        boolean_l_k = True

            if boolean_k_l and boolean_l_k and common_language and close:
                matched = True
                self.matches.append(dude)
                self.matchName["Name"]=dude[0]
                self.matchName["Email"]=dude[4]
                self.matchName["Phone Number"]=dude[5]
                self.matchNames.append(self.matchName)
                self.matchName = {}
                matched == True
        
class Player2():
    def __init__(self, name, known, unknown, email, phoneNumber):
        self.name = name
        self.known = known
        self.unknown = unknown
        self.matches = []
        self.email = email
        self.phoneNumber = phoneNumber
        self.matchName = {}
        self.matchNames = []
 
        dictionary = []
        dictionary.append(self.name)
        dictionary.append(self.known)
        dictionary.append(self.unknown)
        dictionary.append(self.email)
        dictionary.append(self.phoneNumber)   
        dictionary.append(self.matches)     
        firebase.post("LanguageData2",(dictionary))

    def match_people(self):
        for person in firebase.get("LanguageData2",None):
            dude = firebase.get("LanguageData2/"+person,None)
            common_language = False
            boolean_l_k = False 
            boolean_k_l = False
            matched = False
            languages_known = dude[1]
            languages_unknown = dude[2]

            for lang1 in languages_known:
                for lang2 in self.known:
                    if lang1 == lang2:
                        common_language = True 
            
            for lang1 in languages_unknown:
                for lang2 in self.known:
                    if lang1 == lang2:
                        boolean_k_l = True  
                
            for lang1 in languages_known:
                for lang2 in self.unknown:
                    if lang1 == lang2:
                        boolean_l_k = True  

            if boolean_k_l and boolean_l_k and common_language:
                matched = True
                self.matches.append(dude)
                self.matchName["Name"]=dude[0]
                self.matchName["Email"]=dude[3]
                self.matchName["Phone Number"]=dude[4]
                self.matchNames.append(self.matchName)
                self.matchName = {}
                matched == True

# George = Player2("George",["English","Mandarin"],["Spanish"],"george@gmail.com","911")
# Alex = Player2("Alex", ["Hebrew", "Spanish"], ["Mandarin"],"alex@gmail.com","911")
# Dylan = Player2("Dylan", ["Mandarin", "Spanish","Hebrew"], ["English"],"dylan@gmail.com","911")
# George.match_people()

persontest = 0

@app.route('/')
def hello_world():
    return 'This website is working, are you?'

@app.route('/inputs', methods=['GET', 'POST']) #allow both GET and POST requests
def form_example():
    if request.method == 'POST': #this block is only entered when the form is submitted
        # response_variables = {"name": request.form["name"], "known_language": request.form["known_language"], "desired_language":request.form["desired_language"]}
        # submitt = True

        return render_template('response.html', name=request.form["name"], known_language=request.form["known_language"], desired_language=request.form["desired_language"])

    return render_template('inputtts.html')

@app.route('/index', methods=['GET']) 
def landing():
    return render_template('index.html')

@app.route('/landing', methods=['GET']) 
def landing_page():
    return render_template('landing.html')

@app.route('/form/<comm_method>', methods=['GET', 'POST']) #allow both GET and POST requests
def form(comm_method):

    zip_use = False
    if comm_method == "local":
        zip_use = True

    if request.method == 'POST': #this block is only entered when the form is submitted
        # response_variables = {"name": request.form["name"], "known_language": request.form["known_language"], "desired_language":request.form["desired_language"]}
        # submitt = True
        request.form.getlist('hello')
        name = request.form["name"]
        phonenum = request.form["phonenum"]
        
        email = request.form["email"]
        known_language = request.form.getlist('known_language')
        desired_language = request.form.getlist('languages')
        if zip_use == True:
            print("zip use true")
            zipcode = request.form["zipcode"]
            persontest = Player1(name,known_language,desired_language,zipcode,email,phonenum)
            print(persontest.name)

        else:
            persontest = Player2(name,known_language,desired_language,email,phonenum)
        persontest.match_people()
        matches = persontest.matches
        matchNames = persontest.matchNames
        # print(firebase.get("LanguageData",None))
        # print(persontest.name)
        # print(persontest.known)
        # print(persontest.unknown)
        # print(persontest.email)
        # print(persontest.phoneNumber)
        # from firebase import firebase
        # firebase = firebase.FirebaseApplication('https://language-2ef38.firebaseio.com/')
        


        return render_template('response.html', zip_use=zip_use, matchNames = matchNames, matches=matches, name=name, known_language=str(known_language), desired_language=str(desired_language))

    return render_template('form.html',zip_use = zip_use)

if __name__ == '__main__':
    app.run()
    # return render_template('form.html')