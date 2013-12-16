import json
import urllib
import datetime
import time

"""
Freebase API-> Search.
1. Construct Search Query to get the mid, using name as the keyword.
2. use MQL read to get the date_of_birth based on the mid.
Return the first record [name,data_of_birth].

"""
def search_by_name(name):
    api_key = 'AIzaSyD2scfSUwizVDGJ8XMBhxM8FpNfUqL4g6M' #my api key
    query = name
    filter= '(any type:/people/person)' #filter, search in people/person
    service_url = 'https://www.googleapis.com/freebase/v1/search' # search API url
    params = {
            'query': query,
            'key': api_key,
            'filter': filter
    } #paramaters of the search query
    output = [] #query result output
    url = service_url + '?' + urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())
    for result in response['result']:
        output = mql_read(result['mid'])#use mqlread to get information based on the mid.
        break  # only need first result
    return output

"""
Freebase API->MQL Read.
Construct MQLRead query to obtain person name and date_of_birth based on a given mid.
return people name and data_of_birth

"""
def mql_read(id):
    mql_service_url = 'https://www.googleapis.com/freebase/v1/mqlread'
    query = {
        "id": id,
        "type": "/people/person",
        "name": "null",
        "date_of_birth": "null"
    }
    qStr=[]
    """
    Below for-loop is to construct the query string for MQLRead.
    We don't need double-quote for null value.
    """
    for entry in query.keys():
        #temp = '"'+entry + '"'+':"'+query.get(entry)+'"'
        if query.get(entry).__eq__("null"):
            temp = '"'+entry + '"'+':'+query.get(entry)+''
        else:
            temp = '"'+entry + '"'+':"'+query.get(entry)+'"'
        qStr.append(temp)


    mql_url = mql_service_url + '?query={' + ','.join(qStr)+'}'
    response = json.loads(urllib.urlopen(mql_url).read())
    try:
        d = json.dumps(response['result'])
        o = json.loads(d) # convert result to json object
        return o
    except Exception, err: # print error if it failed to convert result to json.
        print 'ERR:',response,err.message
#####

"""
Format the query result: data-of-birth.
If no data_of_birth found: result should be xx-xx-xxxx
If the dob only contains year information and can not be converted to date: result should be xx-xx-YYYY
If the data_of_birth is ok, format the original yyyy-mm-dd to dd-mm-yyyy

"""
def getpeople(name):
    dictobj = {}
    try:
        o = search_by_name(name)
        dictobj['name']= o['name']
        #dictobj['dob']=o['date_of_birth']
        if o['date_of_birth']:
            try:
                dictobj['dob']=datetime.datetime.strptime(o['date_of_birth'], '%Y-%m-%d').strftime('%d-%m-%Y')
            except ValueError:
                dictobj['dob']= ''.join(['xx-xx-',o['date_of_birth']])
        else:
            dictobj['dob']='xx-xx-xxxx'
        return dictobj
    except Exception,err:
        print err.message
        dictobj['name']= name
        dictobj['dob'] = 'xx-xx-xxxx'
        return dictobj



"""
read a list of people's name from txt file and get the date_of_birth for each of them.
return a list of DOB, one line per person.
"""
def batch_read(filepath):
    m = []
    with open(filepath) as f:
        for line in f:
            #print line
            time.sleep(0.1)
            o = getpeople(line.strip())
            #time.sleep(1)
            print 'info received: ',o['name'],o['dob']
            m.append(o['dob'])
            #break
    return m

"""
write a list to txt file.

"""
def batch_write(l,filepath):
    try:
        with open(filepath,'w+') as f:
            for i in l:
                f.write(i)
                f.write('\n')
        print 'Batch_write succeed.'
    except Exception,err:
        print err.message,'.batch_write failed'
    return 0

"""
read file, return a list contains each line
"""
def read_file(filepath):
    l=[]
    try:
        with open(filepath) as f:
            for i in f:
                l.append(i.strip())

    except Exception,err:
        print err.message,'.read_file failed'
        return
    return l

"""
Validate results against the truth.
Input:  1. filepath of the result file.
        2. filepath of the truth file.

Print  accuracy of date, month and year.
Return a list of accuracies

"""
def compare_result(resultpath, truthpath):
    result = read_file(resultpath)
    truth = read_file(truthpath)
    counter_d=0#Count number of correct days
    counter_m=0#count number of correct months
    counter_y=0#count number of correct years
    for i in range (0,len(truth)):
        rdate = result[i]
        tdate = truth[i]
        if rdate.__eq__(tdate):
            counter_d+=1
            counter_m+=1
            counter_y+=1
        elif rdate[3:5].__eq__(tdate[3:5]) and rdate[6:10].__eq__(tdate[6:10]):
            counter_m+=1
            counter_y+=1
        elif rdate[6:10].__eq__(tdate[6:10]):
            counter_y+=1

        l = len(truth)+0.0
        accuracy = {'Full_DOB_Accuracy': "{0:.0f}%".format(counter_d/l*100), 'Year/Month_Accuracy':"{0:.0f}%".format(counter_m/l*100), 'Year_Accuracy':"{0:.0f}%".format(counter_y/l*100)}

    for k,v in sorted(accuracy.items()): #sort and print the result
        print k,':',v

    return accuracy



l= batch_read('Data/testing.txt') #query freebase to get dob of list of people in file Data/testing.txt
batch_write(l,'Data/output.txt') #write result to Data/output.txt
print '---------' \
      'Accuracy:'
compare_result('Data/output.txt', 'Data/testing_DOB.txt') # compare the result in output.txt against the ground truth in testing_DOB.txt

