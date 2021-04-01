# hw2

library(tidyverse)
# Θα χρησιμοποιήσετε το dataset EconomistData.
# Τα δεδομένα είναι από το περιοδικό Economist και αφορούν σε δυο δείκτες: 
# HDI = Human Development Index (http://hdr.undp.org/en/content/human-development-index-hdi)
# CPI = Corruption Perceptions Index (https://www.transparency.org/)
#dat <- read_csv("/home/gevan/data/EconomistData.csv")  # αν είστε στον igreed

dat <- read_csv("~/projects/AIDA_projects/AIDA03/project_2/EconomistData.csv")  # αν τρέχετε το rstudio στον υπολογιστή σας
glimpse(dat)

# ο δείκτης HDI παίρνει τιμές από 0 ως 1, με 1 να είναι το άριστο 
# ο δείκτης CPI παίρνει τιμές από 0 ως 10, με 10 να είναι το άριστο

# Δείτε ποια Regions υπάρχουν
unique(dat$Region)
# Εξηγήσεις ακρωνυμίων:
# MENA = Middle East and North Africa
# SSA = Sub-Saharan Africa
# East EU Cemt Asia = Ανατολική Ευρώπη και χώρες της Ασίας που έχουν CEMT permit,
# όπου CEMT = Conférence Européenne des Ministres des Transports

# Δείτε ποιες χώρες είναι στο Region "EU W. Europe"
dat %>% filter(Region=="EU W. Europe") %>% view()
# Η Ελλάδα αγωνίζεται σκληρά να περάσει τη Βουλγαρία στην πρώτη θέση της διαφθοράς!


# Μια και αναφέρθηκε στο μάθημα: Για όσους βλέπουν sql στον ύπνο τους, να πως
# παρακάμπτεις το library dplyr που παρέχει τις select, filter, arrange, mutate, summarize
# και γράφεις απευθείας σε λατρεμένη sql!

library(sqldf)

dat2 <- sqldf("
  select Region, avg(HDI) as avgHDI, avg(CPI) as avgCPI
  from dat
  group by Region")


# Ορίστε μια σύγκριση των Regions ως προς τους δυο δείκτες 
ggplot(dat2, aes(x = avgHDI, y = avgCPI, color=Region)) + geom_point()

# Να πως πετυχαίνουμε το ίδιο με τις functions της dplyr
(dat3 <- dat %>% 
    group_by(Region) %>% summarise(avgHDI = mean(HDI), avgCPI = mean(CPI)))

ggplot(dat3, aes(x = avgHDI, y = avgCPI, color=Region)) +
  geom_point()

# Για να απαντήσετε στα παρακάτω προβλήματα, συμβουλευτείτε το cheat sheet του
# ggplot2 (https://www.rstudio.com/wp-content/uploads/2015/03/ggplot2-cheatsheet.pdf)
# Δεν υπάρχει μια απάντηση καθώς υπάρχουν πολλοί τρόποι να αναπαρασταθούν τα
# ζητούμενα του κάθε προβλήματος. Πειραματιστείτε με διαφορετικά plots και
# αυτοσχεδιάστε. Καταθέστε στο CoMPUs το παρόν αρχείο με τις απαντήσεις σας.

# 1. Δώστε ένα plot που να περιγράφει την κατανομή της CPI 
ggplot(dat,aes(CPI))+ geom_density()
ggplot(dat,aes(CPI))+ geom_bar()

# 2. Δώστε ένα plot που να δείχνει το πλήθος των χωρών ανά Region
ggplot(dat,aes(Region))+ geom_dotplot()

# 3. Δώστε ένα plot που να δείχνει το ποσοστό των χωρών ανά Region
ggplot(dat, aes(Region)) + 
  geom_bar(aes(y = (..count..)/sum(..count..))) + 
  scale_y_continuous(labels=scales::percent) +
  ylab("relative frequencies")

# 4. Δώστε ένα plot που να δείχνει τη μέση HDI ανά Region 
ggplot(dat2,aes(y=avgHDI,x=Region))+geom_dotplot()
# 5. Δώστε ένα plot που να δείχνει τη συσχέτιση των ΗDI και CPI για όλες τις χώρες
dat5<-dat %>% 
  group_by(Country)
ggplot(dat5,aes(x = HDI,y = CPI))+geom_point()


# 6. Δώστε μια ομάδα από plots (facet) που να δείχνει τη συσχέτιση των ΗDI και CPI
#    για όλες τις χώρες του κάθε Region 

ggplot(dat,aes(x = HDI,y = CPI))+geom_point()+facet_grid(.~ Region)
