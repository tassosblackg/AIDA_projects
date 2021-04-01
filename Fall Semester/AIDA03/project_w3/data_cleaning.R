# data cleaning week 3
#------------------------------ |Askhsh 3.1|------------------------------------------------------------
df <- read.csv("~/projects/AIDA_projects/AIDA03/project_w3/dirty_iris.csv",stringsAsFactors=FALSE)
head(df)
# check percentage of missing values per column
pMiss = function(x){sum(is.na(x))/length(x)*100}
apply(df,2,pMiss)
apply(df, 1, pMiss)
# Find missing values in R
ok <-complete.cases(df)
ok
sum(!ok)
# check for other special values is.nan(), is.infinite() not implemented for list

# ------------------------ |Askshsh 3.2|-----------------------------------------------------------------
library('editrules')
E <- editfile('~/projects/AIDA_projects/AIDA03/project_w3/iris_rules.txt')
E
# see how many times rules are violated
ve <- violatedEdits(E, df)
summ_ve<-summary(ve)
plot(ve)
# percentage of data with no errors
zero_err<-summ_ve[summ_ve$errors == 0, ]
zero_err$rel

# show Too long petals -> 'num7' constraint is TRUE
library('dplyr')
df_ve <- data.frame(ve)
res <- filter(df_ve, num7 == TRUE)

# find outliers with boxplots
library('ggplot2')
ggplot(df,aes(y=Sepal.Length, x=Species)) +
  geom_boxplot() +
  scale_y_log10() + 
  coord_trans(y="log10") 

st <- boxplot.stats(df["Sepal.Length"],coef = 1.5)


# -------------------------|Askhsh 3.3|------------------------------------------------------------------
library('deducorrect')
R <- correctionRules("~/projects/AIDA_projects/AIDA03/project_w3/iris_conversions.txt")
cor <- correctWithRules(R, df)

le <- localizeErrors(E,df,method = 'mip')
le$adapt
library('naniar')
# replace with NA
df_replaced<-df %>% replace_with_na(replace = list(le$adapt == TRUE))

# ----------------------|Askhsh 3.4|--------------------------------------------------------------------
library('VIM')
df2 <- kNN(df_replaced)

seqImpute <- function(x,last){
  n <- length(x)
  x <- c(x,last)
  i <- is.na(x)
  while(any(i)){
    x[i] <- x[which(i) + 1]
    i <- is.na(x)
  }
  x[1:n]
}

df3 <-df[order(df$Species),]
sapply(df3[df3$Petal.Width,],seqImpute, mean(df3$Petal.Width))

df4<-df[order(df$Species, -df$Sepal.Length),]
sapply(df3[df3$Petal.Width,],seqImpute, mean(df3$Petal.Width))
