from tkinter import *
import requests
import shutil
from requests import Request, Session
import json
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

try:
    # Python2
    import Tkinter as tk
    from urllib2 import urlopen
except ImportError:
    # Python3
    import tkinter as tk
    from urllib.request import urlopen

# Setting API
url = 'https://api.coingecko.com/api/v3/coins/markets'
parameters = {
    'vs_currency': 'usd',
    'ids': 'bitcoin,ethereum,dogecoin,ripple'
}
headers = {
    'Accepts': 'application/json',
}

session = Session()
session.headers.update(headers)


# Initializing Coinmarket Class

class coinmarket:
    def __init__(self, ctr=0, coinname="blank", coinprice="blank",change24ho = 0.00):
        try:
            # Grabs API Response by parsing URL and parameters
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
            i = 0
            # Goes through each coin parsed
            while i < len(data):
                # Prints Name of Coin
                print(data[i]['name'])
                # Sets URL of Coin Image
                imgurl = data[i]['image']
                # Uses Image URL to Grab png file
                r = requests.get(imgurl, stream=True)
                if r.status_code == 200:
                    with open(".\coinimg\\" + str(data[i]['id'] + ".png"), 'wb') as f:
                        r.raw.decode_content = True
                        shutil.copyfileobj(r.raw, f)
                # Sets Coin name and Coin Price Variables
                # self._coinprice = data[0]['current_price']
                self._coinname = data[0]["name"]
                coinprice = data[0]['current_price']
                i += 1
        # Prints error if unable to parse parameters
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)
        self._ctr = ctr
        self._coinprice = coinprice

    def set_coinname(self, coinname):
        self._coinname = coinname

    def get_coinname(self):
        return self._coinname

    def set_coinprice(self, coinprice):
        self._coinprice = coinprice

    def get_coinprice(self):
        return self._coinprice

    def set_ctr(self, ctr):
        self._ctr = ctr

    def get_ctr(self):
        return self._ctr


# Attempting to use event to change coin information
def changecoin():
    ctr = 1
    response = session.get(url, params=parameters)
    data = json.loads(response.text)

    coinnamew.config(text=data[ctr]["name"])
    coinprice = data[ctr]['current_price']
    if (ctr < len(data)):
        ctr += 1
    else:
        ctr = 0
    print(ctr)

def autoloop(root, cls, name, img, price):
    try:

        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        i = cls.get_ctr()
        i += 1
        print(i)
        if (i < len(data)):
            cls.set_ctr(i)
        else:
            cls.set_ctr(0)
            i = 0
        cls.set_coinname(data[i]['name'])
        cls.set_coinprice(data[i]['current_price'])
        coinid = data[i]["id"]
        print(cls.get_coinprice())
        print(cls.get_coinname())
        coinimage = PhotoImage(file='.\coinimg\\' + coinid + ".png")
        name.config(text=cls.get_coinname())
        img.config(image=coinimage)
        img.image = coinimage
        price.config(text=cls.get_coinprice())

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
    root.after(10000, autoloop, root, cls, name, img, price)

def refreshprice(cls, name, img, price):
    try:

        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        i = cls.get_ctr()
        i += 1
        print(i)
        if (i < len(data)):
            cls.set_ctr(i)
        else:
            cls.set_ctr(0)
            i = 0
        cls.set_coinname(data[i]['name'])
        cls.set_coinprice(data[i]['current_price'])
        coinid = data[i]["id"]
        print(cls.get_coinprice())
        print(cls.get_coinname())
        coinimage = PhotoImage(file='.\coinimg\\' + coinid + ".png")
        name.config(text=cls.get_coinname())
        img.config(image=coinimage)
        img.image = coinimage
        price.config(text=cls.get_coinprice())

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)



# Main window for tkinter
def main():
    window = Tk()
    ##Creates the window from the imported Tkinter module
    window.geometry("800x700")
    ##Creates the size of the window
    window.title("Crypto Coin Tracker")
    test = coinmarket()

    # Creates Labels and Image for tkinter GUI calling the values from the initializer
    coinnamew = tk.Label(text=test.get_coinname())
    coinnamew.pack()
    img = PhotoImage(file='.\coinimg\\'  + test.get_coinname() + ".png")
    w1 = tk.Label(window, image=img)
    w1.pack()
    w1.bind("<Button-1>", lambda x: refreshprice(test, coinnamew, w1, coinpricew))
    coinpricew = tk.Label(text=test.get_coinprice())
    coinpricew.pack()
    nextcoin = tk.Button(text="Next Coin", command=lambda: refreshprice(test, coinnamew, w1, coinpricew)).pack()
    autoloop(window, test, coinnamew, w1, coinpricew)
    window.mainloop()



##Loops the window to prevent the window from just "flashing once"
if __name__ == "__main__": main()
