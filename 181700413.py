import re
import json
#str = '2!王五,福建省福州市鼓楼18960221533区五一北路123号福州鼓楼医院.'
def split_string(str):
    s=str.split(',')
    empty_dict=dict()
    empty_dict['name']=s[0][2:]
    patten=re.compile(r'\d{11}')
    telephone=patten.findall(s[1])
    empty_dict['telephone']=telephone[0]
    hh=s[1].split(telephone[0])
    hh = s[1].split(telephone[0])
    address = hh[0] + hh[1][0:-1]
    empty_dict['address'] = address
    return empty_dict
def alladdress():
    with open('address_query.txt','r')as f:
        t=f.read()
        s=t.split('\n')
        cnt=0
        empty_dict=dict()
        for i in s:
            if(cnt%3==0):
                list_add=s[cnt+2].split(' ')
                empty_dict[s[cnt+1]]=list_add
            cnt=cnt+1
        return empty_dict
while 1:
    try:
        str = input();
        if (str == "END"):
            break
    except EOFError:
        break
    rank=str[0]
    t = split_string(str)
    str = t['address']
    newstr=str
    query_address = alladdress()
    provine = []
    county = ['县','区','市']
    street = ['街道','镇','乡']
    road = ['路','巷','道','街','弄','胡同']
    for key in query_address:
        provine.append(key)
    for i in provine:
        lists=[]
        cnt=0
        for j in query_address[i]:
            if(j==""):
                lists.append(cnt)
            cnt = cnt+1
        for j in lists:
            query_address[i].pop((int)(j))
    for i in provine:
        if(str.find(i) != -1):
            t['provine'] = i
            if(i == '北京' or i == '上海' or i == '天津' or i == '重庆'):
                t['city'] = i+'市'
                t['provine']=t['provine']
                newstr = str[2:]
                if(newstr[0]=='市'):
                    newstr=str[3:]
            else :
                if(i[-1]!='区'):
                    t['provine'] = t['provine'] + '省'
                for j in query_address[i]:
                    city = j[0:-1]
                    if(str.find(city) != -1):
                        t['city'] = j
                        if(j[-1]=='市'):
                            if(str.find('市') != -1 and str[str.find('市')-1] == city[-1]):
                                    index1=str.find('市')
                                    newstr=str[index1+1:]
                            else :
                                index1=str.find(city[-1])
                                newstr=str[index1+1:]
                        else:
                            index1=str.find(j[-1])
                            newstr=str[index1+1:]
            break
        else:
            t['provine'] = ""
            t['city'] = ""

    for k in county:
        if(newstr.find(k) != -1):
            index2=newstr.find(k)
            t['county'] = newstr[0:index2+1]
            newstr = newstr[index2+1:]
            break
        else:
            t['county'] = ""
    for l in street:
        if (newstr.find(l) != -1):
            index3 = newstr.find(l)
            if(l=='街道'):
                t['street'] = newstr[0:index3 + 2]
                newstr = newstr[index3 + 2:]
            else:
                t['street'] = newstr[0:index3 + 1]
                newstr = newstr[index3 + 1:]
            break
        else:
            t['street'] = ""
    if(rank == '1'):
        t['last'] = newstr
    elif(rank == '2'or rank == '3'):
        for m in road:
            if (newstr.find(m) != -1):
                index4 = newstr.find(m)
                t['road'] = newstr[0:index4 + 1]
                newstr = newstr[index4 + 1:]
                break
            else :
                t['road'] = ""
        if(newstr.find('号') != -1):
            index5 = newstr.find('号')
            t['number'] = newstr[0:index5 + 1]
            newstr = newstr[index5 + 1:]
        else:
            t['number'] = ""
        t['last'] = newstr
    #t = json.dumps(t, ensure_ascii=False)
    t.pop('address')
    cnt=0
    address=[]
    for key in t:
        if(cnt>=2):
            address.append(t[key])
        cnt=cnt+1
    result=dict()
    result['姓名'] = t['name']
    result['手机'] = t['telephone']
    result['地址'] = address
    hh=json.dumps(result,ensure_ascii=False)
    print(hh)

