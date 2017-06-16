from flask import Flask
from flask import render_template
from flask import request
import time
import datetime

app = Flask(__name__)


@app.route('/')
def Home():
    from DbClass import DbClass
    db = DbClass()

    #get's the all the food that has been eaten from the courrent day and counts it
    food_eaten = db.getFood_eaten()
    food_size=0
    for value in food_eaten:
        if value[1] =='kg':
            weight = float(value[0] *1000)
        else:
            weight=float(value[0])
        food_size=weight+food_size

    if food_size > 1000:
        food_size=float(food_size/1000)
        food_eaten = [food_size,'kg']
    else:
        food_eaten = [food_size, 'g']

    #get"s the dog naam

    naam= db.getDog_info()
    naam=naam[-1]

    #gets how many food is in the reservoir, will be last beaacause it is ordered by the timestamp
    food_reservoir = db.getFood_reservoir()
    food_reservoir = food_reservoir[-1]


    return render_template('index.html',eaten=food_eaten,naam=naam, reservoir = food_reservoir)

@app.route('/manualFeed' ,methods=['GET','POST'])
def manualFeed():
    from DbClass import DbClass
    from a4988 import a4988
    from HX711 import HX711
    db = DbClass()
    mot=a4988()

    # 2 declarations ofr the 2 different scale's, hx_res is the reservoir scale
    hx=HX711(20,21)
    hx_res = HX711(23,24)

    #gets the dog's name
    naam= db.getDog_info()
    naam=naam[-1]


    #catxhes the form info
    portion = request.form["portionsize"]
    unit = request.form["unit"]

    #make's sure the portion is in grams
    if unit=='g':
        #in my case, 1 turn = +/- 25 g
        turn=int(int(portion)/20)
    else:
        turn=int((int(portion)*1000)/20)
        portion = int(portion)*1000





    #starts up the scale
    hx.set_reading_format("LSB", "MSB")
    hx.set_reference_unit(2167)
    hx.reset()
    hx.tare()

    #turns the motor
    for i in range(0,turn):
        mot.turn_motor()

    #gets the weight and put the resluts in a list
    list_weight=[]
    for i in range(0,10):
        val = max(0, int(hx.get_weight(5)))
        print(val)
        hx.power_down()
        hx.power_up()
        list_weight.append(int(val))
        time.sleep(0.5)

    #the list gets sorted so hightest value would be last
    weight=sorted(list_weight)
    portion_weight= int(weight[-1])

    #insert how much food is eaten in to to food_eaten tabe
    if portion_weight > 1000 :
        portion_Data= float(portion_weight/1000)
        db.setDataToFood_eaten(portion_Data,2,0)
    else:
        db.setDataToFood_eaten(portion_weight,1,0)


    ##################################################

    #starts up the reservoir scale
    hx_res.set_reading_format("LSB", "MSB")
    hx_res.set_reference_unit(393.35)
    hx_res.reset()

    # gets the weight and put the resluts in a list
    list_weight = []
    for i in range(0, 10):
        val = max(0, int(hx_res.get_weight(5)))
        print(val)
        hx_res.power_down()
        hx_res.power_up()
        list_weight.append(int(val))
        time.sleep(0.5)

    #calculate how much food is left
    weight = (list_weight)
    portion_weight = int(weight[-1])
    print(portion_weight)
    portion_weight=portion_weight-22954 #can only be done when de reference unit is positive
    print('portie:' + str(portion_weight))

    #inserts how much food is leftt in de Food reservoir tale
    if portion_weight > 1000:
        portion_Data = float(portion_weight / 1000)
        print('data' + str(portion_Data))
        db.setDataToFood_reservoir(portion_Data, 2)
    elif portion_weight < 0:
        portion_weight= 0
        db.setDataToFood_reservoir(portion_weight, 1)
    else: db.setDataToFood_reservoir(portion_weight, 1)



    #gets how much food is in teh reservoir
    food_reservoir = db.getFood_reservoir()
    food_reservoir = food_reservoir[-1]

    #get hw-ow much food is eaten today and calculate's it
    food_eaten = db.getFood_eaten()
    food_size = 0
    for value in food_eaten:
        if value[1] == 'kg':
            weight = float(value[0] * 1000)
        else:
            weight = float(value[0])
        food_size = weight + food_size

    if food_size > 1000:
        food_size = float(food_size / 1000)
        food_eaten = [food_size, 'kg']
    else:
        food_eaten = [food_size, 'g']

    return render_template('index.html',eaten=food_eaten,naam=naam, reservoir = food_reservoir)

@app.route('/settings')
def Settings():
    from DbClass import DbClass
    db = DbClass()

    #get's all the dog's info
    dog_info=db.getDog_info()
    dog_info=dog_info[-1]

    #gets the current max portionsize
    max_portionsize = db.getMax_portionsize()
    max_portionsize=max_portionsize[-1]
    cur_max_portionsize = max_portionsize[0]
    unit_max = max_portionsize[1]
    print(unit_max)

    #get th dogs weight ot calculate how much foo is recommended
    weight=dog_info[1]
    portionsize = db.getPortionsize(weight)
    portionsize = portionsize[0]

    rest = db.getResting_portionsize()
    rest=rest[-1]
    weight = rest[0]

    return render_template('settings.html',recommended = portionsize,dog_info=dog_info,max_portionsize=cur_max_portionsize, unit_max=unit_max, rest=weight)




@app.route('/addInfo',methods=['GET','POST'])
def addData():
    from DbClass import DbClass
    db = DbClass()

    #catches the form's data and adds it to the dog_info table
    name=request.form["name"]
    weight = request.form["weight"]
    unit = request.form["unit"]
    if unit == 'kg':
        unit=2
    else:
        unit=1
    age= request.form["age"]
    birthday=request.form["birthday"]

    db.setDataToDog_info(name,weight,unit,age,birthday)

    #gets the dog info
    dog_info = db.getDog_info()
    dog_info = dog_info[-1]

    #gets the current max portionsize
    max_portionsize = db.getMax_portionsize()
    max_portionsize = max_portionsize[-1]
    cur_max_portionsize=max_portionsize[0]
    unit_max = max_portionsize[1]


    # get th dogs weight ot calculate how much foo is recommended
    weight = dog_info[1]
    portionsize = db.getPortionsize(weight)
    portionsize = portionsize[0]

    rest = db.getResting_portionsize()
    rest = rest[-1]
    weight = rest[0]

    return render_template('settings.html',recommended=portionsize,dog_info=dog_info,max_portionsize=cur_max_portionsize,unit_max=unit_max,rest = weight)


@app.route('/time')
def feedTimes():
    from DbClass import DbClass
    db = DbClass()
    #gets all the feeding times and orders them
    timelist = db.getFeedingTimes()
    timelist= sorted(timelist)

    return render_template('feeding_times.html',timelist=timelist, count = 0)

@app.route('/time/newtime')
def newTimes():
    #opens the new time page

    return render_template('add_time.html',)

@app.route('/addTime',methods=['GET','POST'])
def addTime():
    from DbClass import DbClass
    db = DbClass()

    #cathces the form data and adds it to the
    time=request.form["time"]
    db.setDataToFeeding_times(time)

    timelist = db.getFeedingTimes()
    timelist = sorted(timelist)
    return render_template('feeding_times.html',timelist=timelist, count = 0)

@app.route('/removeTime',methods=['GET','POST'])
def removeTime():
    from DbClass import DbClass
    db = DbClass()

    time = request.form["time"]

    db.remove_feedingtime(str(time))
    timelist = db.getFeedingTimes()
    timelist = sorted(timelist)
    return render_template('feeding_times.html',timelist=timelist, count = 0)

@app.route('/addPortion',methods=['GET','POST'])
def addPortion():
    from DbClass import DbClass
    db = DbClass()

    #catches the form data and adds it to the max portionsize table
    portion = request.form["portion"]
    unit = request.form["unit"]
    if unit == 'kg':
        unit=2
    else:
        unit=1
        print(float(portion))
    db.setDataToMax_portionSize(float(portion),int(unit))

    #gets the dog's info
    dog_info = db.getDog_info()
    dog_info = dog_info[-1]

    #gets the max_portiinsize
    max_portionsize = db.getMax_portionsize()
    max_portionsize = max_portionsize[-1]
    cur_max_portionsize = max_portionsize[0]
    unit_max = max_portionsize[1]

    weight = dog_info[1]
    portionsize = db.getPortionsize(weight)
    portionsize = portionsize[0]

    rest = db.getResting_portionsize()
    rest = rest[-1]
    weight = rest[0]

    return render_template('settings.html',recommended=portionsize,dog_info=dog_info,max_portionsize=cur_max_portionsize, unit=unit_max,rest=weight)

@app.route('/history')
def history():
    from DbClass import DbClass
    import datetime
    db = DbClass()
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    food_eaten = db.getFood_eaten_graph(str(date))

    data_list = []
    for i in food_eaten:
        temp_list = []
        if i[1] == 'kg':
            food = int(i[0] * 1000)
        else:
            food = int(i[0])
        time = i[2].strftime('%H:%M:%S')
        temp_list.append(time)
        temp_list.append(food)
        data_list.append(temp_list)

    if data_list == []:
        data_list=[['no food has bean eaten',0]]
    print(data_list)

    return render_template('history.html',data_list=data_list,date = date)


@app.route('/changeDate',methods=['GET','POST'])
def changeDate():
    from DbClass import DbClass

    db = DbClass()
    date = request.form["date"]
    food_eaten = db.getFood_eaten_graph(str(date))


    data_list = []
    for i in food_eaten:
        temp_list = []
        if i[1] == 'kg':
            food = int(i[0] * 1000)
        else:
            food = int(i[0])
        time = i[2].strftime('%H:%M:%S')
        temp_list.append(time)
        temp_list.append(food)
        data_list.append(temp_list)

    if data_list == []:
        data_list = [['no food has been eaten', 0]]
    print(data_list)

    return render_template('history.html',data_list=data_list,date = date)




if __name__ == '__main__':
        import os
        port = int(os.environ.get("PORT",8080))
        host='0.0.0.0'
        app.run(host=host, port = port, debug = True)

