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
from fake_useragent import UserAgent
from random import randint
from time import sleep


options = Options()
ua = UserAgent()
userAgent = ua.random
print(userAgent)
options.add_argument(f'user-agent={userAgent}') #user agent para reducir el riesgo de bloqueo de la página


DRIVER_PATH = 'C:/chromedriver.exe' 
driver = webdriver.Chrome(chrome_options=options, executable_path=DRIVER_PATH) #Options para el user agent
my_page = 'https://www.facilito.gob.pe/facilito/pages/facilito/buscadorAGranelGLP.jsp'
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


# //*[@id="contenido_listado"]/div[5]/div[2]/select[3]
# //*[@id="contenido_listado"]/div[5]/div[3]/table/tbody/tr[1]  
# //*[@id="contenido_listado"]/div[5]/div[3]/table/tbody/tr[2]

#Primero elijo el departamento, luego corro




"""for p in provincias:
    Select(driver.find_element_by_xpath('//*[@id="contenido_listado"]/div[5]/div[2]/select[2]')).select_by_visible_text(p)
    for i in lima..."""





general={'Titles':['Distrito', 'Establecimiento', 'Dirección', 'Teléfono', 'Precio de Venta\n(Soles por galón)', 'Unidad de Medida']}
general=pd.DataFrame(general).transpose()

before_XPath = '//*[@id="tblPreciosAGranelGlp"]/tbody/tr['
aftertd_XPath = "]/td["
aftertr_XPath = "]"

#//*[@id="tblPreciosAGranelGlp"]/tbody/tr[1]/th
Select(driver.find_element_by_xpath('//*[@id="tblPreciosAGranelGlp_length"]/label/select')).select_by_visible_text('50')
sleep(randint(1,2))
for x in range(2,11): ##ELEGIR 50
        rows2 = len(driver.find_elements_by_xpath('/html/body/form/main/section[2]/div/div[2]/div/div/table/tbody/tr')) # Contará una lista de cada tr incluyendo el título 
        columns2 = len(driver.find_elements_by_xpath('/html/body/form/main/section[2]/div/div[2]/div/div/table/tbody/tr[2]/td'))
        titles={'Titles':['Distrito', 'Establecimiento', 'Dirección', 'Teléfono', 'Precio de Venta\n(Soles por galón)', 'Unidad de Medida']}
        d2={}
        for t_row in range(1, (rows2 + 1)): #La primera fila es el título #rows +1, pues range no toma al último valor
            fila2='Linea{}'.format(t_row) ##Nuevamente cuento las filas
            d2[fila2]=[]
            Col1=driver.find_element_by_xpath('//*[@id="tblPreciosAGranelGlp"]/tbody/tr['+str(t_row)+ "]/th").text
            d2[fila2].append(Col1)
            for t_column in range(1, (columns2 + 1)):
                FinalXPath = before_XPath + str(t_row) + aftertd_XPath + str(t_column) + aftertr_XPath
                cell_text = driver.find_element_by_xpath(FinalXPath).text
                d2[fila2].append(cell_text) #Entramos a la lista (values) del diccionario
        titles.update(d2) 
        print(titles)
        try:
           driver.find_element_by_xpath("//*[@id='tblPreciosAGranelGlp_paginate']/span/*[contains(text(),'"+str(x)+"')]").click()
           print(x)
        except:
           print("No hay fila"+str(x))
        sleep(randint(1,2))
                   
        df= pd.DataFrame(data=titles).transpose()
        df['Combustible']='GLGranel'
        df['Provincia']='Lima'
        general=pd.concat([general, df])


general.to_excel('D:\\Git-Hub\\facilito\\Trabajo BCRP\\Scripts\\GLP Granel\\Data\\dfGLGranel_Lima19-08.xlsx', index = True)











##################################


general={'Titles':['Distrito', 'Establecimiento', 'Dirección', 'Teléfono', 'Precio de Venta\n(Soles por galón)', 'Unidad de Medida']}
general=pd.DataFrame(general).transpose()
for i in lima: 
    Select(driver.find_element_by_xpath('//*[@id="contenido_listado"]/div[5]/div[2]/select[3]')).select_by_visible_text(i)
    dict_productos_barranca={}
    sleep(randint(5,10))
    before_XPath = '//*[@id="contenido_listado"]/div[5]/div[3]/table/tbody/tr['
    aftertd_XPath = "]/td["
    aftertr_XPath = "]" # //*[@id="contenido_listado"]/div[5]/div[3]/table/tbody/tr[1]/th[1]
    rows = len(driver.find_elements_by_xpath('//*[@id="contenido_listado"]/div[5]/div[3]/table/tbody/tr'))
    columns = len(driver.find_elements_by_xpath('//*[@id="contenido_listado"]/div[5]/div[3]/table/tbody/tr[2]/td'))
   # print(rows,columns)
    titles={'Titles':['Distrito', 'Establecimiento', 'Dirección', 'Teléfono', 'Precio de Venta\n(Soles por galón)', 
                      'Unidad de Medida']}
    d={}
    for t_row in range(2, (rows + 1)): #La primera fila es el título #rows +1, pues range no toma al último valor
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
        driver.find_element_by_xpath('//*[@id="contenido_listado"]/div[5]/div[3]/div/a[2]').click()
        sleep(randint(5,10))
        rows2 = len(driver.find_elements_by_xpath('//*[@id="contenido_listado"]/div[5]/div[3]/table/tbody/tr')) # Contará una lista de cada tr incluyendo el título 
            #print(rows)
        columns2 = len(driver.find_elements_by_xpath('//*[@id="contenido_listado"]/div[5]/div[3]/table/tbody/tr[2]/td'))
        if rows2>1: ##Con esto evito que me ponga solo encabezados
            d2={}
            for t_row in range(2, (rows2 + 1)): #La primera fila es el título #rows +1, pues range no toma al último valor
                  # print('-----------')
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
                

    titles.update(d)  
    df= pd.DataFrame(data=titles).transpose()
    df['Combustible']='GLGranel'
    df['Distrito_ID']=i
    df['Provincia']='Lima'
    general=pd.concat([general, df])
        #print(df)
        
        #df.to_excel('D:\\Git-Hub\\Works\\FACILITO-OSINERGMIN\\DIARIO\\Diesel\\Datos\\PROVINCIA LIMA\\'+i+'\\df{}.xlsx'.format(j), index = True)
        #dict_productos_barranca[j]=df
    #dict_barranca=[i]=dict_productos_barranca

general.to_excel('C:\\Trabajo BCRP\\Scripts\\GLP Granel\\Data\\dfGLGranel_Lima28-04.xlsx', index = True)

