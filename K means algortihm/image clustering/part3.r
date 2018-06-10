library(jpeg)
library(ggplot2)
install.packages("jpg")

for (i in 1:3) {
  

  path <- paste("http://www.utdallas.edu/~axn112530/cs6375/unsupervised/images/image",i,".jpg",sep = "")
  download.file(path,"Image.jpg",mode = 'wb')
  img <- readJPEG("Image.jpg")
  
  # Obtain the dimension
  imgDim <- dim(img)
  
  # Assign RGB channels to data frame
  imgRGB <- data.frame(
    x = rep(1:imgDim[2], each = imgDim[1]),
    y = rep(imgDim[1]:1, imgDim[2]),
    R = as.vector(img[,,1]),
    G = as.vector(img[,,2]),
    B = as.vector(img[,,3])
  )
  
 
  
  noClusters <- 3
  kMeans <- kmeans(imgRGB[, c("R", "G", "B")], centers = noClusters)
  kColours <- rgb(kMeans$centers[kMeans$cluster,])
  
  ggplot(data = imgRGB, aes(x = x, y = y)) + geom_point(colour = kColours) + labs(title = paste("Segmented Image:",i,sep = "")) 
  res<- paste("image ",i,".png",sep = "")  
  ggsave(res,path = "C:/Users/nitesh/Documents/ML_ass3/ML/Assignment/Assignment6/part 3/ClusteredImages")
}
  

