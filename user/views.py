from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
import json
from django.views.decorators.cache import cache_control
#--------------------------------------------------
with open('data.json','r') as fh:
    data=json.load(fh)
flights=data["flights"]
tickets=data["tickets"]
description={}
for fid,flight in data['flights'].items():
    description[fid]=0 
current_user={"username":"","password":""}
current_page={"page":"","argument":{}}
displayflights={}
length=len(flights)
Edit={}
for  fid,flight in flights.items():
    Edit[fid]=0
add=0

def user_loggedin():
    if request.session.get("username") is not None:
        return True
    else:
        return False
def login(request):
    if request.method=="GET":
        return render(request,"user/index.html",{'page':'index'})
def index(request):
    if request.session.get("username"):
        if request.session.get("page") is not None:
            return redirect(request.session.get("page"))
    elif request.POST.get("username") is not None:
        if {'username':request.POST["username"],'password':request.POST['password']} in data["userid"]:
            request.session["username"]=request.POST["username"]
            request.session["password"]=request.POST["password"]
            return redirect("booking") 
        else:
            error="Wrong Credentials"
            return render(request,"user/index.html", {"error":error})
    else:
        return redirect("booking")
def register(request):
    if request.method=="GET":
        return render(request,"user/index.html",{'newuser':'yes'})
    elif request.POST.get("newusername") is not None:
        if {"username":request.POST["newusername"],"password":request.POST["newpassword"]} in data["userid"]:
            return render(request,"user/index.html",{'newuser':'yes','error':"User already exists"})
        else:
            data["userid"].append({"username":request.POST["newusername"],"password":request.POST["newpassword"]})
            request.session["username"]=request.POST["newusername"]
            request.session["password"]=request.POST["newpassword"]
            data["tickets"][request.session["username"]]={"ticketid": "1","bookings": {}}
            with open ('data.json','w') as fh:
                json.dump(data,fh,indent=4)
            return redirect("booking")
def logout(request):
    if request.session.get("username"):
        del request.session["username"]
        del request.session["password"]
    else:
        return redirect("errorpage")
    return redirect("login")

def errorpage(request):
    return render(request,"user/errorpage.html")

@cache_control(no_store=True, user_loggedin=True)
def adminpage(request):
    with open('data.json','r') as fh:
        data=json.load(fh)
        flights=data['flights']
    if request.method=="GET":
        if request.session.get("username") =="durbar":
            return render(request, "admin.html",{'flights':data['flights'],'add':add,'edit':Edit})
        else:
            return render(request,"user/errorpage.html",{'user':'durbar'})
    if request.session.get("username") =="durbar":
        #return render(request, "admin.html",{'flights':data['flights'],'add':add,'edit':Edit})
        if request.POST.get("addflight") is not None:
            globals()['add']=(globals()['add']+1)%2
            #return Httprequest('',{'add':add})
            return render(request, "admin.html",{'flights':flights,'add':add,'edit':Edit})
        elif request.POST.get("add") is not None:
            #globals()['add']=0
            if request.POST["id"] in flights.keys():
                flight={
                    "id":request.POST["id"],
                    "source":request.POST["source"],
                    "destination":request.POST["destination"],
                    "deptime":request.POST["deptime"],
                    "depdate":request.POST["depdate"],
                    "arrtime":request.POST["arrtime"],
                    "arrdate":request.POST["arrdate"],
                    "capacity":int(request.POST["remain"]),
                    "remain":int(request.POST["remain"]),
                    "price":int(request.POST["price"])}
                return render(request,"admin.html",{'flights':flights,'flight':flight,'add':add,'edit':Edit,'error':'ERROR: This flight id aready exists'})
            remainingseats=[]
            for i in range(1,int(request.POST["remain"])+1):
                remainingseats.append(str(i))
            flights[request.POST["id"]]={
                    "id":request.POST["id"],
                    "source":request.POST["source"],
                    "destination":request.POST["destination"],
                    "deptime":request.POST["deptime"],
                    "depdate":request.POST["depdate"],
                    "arrtime":request.POST["arrtime"],
                    "arrdate":request.POST["arrdate"],
                    "capacity":int(request.POST["remain"]),
                    "remain":int(request.POST["remain"]),
                    "remainingseats":remainingseats,
                    "price":int(request.POST["price"])}
            data["flights"]=flights
            with open('data.json','w') as fh:
                json.dump(data,fh,indent=4)
            Edit[request.POST["id"]]=0
            return render(request,"admin.html",{'flights':flights,'add':add,'edit':Edit})
        elif request.POST.get("editbutton") is not None:
            Edit[request.POST["editbutton"]]=(Edit[request.POST["editbutton"]]+1)%2
            return render(request, "admin.html", {'flights':flights,'add':add,'edit':Edit})
        elif request.POST.get("editdetailsbtn") is not None:
            del flights[request.POST["editdetailsbtn"]]
            del Edit[request.POST["editdetailsbtn"]]
            remainingseats=[]
            for i in range(1,int(request.POST["remain"])+1):
                remainingseats.append(str(i))
            flights[request.POST["id"]]={       
                "id":request.POST["id"],
                    "source":request.POST["source"],
                    "destination":request.POST["destination"],
                    "deptime":request.POST["deptime"],
                    "depdate":request.POST["depdate"],
                    "arrtime":request.POST["arrtime"],
                    "arrdate":request.POST["arrdate"],
                    "capacity":int(request.POST["remain"]),
                    "remain":int(request.POST["remain"]),
                    "remainingseats":remainingseats,
                    "price":int(request.POST["price"])}
            data["flights"]=flights
            Edit[request.POST["id"]]=0
            with open('data.json','w') as fh:
                json.dump(data,fh,indent=4)
            return render(request, "admin.html",{'flights':flights,'add':add,'edit':Edit})
        elif request.POST.get("deletebutton") is not None:
            flight=flights[request.POST["deletebutton"]]
            cancelled_tickets={}
            for user in data["userid"]:
                cancelled_tickets[user["username"]]=[]
            for user, tickets in data["tickets"].items():
                for tickid, booking in tickets["bookings"].items():
                    if booking["fid"]==request.POST["deletebutton"]:
                        cancelled_tickets[user].append(tickid)
            for user,ticks in cancelled_tickets.items():
                for ticketid in ticks:
                    data["tickets"][user]["bookings"][ticketid]["status"]="flight_cancelled"
                    data["tickets"][user]["bookings"][ticketid]["flightdetails"]=flight["source"]+" ("+flight["depdate"]+" at "+flight["deptime"]+")"+" to "+flight["destination"]+" ("+flight["arrdate"]+" at "+flight["arrtime"]+")"
            del flights[request.POST["deletebutton"]]
            del Edit[request.POST["deletebutton"]]
            data["flights"]=flights
            with open('data.json','w') as fh:
                json.dump(data,fh,indent=4)
            return render(request, "admin.html",{'flights':flights,'add':add,'edit':Edit})
#@cache_control(no_store=True, user_loggedin=True)
def booking(request):
    request.session["page"]="booking"
    with open ('data.json',"r") as json_file:
        data=json.load(json_file)
    flights= data["flights"]
    request.session["pagehtml"]="user/booking.html"
    request.session["pageargument"]={'flights':flights,'description':description,'user':request.session.get("username")}
    #Booking another ticket after payment (from payment page)
    if request.POST.get("anotherbooking") is not None:
        tickets=data["tickets"]
        ticketid=tickets[request.session["username"]]["ticketid"]
        fid=tickets[request.session["username"]]["bookings"][ticketid]["fid"]
        data["flights"][fid]=tickets[request.session["username"]]["bookings"][ticketid]["flight"]
        del data["tickets"][request.session["username"]]["bookings"][ticketid]["flight"]
        tickets[request.session["username"]]["ticketid"]=str(int(ticketid)+1)
        data["tickets"]=tickets
        description[fid]=0
        with open('data.json','w') as fh:
            json.dump(data,fh,indent=4)
        return render(request,"user/booking.html",{'flights':flights,'description':description,'user':request.session["username"]})
    #Cancel payment on payment page and go back to booking page
    elif request.POST.get("cancelpayment") is not None:
        ticketid=request.POST["cancelpayment"]
        fid=data["tickets"][request.session["username"]]["bookings"][ticketid]["fid"]
        seatdetails=data["tickets"][request.session["username"]]["bookings"][ticketid]["seatdetails"]
        for seat,tick in seatdetails.items():
            data["flights"][fid]["remainingseats"].append(seat)
            data["flights"][fid]["remain"]+=1
        del data["tickets"][request.session["username"]]["bookings"][ticketid]["seatdetails"]
        data["flights"][fid]["price"]/=1.05**(int((data["flights"][fid]["capacity"]-flights[fid]["remain"])/10))
        del data["tickets"][request.session["username"]]["bookings"]
        data["tickets"][request.session["username"]]["bookings"]={}
        description[fid]=0
        with open('data.json','w') as fh:
            json.dump(data,fh,indent=4)
        return render(request,"user/booking.html",{'flights':flights,'description':description,'user':request.session["username"]})
    #Description button-click
    elif request.POST.get("description") is not None:
        fid=request.POST["description"]
        description[fid]=(description[fid]+1)%2
        if len(displayflights)==0:
            return render(request,"user/booking.html",{'flights':flights,'description':description,'user':request.session.get("username")})
        else:
            return render(request,"user/booking.html",{"flights":displayflights,'description':description,'user':request.session.get("username")})
    #Go back from My bookings page
    elif request.POST.get("goback") is not None:
        if len(displayflights)==0:
            return render(request,"user/booking.html",{'flights':flights,'description':description,'user':request.session["username"]})
        else:
            return render(request,"user/booking.html",{"flights":displayflights,'description':description,'user':request.session["username"]})
    # Search for Flights
    elif request.POST.get("sourcesearch") is not None:
        displayflights.clear()
        if request.POST.get("sourcesearch")!="" and request.POST.get("destinationsearch")!="":
            for fid,flight in flights.items():
                if flight["source"]==request.POST.get("sourcesearch") and flight["destination"]==request.POST.get("destinationsearch"):
                    displayflights[fid]=flight
            if displayflights:
                return render(request, "user/booking.html",{'flights':displayflights,'description':description,'user':request.session["username"]})
            else:
                return render(request, "user/booking.html",{'message':"No flights for your search"})
            return render(request, "user/booking.html",{'flights':displayflights})
        elif request.POST.get("sourcesearch")=="" and request.POST.get("destinationsearch")=="":
            return render(request, "user/booking.html",{'flights':flights,'message':"ERROR: Please type something",'description':description,'user':request.session["username"]})
        else:
            for fid,flight in flights.items():
                if flight["source"]==request.POST.get("sourcesearch") or flight["destination"]==request.POST.get("destinationsearch"):
                    displayflights[fid]=flight        
            return render(request, "user/booking.html",{'flights':displayflights,'description':description,'user':request.session["username"]})
    #DO NOT BOOK
    elif request.POST.get("donotbook") is not None:
        ticketid=data["tickets"][request.session["username"]]["ticketid"]
        del data["tickets"][request.session["username"]]["bookings"][ticketid]
        with open('data.json','w') as fh:
            json.dump(data,fh,indent=4)
        return render(request,"user/booking.html",{'flights':flights,'description':description,'user':request.session["username"]})
    #Directly enetring into bookings
    else:
        return render(request,request.session["pagehtml"],request.session["pageargument"])
@cache_control(no_store=True, user_loggedin=True)
def payment(request):
    request.session["page"]="payment"
    if request.session.get("username") is None:
        return redirect("errorpage")
    elif request.POST.get("submitdetails"):
        with open ('data.json',"r+") as json_file:
            data=json.load(json_file)
        tickets=data["tickets"]
        flights=data["flights"]
        ticketid=data["tickets"][request.session["username"]]["ticketid"]
        ticket=data["tickets"][request.session["username"]]["bookings"][ticketid]
        seatdetails={}
        fid=ticket["fid"]
        flight=data["flights"][fid]
        totalcost=flights[fid]["price"]*int(request.POST["submitdetails"])
        for h in range(1,1+int(request.POST["submitdetails"])):
            tempdict={"name":request.POST["name"+str(h)],"age":request.POST["age"+str(h)],"gender":request.POST["gender"+str(h)],"meals":request.POST["meals"+str(h)]}
            tempdict["ticketcost"]=flights[fid]["price"]
            if request.POST["meals"+str(h)]=="yes":
                tempdict["ticketcost"]+=500
                totalcost+=500
            seatdetails[flight["remainingseats"].pop(0)]=tempdict
        ticket["seatdetails"]=seatdetails
        ticket["cost"]=totalcost
        ticket["no"]=int(request.POST["submitdetails"])
        flight["remain"]-=int(request.POST["submitdetails"])
        flight["price"]*=1.05**(int((flights[fid]["capacity"]-flights[fid]["remain"])/10))
        ticket["flight"]=flight
        tickets[request.session["username"]]["bookings"][ticketid]=ticket
        flightdetails=flight["source"]+" ("+flight["depdate"]+" at "+flight["deptime"]+")"+" to "+flight["destination"]+" ("+flight["arrdate"]+" at "+flight["arrtime"]+")"
        data["tickets"]=tickets
        with open('data.json','w') as fh:
            json.dump(data,fh,indent=4)
        request.session["pagehtml"]="user/payment.html"
        request.session["pageargument"]={'flightdetails':flightdetails,'ticket':ticket,'tickets':json.dumps(tickets),'tickid':ticketid}
        return render(request,"user/payment.html",{'flightdetails':flightdetails,'ticket':ticket,'tickets':json.dumps(tickets),'tickid':ticketid})
    else:
        if request.session.get("username") is not None:
            return render(request,request.session["pagehtml"],request.session["pageargument"])

@cache_control(no_store=True, user_loggedin=True)
def ticketbooking(request):
    request.session["page"]="ticketbooking"
    if request.session.get("username") is None:
        return redirect("errorpage")
    elif request.POST.get("bookticket"):
        with open ('data.json',"r") as json_file:
            data=json.load(json_file)
        ticketid=data["tickets"][request.session["username"]]["ticketid"]
        data["tickets"][request.session["username"]]["bookings"][ticketid]={"fid":request.POST["bookticket"]}
        with open ('data.json',"w") as json_file:
            json.dump(data,json_file,indent=4)
        request.session["pagehtml"]="user/ticketbooking.html"
        request.session["pageargument"]={"numberofpassengers":request.POST["number"]}
        return render(request,"user/ticketbooking.html",{"numberofpassengers":request.POST["number"]})
    else:
        if request.session.get("username"):
            return render(request,request.session["pagehtml"],request.session["pageargument"])
@cache_control(no_store=True, user_loggedin=True)
def mybookings(request):
    request.session["page"]="mybookings"
    if request.session.get("username") is None:
        return redirect("errorpage")
    with open ('data.json',"r") as json_file:
        data=json.load(json_file)
        flights= data["flights"]
        tickets=data["tickets"]
    request.session["pagehtml"]="user/Mybookings.html"
    if request.POST.get("goback"):
        return render(request, "user/mtbookings.html",{'tickets':tickets[request.session["username"]]["bookings"]})
    else:
        if request.session["username"]:
            request.session["pageargument"]={'tickets':tickets[request.session["username"]]["bookings"],'number':1}
            return render(request,request.session["pagehtml"],{'tickets':tickets[request.session["username"]]["bookings"],'flights':flights,'message':"You have no bookings"})
@cache_control(no_store=True, user_loggedin=True)
def cancelbooking(request):
    request.session["page"]="cancelbooking"
    if request.session.get("username") is None:
        return redirect("errorpage")
    request.session["pagehtml"]="user/cancelbooking.html"
    with open ('data.json',"r+") as json_file:
        data=json.load(json_file)
    flights= data["flights"]
    tickets=data["tickets"]
    if request.POST.get("cancelbooking") is not None:
        return render(request, "user/cancelbooking.html", {'tickid':request.POST["cancelbooking"],'seatdetails':tickets[request.session["username"]]["bookings"][request.POST["cancelbooking"]]["seatdetails"]})

    elif request.POST.get("cancelticket"):
        string=request.POST["cancelticket"].split("-")
        ticketid=string[1]
        fid=tickets[request.session["username"]]["bookings"][ticketid]["fid"]    
        tickets[request.session["username"]]["bookings"][ticketid]["cost"]-=tickets[request.session["username"]]["bookings"][ticketid]["seatdetails"][string[0]]["ticketcost"]
        tickets[request.session["username"]]["bookings"][ticketid]["no"]-=1
        del tickets[request.session["username"]]["bookings"][ticketid]["seatdetails"][string[0]]
        flights[fid]["remain"]+=1
        flights[fid]["remainingseats"].append(string[0])
        flights[fid]["price"]/=1.05**(int((flights[fid]["capacity"]-flights[fid]["remain"])/10))
        data["tickets"][request.session["username"]]["bookings"][ticketid]["flight"]=data["flights"][fid]
        if tickets[request.session["username"]]["bookings"][ticketid]["cost"]==0:
            del tickets[request.session["username"]]["bookings"][ticketid]
        data["tickets"]=tickets
        data["flights"]=flights
        with open('data.json','w') as fh:
            json.dump(data,fh,indent=4)
        request.session["pageargument"]={'tickets':tickets[request.session["username"]]["bookings"],'message':"You have no bookings"}
        return render(request,"user/Mybookings.html",{'tickets':tickets[request.session["username"]]["bookings"],'message':"You have no bookings"})
    else:
        return render(request,request.session["pagehtml"],request.session["pageargument"])