class fridge:
    
    def __init__(self):
        import requests
        r = requests.get('http://freezer/ezt.html')
        self.text = r.text
        #Now find the index of the first instance of TEMPERATURE
        self.t_index = r.text.find('TEMPERATURE</td>')

    def get_set_temp(self):
        '''
        Parameters: none, it just accesses the fridge website
        Returns: float, Set point temperature of the fridge
        '''
        ST = float(self.text[self.t_index+51:self.t_index+55])
        return(ST)

    def get_fridge_temp(self):
        '''
        Parameters: none, it just accesses the fridge website
        Returns: float, Set point temperature of the fridge
        '''
        FT = float(self.text[self.t_index+29:self.t_index+33])
        return(FT)

    def get_product_temp(self):
        '''
        Parameters: none, it just accesses the fridge website
        Returns: float, Set point temperature of the fridge
        '''
        PT = float(self.text[self.t_index+106:self.t_index+110])
        return(PT)

    #fridge_temp = float(r.text[found+29:found+33])
    #set_temp = float(r.text[found+51:found+55])
    #product_temp = float(r.text[found+106:found+110])

f = fridge()
ST = f.get_set_temp()
FT = f.get_fridge_temp()
PT = f.get_product_temp()