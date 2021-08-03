from django import template
register= template.Library()

@register.filter
def element(dictionary, key):
    return dictionary[str(key)]
register.filter('element',element)

@register.filter
def remainatcurrentprice(value):
    if value%10==0:
        return 10
    else:
        return value%10
register.filter('remainatcurrentprice',remainatcurrentprice)

@register.filter
def remainathikeprice(value):
    if value%10==0:
        return value-10
    else:
        return int(value/10)*10
register.filter('remainathikeprice',remainathikeprice)

@register.filter
def roundoff(value):
    return round(value,2)
register.filter('roundoff',roundoff)

@register.filter
def seatnumber(seatnumber,ticketid):
    return (seatnumber+"-"+ticketid)
register.filter('seatnumber',seatnumber)

@register.filter
def flightdetails(flights,fid):
    return flights[fid]["source"]+" ("+flights[fid]["depdate"]+" at "+flights[fid]["deptime"]+")"+" to "+flights[fid]["destination"]+" ("+flights[fid]["arrdate"]+" at "+flights[fid]["arrtime"]+")"
register.filter('flightdetails',flightdetails)

@register.filter
def Range(n):
    return range(1,int(n)+1)
register.filter('Range',Range)