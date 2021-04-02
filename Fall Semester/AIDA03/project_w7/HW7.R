# Shiny App 
# Greece map HW7 - EDAV
# github: @tasosblackg

# Load libraries
library(shiny)
library(sf)
library(raster)
library(rgdal)
library(tmap)
library(ggplot2)
library(dplyr)
library(tidyr)
library(leaflet)
library(tidyr)
library(purrr)

# Read Raster data from previous HW 
# setwd('Desktop/edav_hw7')
greece <- raster('gr_elevation.tif')
nomoi <- st_read('data/GRC_ADM2/GRC_ADM2.shp')
poleis <- st_read('data/poleis/gr_poleisWGS84.shp')

# Add attributes
poleis$height <- raster::extract(greece,poleis,na.rm=TRUE)

nomoi$mean_height <- raster::extract(x=greece,y=nomoi,fun=mean,na.rm=TRUE)
nomoi$sd_height <- raster::extract(x=greece,y=nomoi,fun=sd,na.rm=TRUE)

plot(greece)



pal <- colorNumeric(c("#0C2C84", "#41B6C4", "#FFFFCC"), values(greece),
                    na.color = "transparent")




# Shiny App
ui <- fluidPage(titlePanel("Greece Map Reactive"),
                sliderInput(inputId = "sliderCH", "City Height", min = min(poleis$height), max = max(poleis$height), value = median(poleis$height)),
                sliderInput(inputId = "sliderRmH", "Region_mean_height", min = round(min(nomoi$mean_height),digits = 2), max = round(max(nomoi$mean_height),digits = 2), value = round(median(nomoi$mean_height),digits= 2) ),
                sliderInput(inputId = "sliderRsH", "Region_sd_height", min = round(min(nomoi$sd_height),digits = 2), max = round(max(nomoi$sd_height),digits = 2), value = round(median(nomoi$sd_height),digits = 2)),                
                leafletOutput("GreeceMap")
                
)

server <- function(input, output) {
  
  output$GreeceMap <- renderLeaflet({
    leaflet() %>% 
      addRasterImage(greece,colors=pal)%>%
      addLegend(pal = pal, values = values(greece),
                title = "Surface height")
  })
  
  observe({
    
    cityH <- input$sliderCH
    region_mean <- input$sliderRmH
    region_sd <- input$sliderRsH
    
    cities <- poleis %>% filter(height >= cityH)
    regions <- nomoi %>% filter(mean_height >= region_mean, sd_height >= region_sd)
 
    
    leafletProxy("GreeceMap") %>% clearMarkers() %>% 
      addPolygons(data = regions, 
                  fillOpacity = 0.3,
                  color = 'red',
                  stroke = T) %>%
      addCircleMarkers(data = cities,    fillColor = "goldenrod",
                       fillOpacity = 1,
                       stroke = F,label = poleis$NAME)
  })
  
}

shinyApp(ui, server)


#--------------------------------------------------------------
# Backup Test Code -- Comment Out --No Need
#--------------------------------------------------------------

# map <-leaflet(width=480,height=640)
# map <- addTiles(map)
# map


# poleis_lolan <- extract(poleis, geometry, into = c('Lat', 'Lon'), '\\((.*),(.*)\\)', conv = T)
# p <- poleis %>% filter(height >= 170)
# p
# n <- nomoi %>% filter(mean_height >= 150, sd_height>= 30
#                       )
# 
# leaflet() %>%
#   addTiles() %>% # a basemap; not required but nice...
#   addRasterImage(greece,colors=pal) %>%
#   addPolygons(data = nomoi, 
#               fillOpacity = 0.3,
#               color = 'red',
#               stroke = T) %>%
#   addCircleMarkers(data = poleis,    fillColor = "goldenrod",
#                    fillOpacity = 1,
#                    stroke = F,label = poleis$NAME)%>%
#   addLegend(pal = pal, values = values(greece),
#             title = "Surface height")