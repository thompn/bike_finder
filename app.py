import bs4, requests, re, cssutils, sys, random
import MySQLdb, datetime, telepot,time
#49248388

# define SQL queries to be used
tgkey = "SELECT * FROM auth.keys WHERE name = '%s'"


# function to get keys from db
def get_auth(name):
    #open db
    db=MySQLdb.connect(read_default_group='auth')
    #open cursor
    cursor = db.cursor()
    botname = name
    #use cursor
    cursor.execute(tgkey % (botname))
    results = cursor.fetchall()
    for row in results:
        token = row[2]
    keys = token.split('\n')
    #close cursor
    cursor.close()
    #close db
    db.close()
    return keys

# function to open url and run bs on source code
def get_web_content(url):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, "lxml")
    return soup

# run through source and identify bikes,
# find metadata from divs and load into
# various dictionaries
def find_bikes(url, existingLinks):
    # load page, find pages + store links
    soup = get_web_content(url)
    if "no ha obtenido resultados." in soup:
        pass
    else:
        pages = soup.findAll('a', {"data-xtclib":"parrillaVO_paginacion"})
        pagelinks=[]
        if not pages:
            pass
        else:
            count = 0
            for page in pages:
                count+=1
                if count <10:
                    pagelinks.append(page['href'])
                    if count == 9:
                        url = base_url + pagelinks[-1]
                        soup = get_web_content(url)
                        pages = soup.findAll('a',\
                        {"data-xtclib":"parrillaVO_paginacion"})
                        for page in pages:
                            if page in pagelinks:
                                pass
                            else:
                                pagelinks.append(page['href'])
                    else:
                        pass
        # scrape each page
        count = 0
        addedthisround = []
        if pagelinks:
            for link in pagelinks:
                url = base_url + link
                soup = get_web_content(url)
                src = soup.findAll('div' ,{"style":"position:relative"})
                for div in src:
                    bikeName = div.find('h2', {"class":"floatleft"})\
                    .text.replace(",","")
                    bikePhoto = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(div))
                    if len(str(bikePhoto)) < 68:
                        bikePhoto = str(bikePhoto)[2:-8]
                    else:
                        bikePhoto = str(bikePhoto)[2:-10]
                    bikePrice = div.find('p' ,{"class":"preu"})\
                    .text.replace(".","") #price
                    bikePrice = bikePrice[:-2]
                    if len(str(bikePrice)) < 2:
                        pass
                    else:
                        bikeMiles = div.find('span' ,{"class":"d1"})\
                        .text.replace(".","") #mileage
                        bikeYear = div.find('span' ,{"class":"d2"}).text #year
                        bikeLoc = div.find('span' ,{"class":"lloc"}).text #location
                        bikeLink = "http://motos.coches.net" + div\
                        .find('a')['href'] #link
                        bikePosted = div.find('p' ,{"class":"data floatright"})\
                        .text #posted
                        if str(bikePosted).upper == 'AHORA':
                            bikePosted = now
                        if "N/D" in str(bikeMiles):
                            bikeMiles = 0
                        bikeMiles = str(bikeMiles).replace("km","")
                        bikemeta = bikeYear, bikeName, bikeMiles, bikePrice
                        if bikeLink in existinglinks:
                            pass
                        else:
                            if bikeLink in addedthisround:
                                pass
                            else:
                                if len(str(bikePhoto)) < 10:
                                    pass
                                else:
                                    count+=1
                                    addedthisround.append(bikeLink)
                                    try:
                                        insertsql = insert.format(make,bikeName,\
                                        bikePrice,bikeMiles,bikeYear,bikeLoc,bikeLink,\
                                        bikePhoto,bikePosted,tbl)
                                        cursor.execute(insertsql)
                                        db.commit()
                                        bot.sendMessage('49248388','{0} {1} found in {2}:\
                                        {3}'.format(bikeYear,bikeName,bikeLoc,bikeLink),\
                                        disable_web_page_preview=True)
                                        bot.sendPhoto('49248388', bikePhoto,\
                                        caption='{0}€ | {1}km'.format(bikePrice,bikeMiles))
                                    except Exception as e:
                                        #send error message telegram
                                        print(e)
        else:
            bikedivs = soup.findAll('div' ,{"style":"position:relative"})
            for div in bikedivs:
                bikeName = div.find('h2', {"class":"floatleft"})\
                .text.replace(",","")
                bikePhoto = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(div))
                if len(str(bikePhoto)) < 68:
                    bikePhoto = str(bikePhoto)[2:-8]
                else:
                    bikePhoto = str(bikePhoto)[2:-10]
                bikePrice = div.find('p' ,{"class":"preu"})\
                .text.replace(".","") #price
                bikePrice = bikePrice[:-2]
                if len(str(bikePrice)) < 2:
                    pass
                else:
                    bikeMiles = div.find('span' ,{"class":"d1"})\
                    .text.replace(".","") #mileage
                    bikeYear = div.find('span' ,{"class":"d2"}).text #year
                    bikeLoc = div.find('span' ,{"class":"lloc"}).text #location
                    bikeLink = "http://motos.coches.net" + div\
                    .find('a')['href'] #link
                    bikePosted = div.find('p' ,{"class":"data floatright"})\
                    .text #posted
                    if str(bikePosted).upper == 'AHORA':
                        bikePosted = now
                    if "N/D" in str(bikeMiles):
                        bikeMiles = 0
                    bikeMiles = str(bikeMiles).replace("km","")
                    bikemeta = bikeYear, bikeName, bikeMiles, bikePrice
                    if bikeLink in existinglinks:
                        pass
                    else:
                        if bikeLink in addedthisround:
                            pass
                        else:
                            if len(str(bikePhoto)) < 10:
                                pass
                            else:
                                count+=1
                                addedthisround.append(bikeLink)
                                try:
                                    insertsql = insert.format(make,bikeName,\
                                    bikePrice,bikeMiles,bikeYear,bikeLoc,bikeLink,\
                                    bikePhoto,bikePosted,tbl)
                                    cursor.execute(insertsql)
                                    db.commit()
                                    bot.sendMessage('49248388','{0} {1} found in {2}:\
                                    {3}'.format(bikeYear,bikeName,bikeLoc,bikeLink),\
                                    disable_web_page_preview=True)
                                    bot.sendPhoto('49248388', bikePhoto,\
                                    caption='{0}€ | {1}km'.format(bikePrice,bikeMiles))
                                except Exception as e:
                                    #send error message telegram
                                    print(e)

# function to handle incoming messages for
# telegram bot application
def handle(msg):
        now = str(datetime.datetime.now())
        content_type, chat_type, chat_id = telepot.glance(msg)
        uname = msg['from']['first_name']
        msgtxt = msg['text']
        value = msgtxt[6::]
        usrid = msg['from']['id']
        msgid = msg['message_id']
        print("{0} | {1} | {2} | {3} | {4} | {5} | {6} ".format(now, usrid,\
        uname, content_type,chat_type, chat_id, msgtxt))
        while True:
            make = pref1[0]
            model = pref1[1]
            tbl = model
            model = model.replace(" ","%20")
            pricemax = pref1[2]
            yearmin = pref1[3]
            milesmax = pref1[4]
            loc = ''
            insert = "INSERT INTO bike_{9} VALUES (NULL, '{0}','{1}','{2}',\
            '{3}','{4}','{5}','{6}','{7}','{8}')"
            getbikes = "SELECT * FROM bike_{0}".format(tbl)
            find_bikes(url)

#assemble preferences into vars
def make_prefs(x):
    make = x[0]
    model = x[1]
    tbl = model
    model = model.replace(" ","%20")
    pricemax = x[2]
    yearmin = x[3]
    milesmax = x[4]
    loc = x[5]
    try:
        loc = options[loc.title()]
    except:
        loc = ""
    try:
        make = options[make.upper()]
    except:
        pass
    prefs = make,loc,model,milesmax,yearmin,pricemax
    return prefs, tbl

# get keys from db and start telegram
keys=get_auth('ncktbot')
bot = telepot.Bot(keys[0])
response = bot.getUpdates()

print('starting')

#set base URL of site to crawl
base_url = 'http://motos.coches.net/ocasion/default.aspx'

# open page to find dropdown options + load to dict
soup = get_web_content(base_url)
options = {}
for option in soup.find_all('option'):
    options[option.text] = option['value']

# set bike preferences
# format: make, model, maxprice, minyear, max miles, location
pref1 = ('ducati','monster','8000','2011','30000', '')
pref2 = ('husqvarna','nuda','8000','2011','30000', '')
pref3 = ('honda','cb','2000','','', 'barcelona')

preflist = [pref1, pref2, pref3]

while True:
    db=MySQLdb.connect(read_default_group='bikes')
    cursor = db.cursor()
    count = 0
    for x in preflist:
        prefs = make_prefs(x)
        make = prefs[0][0]
        tbl = prefs[1]
        url = base_url+"?MakeId={0}&ModelId=0&PrvId={1}&Version={2}&BodyTypeId=0&FuelTypeId=0&Section2=0&MaxKms={3}&MinKms=0&MaxYear=&MinYear={4}&MaxPrice={5}&SearchOrigin=2".format(*prefs[0])
        getbikes = "SELECT * FROM bike_{0}".format(prefs[1])
        insert = "INSERT INTO bike_{9} VALUES (NULL, '{0}','{1}','{2}',\
        '{3}','{4}','{5}','{6}','{7}','{8}')"
        try:
            cursor.execute(getbikes)
            existing = cursor.fetchall()
        except Exception as e:
            print(e)
        existinglinks = []
        if not existing:
            pass
        else:
            for row in existing:
                existinglinks.append(row[7])
        find_bikes(url, existinglinks)
        now = str(datetime.datetime.now())
        count += 1
        print('run{1} complete at {0}'.format(now, count))
    cursor.close()
    db.close()
    print('-----------------')
    time.sleep(60)
