df = read.csv("Output.csv",sep=',')

u = unique(df[,c("NumericalLocation.Row.", "NumericalLocation.Col.")])
locationX = c()
locationY = c()
means = c()
counts = c()

i <- 1
for(r in 1:nrow(u)){
  selection <- df[df$NumericalLocation.Row. == u[r,1] & df$NumericalLocation.Col. == u[r,2],]
  count = nrow(selection[selection$Area != 0,])
  mean = mean(selection[selection$Area != 0,]$Area)
  
  locationX[i] =  u[r,1]
  locationY[i] = u[r,2]
  means[i]= mean
  counts[i]= count
  i <- i + 1
}

of <- data.frame(xLoc = locationX, yLoc = locationY, avg = means, qual = counts)

write.csv(of, file = "Data_QC.csv")
  