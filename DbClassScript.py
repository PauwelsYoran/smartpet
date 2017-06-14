import time
class DbClass:
    def __init__(self):
        import mysql.connector as connector


        self.__dsn = {
            "host": "localhost",
            "user": "feedingScript",
            "passwd": "abc123",
            "db": "smartpet"
        }

        self.__connection = connector.connect(**self.__dsn)


    def getDataFromDatabase(self):
        self.__cursor = self.__connection.cursor()
        # Query zonder parameters
        sqlQuery = "SELECT * FROM tablename"

        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def getDataFromDatabaseMetVoorwaarde(self, voorwaarde):
        self.__cursor = self.__connection.cursor()
        # Query met parameters
        sqlQuery = "SELECT * FROM tablename WHERE columnname = '{param1}'"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(param1=voorwaarde)

        self.__cursor.execute(sqlCommand)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def setDataToDatabase(self, value1):
        self.__cursor = self.__connection.cursor()
        # Query met parameters
        sqlQuery = "INSERT INTO tablename (columnname) VALUES ('{param1}')"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(param1=value1)

        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        self.__cursor.close()

    def getPortionsize(self, weight_dog):
        self.__cursor = self.__connection.cursor()
        # Query met parameters
        sqlQuery = "SELECT p.portionsize,u.unit from dogweight_portionsize as dp join portieanalyse as p on p.ID = dp.portieanalyse_ID join unit as u on p.unit_id = u.ID WHERE '{param1}' BETWEEN min_weight_dog and max_weight_dog"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(param1=weight_dog)

        self.__cursor.execute(sqlCommand)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def getFeedingTimes(self):
        self.__cursor = self.__connection.cursor()
        # Query zonder parameters
        sqlQuery = "SELECT time FROM feeding_times"

        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result


    def getDog_info(self):
        self.__cursor = self.__connection.cursor()
        # Query zonder parameters
        sqlQuery = "SELECT name,weight,u.unit,age,birthday FROM dog_info join unit as u on u.ID = dog_info.unit_ID"

        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def getFood_eaten(self):
        self.__cursor = self.__connection.cursor()
        # Query zonder parameters
        sqlQuery = "SELECT portionsize,u.unit FROM food_eaten JOIN unit as u on u.ID= food_eaten.unit_id WHERE DATE(food_eaten.timestamp)= DATE(NOW())"

        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def getFood_eaten_graph(self, date):
        self.__cursor = self.__connection.cursor()
        # Query met parameters
        sqlQuery = "SELECT portionsize,u.unit,timestamp FROM food_eaten JOIN unit as u on u.ID= food_eaten.unit_id WHERE DATE(food_eaten.timestamp)= DATE('{param1}') order by TIMESTAMP "
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(param1=date)

        self.__cursor.execute(sqlCommand)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result
    def getFood_reservoir(self):
        self.__cursor = self.__connection.cursor()
        # Query zonder parameters
        sqlQuery = "SELECT weight, u.unit FROM food_reservoir join unit as u on u.ID = food_reservoir.unit_id ORDER by timestamp"

        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def getMax_portionsize(self):
        self.__cursor = self.__connection.cursor()
        # Query zonder parameters
        sqlQuery = "SELECT weight,u.unit FROM max_portionsize JOIN unit as u on u.ID= max_portionsize.unit_ID order by timestamp"

        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def getResting_portionsize(self):
        self.__cursor = self.__connection.cursor()
        # Query zonder parameters
        sqlQuery = "SELECT weight FROM resting_portionsize  ORDER BY timestamp"

        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def setDataToDog_info(self, name,weight,unit,age,birthday):
        self.__cursor = self.__connection.cursor()
        # Query met parameters
        sqlQuery = "INSERT INTO dog_info (name,weight,unit_ID,age,birthday) VALUES ('{param1}','{param2}','{param3}','{param4}','{param5}')"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(param1=name, param2 = weight, param3 = unit, param4= age, param5=birthday)

        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        self.__cursor.close()

    def setDataToFeeding_times(self, time):
        self.__cursor = self.__connection.cursor()
        # Query met parameters
        sqlQuery = "INSERT INTO feeding_times (time) VALUES ('{param1}')"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(param1=time)

        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        self.__cursor.close()


    def setDataToFood_eaten(self, portionsize, unit, ball_used):
        self.__cursor = self.__connection.cursor()
        # Query met parameters
        sqlQuery = "INSERT INTO food_eaten (portionsize,unit_id,ball_used) VALUES ('{param1}','{param2}','{param3}')"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(param1=portionsize, param2 =unit, param3= ball_used)

        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        self.__cursor.close()

    def setDataToFood_reservoir(self, weight, unit):
        self.__cursor = self.__connection.cursor()
        # Query met parameters
        sqlQuery = "INSERT INTO food_reservoir (weight, unit_id) VALUES ('{param1}','{param2}')"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(param1=weight, param2=unit, )

        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        self.__cursor.close()


    def setDataToMax_portionSize(self, weight, unit):
        self.__cursor = self.__connection.cursor()
        # Query met parameters
        sqlQuery = "INSERT INTO max_portionsize (weight, unit_id) VALUES ('{param1}','{param2}')"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(param1=weight, param2=unit, )

        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        self.__cursor.close()

    def setDataToResting_portionsize(self, weight, unit):
        self.__cursor = self.__connection.cursor()
        # Query met parameters
        sqlQuery = "INSERT INTO resting_portionsize (weight, unit_id) VALUES ('{param1}','{param2}')"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(param1=weight, param2=unit, )

        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        self.__cursor.close()

    def remove_feedingtime(self, time):
        self.__cursor = self.__connection.cursor()
        # Query met parameters
        sqlQuery = "delete from feeding_times WHERE time = '{param1}'"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(param1=time )

        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        self.__cursor.close()



