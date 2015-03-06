library(randomForest)
library(caret)

#############################
##  SET Working Directory  ##
#############################

#set this directory to a folder that contains SUBFOLDERS for each dataset
setwd("~/Documents/RPI Class Files/Spring 2015/Big Data Analytics/AutoML/Phase 1/datasets")

#get filenames of *train.data files in all subfolders
train.datasets = list.files(path = ".", pattern = "*train.data", include.dirs = FALSE, recursive = TRUE)

#get filenames of *train.solution files in all subfolders
solution.datasets = list.files(path = ".", pattern = "*train.solution", include.dirs = FALSE, recursive = TRUE)

#get filenames of *test.data files in all subfolders
test.datasets = list.files(path = ".", pattern = "*test.data", include.dirs = FALSE, recursive = TRUE)


#############################################################################
##   Enter 3 digit version number IN CONSOLE AFTER EXECUTING NEXT LINE:    ##
#############################################################################
#
#
#
version.number <- readline(prompt="Enter 3 digit version number in format XXX: ")


#create directory for version number. the version number should be removed from folder name when submitting
#version number is appened in code so that code does not overwrite previous results
dir.create(paste("./res_",version.number, sep = ''))


#for loop to create predictions for every dataset
for (i in 1:length(train.datasets))
{

  ## If you want to run this once without running on all datasets,
  ##  Uncomment the line below that assigns 'i' a value.
  ## Make sure to recomment it out when you run the entire program for all datasets
  
  #i = 2     #this (2) is the jasmine dataset
  
  train.data = read.table(train.datasets[i])
  train.data$solution = read.table(solution.datasets[i])
  test.data = read.table(test.datasets[i])
  
  ################################################
  ##     MODEL FITING AND CREATION FUNCTION     ##
  ##              STARTS HERE                   ##
  ################################################
  
  #Currently the prediction doesn't work so I (Anders) commented it out
  #I focused on making the code work on all datasets rather than working on the prediction
  #The error is due to the fact that train.data$solution is a list instead of a vector of integers
  
  set.seed(415)
  
  #rf.model = randomForest(as.factor(solution) ~ . , data = train.data)
  
  #predition = predict(rf.model, test.data)
  
  ########################################
  ##     MODEL FITING AND CREATION      ##
  ##              ENDS HERE             ##
  ########################################
  
  #dataset name without path or file extension for file writing purposes
  dataset.name = substr(test.datasets[i], 0, regexpr('/',test.datasets[i])[1]-1)
  
  #write files
  ##note: need to set prediction dataframe when prediction is working.  Currently set to just write the given solution
  write.csv(train.data$solution, file = paste("./res_",version.number,"/",dataset.name,"_test_",version.number,".predict", sep = ""))

} #end for loop

