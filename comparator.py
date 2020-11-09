# Importing required libraries
import requests
import webFunction as wf
import JSONFunction as jf
import config

class Temperature:

    def __init__(self, city, range):
        self.tcity = city
        self.vrange = range
        self.tunits = config.tunits

    def getDataFromAPI(self, city, units):
        """
        getDataFromAPI(): This function would construct the query string ,send data to API and then would get the data from weather API.
        >> A query will be generated for sending the request.
        >> Receive the response as per the request.
        >> In case of success function will return the data for further processing.

        @param
        string city
        string units

        @return
        Name of the requested city
        Temperature of the city in degree celsius.
        """

        postURL = config.apiURL + """?q=%s&units=%s&appid=%s""" % (city, units, config.apiKey)

        try:
            # In case of Success Response Code would be 200
            res = requests.get(postURL)

            # In case of error throw exceptions
            if res.status_code != 200:
                res.raise_for_status()
        except requests.exceptions.ConnectionError as err:
            print("Connection Error: %s" % err)

        except requests.exceptions.TooManyRedirects as err:
            print("Many Redirects Error :%s" % err)

        except requests.exceptions.HTTPError as err:
            print("HTTP Error: %s" % err)

        except requests.exceptions.RequestException as err:
            print("General Error observed is %s" % err)

        jsonResult = res.json()

        # Check whether required parameter exists in the response result or not
        if ('main' not in jsonResult) or (jsonResult['main'] == 0):
            raise KeyError('Data does not Exists')
        else:
            return (jsonResult['name'], jsonResult['main']['temp'])

    def getDataFromUI(self, city, units):

        try:

            temp = wf.get_temp_with_selenium(city,units)
            return city, temp

        except Exception as err:
            print("Error: %s" % err)

    def calculateVariance(self, dlist):
        """
            calculateVariance(): Function will calculate the variance of given list.
            >>Get the data as an input
            >>Find out the percent change between consecutive values in the list.

            @param
            list dlist

            @return
            list of variance
        """

        # percent change list
        pc = []

        try:
            # Print the variance of the data set
            for i in dlist[1:]:
                pc.append(((float(dlist[0] - i)) / abs(i)) * 100.00)

            return round(abs(pc[0]),2)

        except Exception as err:
            print("Error: %s" % err)

    def comparator(self):
        """
                comparator(): This function will matches the temperature information from the UI and API
                >> Fetch the temperature data from the UI.
                >> Fetch the temperature data from the API.
                >> Calculate the temperature variance.
                >> Find out whether the temperature difference is within a specified range or not.

                @param
                list dlist

                @return
                True or False
        """

        try:

            cityAPI, tempAPI = self.getDataFromAPI(self.tcity, self.tunits)
            cityWeb, tempWeb = self.getDataFromUI(self.tcity, self.tunits)

            if cityAPI == cityWeb:
                # Creating a temperature data set for variance
                tempList = [tempAPI, tempWeb]

                variance = self.calculateVariance(tempList)

                if variance < self.vrange:
                    print("Success: Temperature difference for %s is within a given variance range (variance is %s%%)"% (self.tcity,variance))
                    config.temp_output[self.tcity] = {"temp":{"API":tempAPI,"Web":tempWeb},"variance (in %)": variance}
                else:
                    raise Exception("Seems both sources for %s have different temperature with variance of %s%%" % (self.tcity, variance))


        except Exception as err:
            print("Error: %s" % err)


if __name__=="__main__":

    # get json input
    citydict = jf.get_input()

    for city in citydict["City"]:
        c = Temperature(city, citydict["Variance"])
        result = c.comparator()
        if result:
            print(result)

    jf.output_data()
