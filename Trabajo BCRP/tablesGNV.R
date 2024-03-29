library(readxl)
library(tidyverse)
library(formattable)
library(data.table)
library(writexl)
#install.packages('tidyverse')
#install.packages("writexl")

text_matrix <- function(dat, table_title) { 
  rbind(c(table_title, rep('', ncol(dat)-1)), 
        rep('', ncol(dat)), 
        names(dat),
        unname(sapply(dat, as.character)))}  
  
# 09/04/ Diesel 2 S-50 UV EN ATE

setwd("C:/Trabajo BCRP/Scripts/GNV/Data")
data<- read_excel("df_LimaGNV17-05.xlsx")
data <- data[,-1,drop=FALSE] #False para que siga siendo dataframe
names(data)[1]="Distrito"
names(data)[2]="Establecimiento"
names(data)[3]="Dirección"
names(data)[4]="Teléfono"
names(data)[5]="PRECIO"
names(data)[6]="Combustible"
names(data)
data<-data[!(data$`Distrito`=="Distrito"),] ###Lo de arriba solo son etiquetas, la columna sigue siendo 0
data[2,5] #character
data$`PRECIO`<-as.numeric(data$`PRECIO`) 
data[2,5]  ##Ahora ya es factor

prices<-data %>%# 
  group_by(Distrito) %>% 
  summarise(`Precio Promedio`=mean(PRECIO),`Número de Establecimientos`=n())%>%
  arrange(Distrito)%>%
  as.data.frame()

prices<-text_matrix(prices, table_title='Precios Promedio de venta en Lima por Distrito del GNV-17/05/2022 (Soles por metros cúbicos)')

write.table(prices, 'ConsolidadoGNV17-05.csv', row.names=F, col.names=F, sep=',')

#write_xlsx(prices, "D:/Git-Hub/Works/FACILITO-OSINERGMIN/DIARIO/Diesel/Datos/PROVINCIA LIMA/Consolidado07-04.xlsx")


######################
#####MUESTREO#########
#####################
write.table(data, 'Muestreo.csv', row.names=F, col.names=F, sep=',')

n<-13
set.seed(12)   
data_sample = data[sample(nrow(data), n, replace = T),]  
data_sample

mean(data$PRECIO)
mean(data_sample$PRECIO)
write.table(data_sample, 'MUESTRA_GNV.csv', row.names=F, col.names=F, sep=',')