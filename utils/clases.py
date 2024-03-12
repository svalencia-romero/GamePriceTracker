
class info_game:
    
    """
    Una clase hecha para tener toda la información de cada juego concreto
    
    """
    def __init__(self,soup,etiqueta,atributo):
        
        """Constructor donde defino la sopa de BS que necesito, la etiqueta y el atributo o atributos concretos

        Args:
            soup (list): La sopa de xml que recibo de la web
            etiqueta (string): la etiqueta que busco en cada scrapeo
            atributo (list): lista de diccionarios que necesito para obtener cada detalle de cada juego
        """
        self.sopa = soup
        self.atribs = atributo
        self.etiq = etiqueta
    
    def caracteristica_tipo(self,mensaje_concreto_error_df,cal=False):
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
                    calificacion_list.append(mensaje_concreto_error_df)
                
            return calificacion_list
        else:
                      
            for indice, valor in enumerate(self.atribs):
                
                try:
                    caracarct = self.sopa.find(self.etiq, attrs=self.atribs[indice]).get_text()
                    break
                except AttributeError:
                    caracarct = mensaje_concreto_error_df        
        
            return caracarct
    
    # def precios(self,mensaje_concreto_error,atribute_list): # Probando los diccionarios de los precios, mas preciso
    #     """
    #     Metodo que nos devuelve los precios
    #     """
    #     precio = self.sopa.find(self.etiq,attrs=self.atribs[indice]).get_attribute_list(atribute_list)[0]
    #  Dejo comentado, la idea es coger del mismo boton todos los precios y encajarlos en precio_0 precio_1 precio_2 preci3_