from django.shortcuts import render
import json
import os
from django.template.defaulttags import csrf_token
from django.http import HttpResponse
with open('data.json','r') as fh:
    data=json.load(fh)
flights=data['flights']
length=len(flights)
Edit={}
for  fid,flight in flights.items():
    Edit[fid]=0
add=0
def index(response):
     return render(response, "useradmin/index.html")
def adminpage(response):
    with open('data.json','r') as fh:
        data=json.load(fh)
    if (response.POST.get("username")=='durbar') and (response.POST.get("password")=='Durbar99@'):
        return render(response, "useradmin/admin.html",{'flights':data['flights'],'add':add,'edit':Edit})
    else:
        return render(response, "useradmin/index.html",{'error':'Error : Wrong Credentials'})
def edit(response):
    with open('data.json','r') as fh:
        data=json.load(fh)
        flights=data['flights']
    if response.POST.get("addflight") is not None:
        globals()['add']=(globals()['add']+1)%2
        #return HttpResponse('',{'add':add})
        return render(response, "useradmin/admin.html",{'flights':flights,'add':add,'edit':Edit})
    elif response.POST.get("add") is not None:
        #globals()['add']=0
        if response.POST["id"] in flights.keys():
            flight={
                "id":response.POST["id"],
                "source":response.POST["source"],
                "destination":response.POST["destination"],
                "deptime":response.POST["deptime"],
                "depdate":response.POST["depdate"],
                "arrtime":response.POST["arrtime"],
                "arrdate":response.POST["arrdate"],
                "capacity":int(response.POST["remain"]),
                "remain":int(response.POST["remain"]),
                "price":int(response.POST["price"])}
            return render(response,"useradmin/admin.html",{'flights':flights,'flight':flight,'add':add,'edit':Edit,'error':'ERROR: This flight id aready exists'})
        Edit[response.POST["id"]]=0
        remainingseats=[]
        for i in range(1,int(response.POST["remain"])+1):
            remainingseats.append(str(i))
        flights[response.POST["id"]]={
                "id":response.POST["id"],
                "source":response.POST["source"],
                "destination":response.POST["destination"],
                "deptime":response.POST["deptime"],
                "depdate":response.POST["depdate"],
                "arrtime":response.POST["arrtime"],
                "arrdate":response.POST["arrdate"],
                "capacity":int(response.POST["remain"]),
                "remain":int(response.POST["remain"]),
                "remainingseats":remainingseats,
                "price":int(response.POST["price"])}
        data["flights"]=flights
        with open('data.json','w') as fh:
            json.dump(data,fh,indent=4)
        return render(response,"useradmin/admin.html",{'flights':flights,'add':add,'edit':Edit})
    elif response.POST.get("editbutton") is not None:
        Edit[response.POST["editbutton"]]=(Edit[response.POST["editbutton"]]+1)%2
        return render(response, "useradmin/admin.html", {'flights':flights,'add':add,'edit':Edit})
    elif response.POST.get("editdetailsbtn") is not None:
        del flights[response.POST["editdetailsbtn"]]
        del Edit[response.POST["editdetailsbtn"]]
        remainingseats=[]
        for i in range(1,int(response.POST["remain"])+1):
            remainingseats.append(str(i))
        flights[response.POST["id"]]={       
            "id":response.POST["id"],
                "source":response.POST["source"],
                "destination":response.POST["destination"],
                "deptime":response.POST["deptime"],
                "depdate":response.POST["depdate"],
                "arrtime":response.POST["arrtime"],
                "arrdate":response.POST["arrdate"],
                "capacity":int(response.POST["remain"]),
                "remain":int(response.POST["remain"]),
                "remainingseats":remainingseats,
                "price":int(response.POST["price"])}
        data["flights"]=flights
        Edit[response.POST["id"]]=0
        with open('data.json','w') as fh:
            json.dump(data,fh,indent=4)
        return render(response, "useradmin/admin.html",{'flights':flights,'add':add,'edit':Edit})
    elif response.POST.get("deletebutton") is not None:
        del flights[response.POST["deletebutton"]]
        del Edit[response.POST["deletebutton"]]
        data["flights"]=flights
        with open('data.json','w') as fh:
            json.dump(data,fh,indent=4)
        return render(response, "useradmin/admin.html",{'flights':flights,'add':add,'edit':Edit})
    