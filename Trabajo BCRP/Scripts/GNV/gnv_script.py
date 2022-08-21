# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 20:54:47 2022

@author: Usuario
"""

########DIESEL############

from bs4 import BeautifulSoup ###No usaremos, es una página dinámica (tiene java script// .do)
import requests
import selenium
from selenium import webdriver
from selenium.webdriver.support.select import Select
import pandas as pd
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent #pip install fake-useragent
from random import randint
from time import sleep
from selenium.webdriver.common.by import By

options = Options()
ua = UserAgent()
userAgent = ua.random
print(userAgent)
options.add_argument(f'user-agent={userAgent}')


DRIVER_PATH = 'C:/chromedriver.exe' 
driver = webdriver.Chrome(chrome_options=options, executable_path=DRIVER_PATH)
my_page = 'https://www.facilito.gob.pe/facilito/pages/facilito/buscadorGNV.jsp'

driver.get(my_page)
sleep(randint(5,10))
driver.find_element_by_xpath("/html/body/main/section[2]/div[1]/div/map/area[14]").click() ###FULLLL XPATH

#####FUNCIONES############
#1.Función que extrae todas las opciones por el nombre del nodo ('distrito', 'provincia', 'departamentoAux', 'producto...)

####EXTRAEMOS DISTRITOS PARA CADA PROVINCIA (ELIJO MANUALMENTE CADA PROVINCIA)#####
#Voy extrayendo los distritos y los copio de la consola a la lista

lima=['ANCON', 'ATE', 'BARRANCO', 'BREÑA', 'CARABAYLLO', 'CHACLACAYO', 
       'CHORRILLOS', 'CIENEGUILLA', 'COMAS', 'EL AGUSTINO', 'INDEPENDENCIA', 'JESUS MARIA', 
       'LA MOLINA', 'LA VICTORIA', 'LIMA', 'LINCE', 'LOS OLIVOS', 'LURIGANCHO', 'LURIN', 
       'MAGDALENA DEL MAR', 'MIRAFLORES', 'PACHACAMAC', 'PUCUSANA', 'PUEBLO LIBRE', 'PUENTE PIEDRA',
       'PUNTA HERMOSA', 'PUNTA NEGRA', 'RIMAC', 'SAN BARTOLO', 'SAN BORJA', 'SAN ISIDRO', 
       'SAN JUAN DE LURIGANCHO', 'SAN JUAN DE MIRAFLORES', 'SAN LUIS', 'SAN MARTIN DE PORRES', 
       'SAN MIGUEL', 'SANTA ANITA', 'SANTA MARIA DEL MAR', 'SANTA ROSA', 'SANTIAGO DE SURCO', 
       'SURQUILLO', 'VILLA EL SALVADOR', 'VILLA MARIA DEL TRIUNFO']


#//*[@id="contenido_listado"]/div[5]/div[1]/select[3] 
#//*[@id="contenido_listado"]/div[5]/div[1]/select[4]
#//*[@id="contenido_listado"]/div[5]/div[2]/table/tbody/tr[2]/td[1] 
# //*[@id="contenido_listado"]/div[5]/div[3]/table/tbody/tr/th[1]
#Primero elijo el departamento, luego corro

"""for p in provincias:
    Select(driver.find_element_by_xpath('//*[@id="contenido_listado"]/div[5]/div[2]/select[2]')).select_by_visible_text(p)
    for i in lima..."""

#//*[@id="tblPreciosGnv"]/tbody
#/html/body/form/main/section[2]/div/div[2]/div/div/table
# #tblPreciosGnv_paginate > span > a.paginate_button.current
driver.find_elements(by=By.XPATH, value='//*[@id="tblPreciosGnv_paginate"]/span/*[contains(text(),"6")]').click()

                   
                   
driver.find_element_by_xpath("//*[@id='tblPreciosGnv_paginate']/span/*[contains(text(),'6')]").click()

                   

#//*[@id="tblPreciosGnv_paginate"]/span/a[4] 

# //*[@id="tblPreciosGnv_paginate"]/span/a[5]
# //*[@id="tblPreciosGnv_paginate"]/span/a[4]
# /html/body/form/main/section[2]/div/div[2]/div/div/div[4]/span/a[4]
# /html/body/form/main/section[2]/div/div[2]/div/div/div[4]/span/a[2]

#/html/body/form/main/section[2]/div/div[2]/div/div/table/thead/tr/th[1] 

general={'Titles':['Distrito', 'Establecimiento', 'Dirección', 'Teléfono', 'Precio de Venta\n(Soles por métros cúbicos)']}
general=pd.DataFrame(general).transpose()

before_XPath = '//*[@id="tblPreciosGnv"]/tbody/tr['
aftertd_XPath = "]/td["
aftertr_XPath = "]"


#####PASAR DE PÁGINA 


# //*[@id="tblPreciosGnv"]/tbody/tr[1]/td[1]

# //*[@id="tblPreciosGnv"]/tbody/tr[1]/th
# //*[@id="tblPreciosGnv"]/tbody/tr[2]/th
# //*[@id="tblPreciosGnv"]/tbody/tr[1]/td[1]
# //*[@id="tblPreciosGnv"]/tbody/tr[1]/td[2] 
# //*[@id="tblPreciosGnv"]/tbody/tr[1]/td[4]/strong/div 

for i in range (2,4):
    print(i)
    
#//*[@id="tblPreciosGnv_paginate"]/span/a[4] 
#//*[@id="tblPreciosGnv_paginate"]/span/a[2] 
Select(driver.find_element_by_xpath('//*[@id="tblPreciosGnv_length"]/label/select')).select_by_visible_text('50')

for x in range(2,8):#range no toma el último valor
        rows2 = len(driver.find_elements_by_xpath('/html/body/form/main/section[2]/div/div[2]/div/div/table/tbody/tr')) # Contará una lista de cada tr incluyendo el título 
        columns2 = len(driver.find_elements_by_xpath('/html/body/form/main/section[2]/div/div[2]/div/div/table/tbody/tr[2]/td'))
        titles={'Titles':['Distrito', 'Establecimiento', 'Dirección', 'Teléfono', 'Precio de Venta\n(Soles por métros cúbicos)']}
        d2={}
        for t_row in range(1, (rows2 + 1)): 
            fila2='Linea{}'.format(t_row) ##Nuevamente cuento las filas
            d2[fila2]=[]
            Col1=driver.find_element_by_xpath('//*[@id="tblPreciosGnv"]/tbody/tr['+str(t_row)+ "]/th").text
            d2[fila2].append(Col1)
            for t_column in range(1, (columns2 + 1)):
                FinalXPath = before_XPath + str(t_row) + aftertd_XPath + str(t_column) + aftertr_XPath
                cell_text = driver.find_element_by_xpath(FinalXPath).text
                d2[fila2].append(cell_text) #Entramos a la lista (values) del diccionario
        titles.update(d2) 
        print(titles)
        try:
           driver.find_element_by_xpath("//*[@id='tblPreciosGnv_paginate']/span/*[contains(text(),'"+str(x)+"')]").click()
           print(x)
        except:
           print("No hay fila"+str(x))
        #driver.find_element_by_xpath('//*[@id="contenido_listado"]/div[5]/div[2]/div/a[2]').click()
        sleep(randint(2,3))
            # Cuando abra la misma ventana, tenemos que verificar que no repitan los datos:        
        df= pd.DataFrame(data=titles).transpose()
        df['Combustible']='GNV'
        df['Provincia']='Lima'
        general=pd.concat([general, df])



general.to_excel('D:\\Git-Hub\\facilito\\Trabajo BCRP\\Scripts\\GNV\\Data\\df_LimaGNV19-08.xlsx', index = True)









general={'Titles':['Distrito', 'Establecimiento', 'Dirección', 'Teléfono', 'Precio de Venta\n(Soles por galón)']}
general=pd.DataFrame(general).transpose()
for i in lima:
    Select(driver.find_element_by_xpath('//*[@id="contenido_listado"]/div[5]/div[1]/select[3]')).select_by_visible_text(i)
    sleep(randint(5,10))
    before_XPath = '//*[@id="contenido_listado"]/div[5]/div[2]/table/tbody/tr['
    aftertd_XPath = "]/td["
    aftertr_XPath = "]"
    rows = len(driver.find_elements_by_xpath('//*[@id="contenido_listado"]/div[5]/div[2]/table/tbody/tr'))
    columns = len(driver.find_elements_by_xpath('//*[@id="contenido_listado"]/div[5]/div[2]/table/tbody/tr[2]/td'))
    #print(rows,columns)
    titles={'Titles':['Distrito', 'Establecimiento', 'Dirección', 'Teléfono', 'Precio de Venta\n(Soles por galón)']}
    d={}
    for t_row in range(1, (rows + 1)): 
        fila='Linea{}'.format(t_row)
        d[fila]=[]
               #print(fila)
               #print('-----------')
        for t_column in range(1, (columns + 1)):
            FinalXPath = before_XPath + str(t_row) + aftertd_XPath + str(t_column) + aftertr_XPath
            cell_text = driver.find_element_by_xpath(FinalXPath).text
            d[fila].append(cell_text) #Entramos a la lista (values) del diccionario
           # print(cell_text)
     
    titles.update(d)        
    for x in range(1,4):
        driver.find_element_by_xpath('//*[@id="contenido_listado"]/div[5]/div[2]/div/a[2]').click()
        sleep(randint(1,10))
        rows2 = len(driver.find_elements_by_xpath('//*[@id="contenido_listado"]/div[5]/div[2]/table/tbody/tr')) # Contará una lista de cada tr incluyendo el título 
        columns2 = len(driver.find_elements_by_xpath('//*[@id="contenido_listado"]/div[5]/div[2]/table/tbody/tr[2]/td'))
        if rows2>1: ##Con esto evito que me ponga solo encabezados
            d2={}
            for t_row in range(1, (rows2 + 1)): 
                fila2='Linea{}'.format(rows+t_row) ##Nuevamente cuento las filas
                d2[fila2]=[]
                for t_column in range(1, (columns2 + 1)):
                    FinalXPath = before_XPath + str(t_row) + aftertd_XPath + str(t_column) + aftertr_XPath
                    cell_text = driver.find_element_by_xpath(FinalXPath).text
                    d2[fila2].append(cell_text) #Entramos a la lista (values) del diccionario
            # Cuando abra la misma ventana, tenemos que verificar que no repitan los datos:        
            if d2[fila2] not in titles.values():    #Esta fila (línea) descartará a los diccionarios repetidos
                print("Esta fila no está en el titles (el diccionario mayor). Se unirá todo el diccionario")
                titles.update(d2) 
            else:
                print('Esta tabla ya está en titles (el diccionario mayor). No se unirá nada')
    df= pd.DataFrame(data=titles).transpose()
    df['Combustible']='GNV'
    df['Distrito_ID']=i
    df['Provincia']='Lima'
    general=pd.concat([general, df])
        #print(df)
        
        #df.to_excel('D:\\Git-Hub\\Works\\FACILITO-OSINERGMIN\\DIARIO\\Diesel\\Datos\\PROVINCIA LIMA\\'+i+'\\df{}.xlsx'.format(j), index = True)
        #dict_productos_barranca[j]=df
    #dict_barranca=[i]=dict_productos_barranca

general.to_excel('D:\\Git-Hub\\facilito\\Trabajo BCRP\\Scripts\\GNV\\Data\\df_LimaGNV12-07.xlsx', index = True)


