rm(list = ls())
library(shinydashboard)

ui <- dashboardPage(
  dashboardHeader(title = "WRC Dashboard"),
  dashboardSidebar(sidebarMenu(
      menuItem("Industry Water Reuse", tabName = "dashboard", icon = icon("dashboard")),
      menuItem("Community Rating Map", tabName = "widgets", icon = icon("th")),
      menuItem("Entity Behaviour", tabName = "rate", icon = icon("th")),
      menuItem("WRC tokens", tabName = "transaction", icon = icon("th"))
      )),
  dashboardBody(tabItems(
  tabItem(tabName = "dashboard", fluidRow(htmlOutput("frame"))
  ),
  tabItem(tabName = "widgets", sidebarLayout(
                  sidebarPanel(width = 4,
                    fluidRow(
                      column(12, dataTableOutput('dto'))
                      )),
                  mainPanel(fluidRow(htmlOutput("hframe"))
                  )
          )),
  tabItem(tabName = "rate", fluidRow(dataTableOutput('bto'))),
  tabItem(tabName = "transaction", fluidRow(dataTableOutput('tto')))
  )
  )
  )

server <- function(input, output) { 
observe({ 
    test <<- paste0("http://localhost:5000/map")
    map <<- paste0("http://localhost:5000/heatmap")  
})

values <- read.csv("templates/ward.csv", stringsAsFactors = FALSE)
behave <- read.csv("templates/behave.csv", stringsAsFactors = FALSE)
tokens <- read.csv("templates/token.csv", stringsAsFactors = FALSE)
output$frame <- renderUI({
    my_test <- tags$iframe(src=test, height=600, width=1130)
    print(my_test)
    my_test
  })

output$hframe <- renderUI({
    my_test <- tags$iframe(src=map, height=600, width=720)
    print(my_test)
    my_test
  })

output$dto <- renderDataTable(values, options = list(dom = 'ft'))
output$tto <- renderDataTable(tokens) 
output$bto <- renderDataTable(behave)
}
shinyApp(ui, server)
