import requests, time

class fridge:
    
    def __init__(self, url = 'http://freezer/ezt.html'):
        self.url = url
        self.update()

    def update(self):
        r = requests.get(self.url)
        self.text = r.text
        #Now find the index of the first instance of TEMPERATURE
        self.t_index = r.text.find('TEMPERATURE</td>')

    def get_set_temp(self):
        '''
        Parameters: none, it just accesses the fridge website
        Returns: float, Set point temperature of the fridge
        '''
        print(self.t_index)
        if self.isfloat(self.text[round(self.t_index+51):round(self.t_index+55)]):
            ST = float(self.text[round(self.t_index+51):round(self.t_index+55)])
        elif self.isfloat(self.text[round(self.t_index+50):round(self.t_index+53)]):
            ST = float(self.text[round(self.t_index+50):round(self.t_index+53)])
        else:
            ST = -999
        return(ST)

    def get_fridge_temp(self):
        '''
        Parameters: none, it just accesses the fridge website
        Returns: float, Set point temperature of the fridge
        '''
        if self.isfloat(self.text[round(self.t_index+29):round(self.t_index+33)]):
            FT = float(self.text[round(self.t_index+29):round(self.t_index+33)])
        elif self.isfloat(self.text[round(self.t_index+28):round(self.t_index+32)]): 
            FT = float(self.text[round(self.t_index+28):round(self.t_index+32)])
        else:
            FT = -999
        return(FT)

    def get_product_temp(self):
        '''
        Parameters: none, it just accesses the fridge website
        Returns: float, Set point temperature of the fridge
        '''
        if self.isfloat(self.text[self.t_index+106:self.t_index+110]):
            PT = float(self.text[self.t_index+106:self.t_index+110])
        elif self.isfloat(self.text[self.t_index+104:self.t_index+107]):
            PT = float(self.text[self.t_index+104:self.t_index+107])
        elif self.isfloat(self.text[self.t_index+108:self.t_index+112]):
            PT = float(self.text[self.t_index+108:self.t_index+112])
        else:
            PT = -999
        return(PT)

    def isfloat(self, num):
        try:
            float(num)
            return True
        except ValueError:
            return False
    #fridge_temp = float(r.text[found+29:found+33])
    #set_temp = float(r.text[found+51:found+55])
    #product_temp = float(r.text[found+106:found+110])

if __name__ == "__main__":

    f = fridge()
    
    while True:
        f.update()

        print("Set point: {st}, fridge temp.: {ft}, product temp.: {pt}".format(
            st = f.get_set_temp(), ft = f.get_fridge_temp(), pt = f.get_product_temp()
        ))
        
        time.sleep(1)
