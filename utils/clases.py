import json

class info_game:
    
    """
    Una clase hecha para tener toda la información de cada juego concreto
    
    """
    def __init__(self,soup,etiqueta,atributo):
        
        """Constructor donde defino la sopa de BS que necesito, la etiqueta y el atributo o atributos concretos

        Args:
            soup (list): La sopa de xml que recibo de la web
            etiqueta (string): la etiqueta que busco en cada scrapeo
            atributo (list): lista de diccionarios o listas que necesito para obtener cada detalle de cada juego
        """
        self.sopa = soup
        self.atribs = atributo
        self.etiq = etiqueta
    
    def caracteristica_tipo(self,mensaje_error,cal=False):
        """ 
        Metodo que nos devuelve la caracteristica concreta que queramos para cada juego
        
        Returns:
            caracarct(str): Devuelve la caracteristica concreta de cada tipo
        """
        if cal == True:
            calificacion_list = []
            for i in range(0,5):
                try:
                    calificacion_list.append(self.sopa.find(self.etiq, attrs=self.atribs[i]).get_text())
                except:
                    calificacion_list.append(mensaje_error)
                
            return calificacion_list
        else:
                      
            for indice, valor in enumerate(self.atribs):
                
                try:
                    caracarct = self.sopa.find(self.etiq, attrs=self.atribs[indice]).get_text()
                    break
                except AttributeError:
                    caracarct = mensaje_error        
        
            return caracarct
    
    def precios_y_otras_caracteristicas(self,mensaje_error): # Probando los diccionarios de los precios, mas preciso
        
        """
        Metodo que nos devuelve los precios
        En este caso self.atr es una lista de atributos para diferentes momentos.
        [0] atributos de  [1] atributos de la lista importante, [2] una lista de cada dirección concreta para cada precio.
        """
        
        try:
            dict_completo = self.sopa.find(self.etiq,attrs=self.atribs[0]).get_attribute_list(self.atribs[1])[0]
            conv_json = json.loads(dict_completo)
            if len(self.atribs[2]) == 3: 
                precio_o_caract = conv_json[self.atribs[2][0]][self.atribs[2][1]][self.atribs[2][2]]
                return precio_o_caract
            elif len(self.atribs[2]) == 5:
                precio_o_caract = conv_json[self.atribs[2][0]][self.atribs[2][1]][self.atribs[2][2]][self.atribs[2][3]][self.atribs[2][4]]
                return precio_o_caract
        
        except:
            precio_o_caract = mensaje_error
            return precio_o_caract
            
            
    
