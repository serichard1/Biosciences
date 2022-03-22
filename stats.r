#Import data
data = read.table("res.txt")

#Clean data
data$V1 = gsub(',','', data$V1)
data$V2 = gsub(',','', data$V2)
data$V1 = gsub('\\(','', data$V1)
data$V2 = gsub('\\(','', data$V2)
data$V1 = gsub('\\)','', data$V1)
data$V2 = gsub('\\)','', data$V2)
data$V1 = gsub('\\[', '', data$V1)
data$V2 = gsub('\\]', '', data$V2)
data$V2 = as.numeric(data$V2)

#Stats
good = data$V2[data$V1 == "tensor0"];
bad = data$V2[data$V1 == "tensor1"];

dev.new();
par(mfrow = c(2,1));

hist(good);
hist(bad);
print(t.test(good,bad));
