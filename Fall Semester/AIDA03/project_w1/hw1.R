# EDAV - Εργασία 1

# Το θέμα της εργασίας είναι η επεξεργασία/μετασχηματισμός δεδομένων (data wrangling) με τη βοήθεια των
# πακέτων dplyr και tidyr του tidyverse. Συμπληρώστε τις απαντήσεις σας στο διαθέσιμο χώρο αμέσως μετά
# το κάθε ερώτημα.

library(tidyverse)

# Αρχίζουμε με την dplyr
library(dplyr)

# Έχουμε το dataset iris.
data("iris")
df<-class(iris)
glimpse(iris)
# 1. Εμφανίστε τις εγγραφές 6 ως 10 (hint: δείτε τις head() και tail())
head(iris) # πρωτες 6
tail(iris) #τελευταιες 6
a=head(iris,10) # 1-10
tail(a,5) # apo tis 10 tis teleytaies 5 -> 6:10

# 2. Εμφανίστε όλα τα λουλούδια versicolor με Sepal.length > 6
versicolor <- filter(iris,Species=="versicolor",Sepal.Length >6)
versicolor
# 3. Εμφανίστε όλα τα λουλούδια που έχουν Petal.length μεγαλύτερο από το μέσο Petal.length
m <- mean(iris$Petal.Length)
flower3 <- filter(iris,Petal.Length> m)

# 4. Εμφανίστε όλες τις στήλες εκτός του Species.
flower4 <- subset(iris,select = -c(Species))
flower4
# 5. Εμφανίστε τις στήλες που αρχίζουν από 'S'.
flower5<-select(iris,starts_with("S"))
flower5
# 6. Εμφανίστε τις μεταβλητές που περιέχουν το αλφαριθμητικό "Len".
indx <- grepl('Len', colnames(iris)) # βρες τους δεικτες των columns που εχουν το "Len"
names(iris[indx])

# 7. Μετονομάστε τη στήλη Species σε Type.
# colnames(iris)[colnames(iris) == "Species"] <- "Type"
iris<-iris %>% rename(Type = Species)
head(iris)
# 8. Ταξινομήστε το αρχείο ως προς Petal.Length (desc) και μετά ως προς Petal.Width (asc)
flower8 <- iris %>% arrange(desc(Petal.Length))
flower8
flower8b <-iris %>% arrange(desc(Petal.Width))
flower8b
# 9. Προσθέστε δυο στήλες με τα αθροίσματα των μηκών και των πλατών
iris$LengthSum<-iris$Sepal.Length + iris$Petal.Length
iris$WidthSum<-iris$Sepal.Width + iris$Petal.Width

#10. Υπολογίστε το άθροισμα της κάθε στήλης (hint: δείτε την summarise_all())
iris_new <- as_tibble(iris)
#summarise_all(iris_new,)
iris_new %>%
  select(-Type) %>%
  summarise_all(sum) #??

#11. Για κάθε είδος (Species) υπολογίστε τα min, max, mean, median του Petal.Length
#    (hint: δείτε την summarise_at())
iris_new %>%
  group_by(Type) %>%
  summarize_at(vars(Petal.Length), funs(min, max, mean, median))

# Συνεχίζουμε με την tidyr
library(tidyr)
#12. Μεταβλητές: από στήλες σε ζεύγη τύπου (κλειδί, τιμή)
#    Πολλές φορές μια μεταβλητή (variable) καταλαμβάνει πολλές στήλες. Για παράδειγμα, στο dataset iris,
#    μπορεί να επιθυμούμε να θεωρήσουμε τα Sepal.Length, Sepal.Width, Petal.Length και Petal.Width ως
#    παραλλαγές της μοναδικής μεταβλητής measure. Μετασχηματίστε το iris στο iris2 με την παρακάτω δομή:

iris_drop_sums <- iris %>% select(-LengthSum,-WidthSum)

  iris2 <- iris_drop_sums %>%
              gather("Sepal.Length","Sepal.Width","Petal.Length","Petal.Width", key="measure",value="value")

head(iris2)
# Species      measure value
# 1  setosa Sepal.Length   5.1
# 2  setosa Sepal.Length   4.9
# 3  setosa Sepal.Length   4.7
# 4  setosa Sepal.Length   4.6
# 5  setosa Sepal.Length   5.0
# 6  setosa Sepal.Length   5.4
# ...



#13. Μεταβλητές: Από ζεύγη τύπου (κλειδί, τιμή) σε στήλες
#    Έστω ότι θέλουμε να επαναφέρουμε το iris2 στο αρχικό iris. Δυστυχώς, αυτό δεν είναι πλέον εφικτό!
#    Έχουμε χάσει την πληροφορία των συνδυασμών Sepal.Length, Sepal.Width, Petal.Length και Petal.Width
#    που αντιστοιχούν στο ίδιο λουλούδι... Για να μη συμβεί αυτό, θα έπρεπε να ακολουθούσαμε μια από τις
#    παρακάτω δυο προσεγγίσεις:
#    (α) να δίναμε πρώτα ένα μοναδικό ID σε κάθε λουλούδι και μετά να προχωρούσαμε σε αυτό που ζητούσε το
#    ερώτημα 12. Συνεπώς, προσθέστε μια στήλη με μοναδικό ID (1,2,3...,150) σε κάθε εγγραφή του iris πριν
#    δημιουργήσετε το iris2.
iris_with_ID <- mutate(iris_drop_sums,ID=row_number())
iris2a <- iris_with_ID %>%
  gather("Sepal.Length","Sepal.Width","Petal.Length","Petal.Width", key="measure",value="value")

#    (β) εναλλακτικά, αριθμήστε τα 50 στιγμιότυπα του κάθε είδος λουλουδιού από το 1 ως το 50.
#    Στο πρώτο σενάριο το κλειδί είναι το πεδίο ID που προσθέσαμε, ενώ στο δεύτερο σενάριο, κλειδί είναι ο
#    συνδυασμός (ID, species). (hint: δείτε τί κάνει η συνάρτηση rep).
iris_with_ID_2<-mutate(iris_drop_sums,ID=rep(1:50, 3) )
iris2b <- iris_with_ID %>%
  gather("Sepal.Length","Sepal.Width","Petal.Length","Petal.Width", key="measure",value="value")
#    Εναλλακτικά, μπορείτε να προσθέσετε στο iris2 την κατάλληλη αρίθμηση που να κάνει κάθε αρχική
#    εγγραφή μοναδική. Παρατηρήστε ότι στο iris2 έχουμε 50 εγγραφές με Sepal.Length για τα setosa,
#    ακολουθούμενες από 50 εγγραφές με Sepal.Length για τα versicolor, κοκ. Εφόσον ο συνδυασμός ενός
#    ID (1,2,3,...,50) για κάθε είδος λουλουδιού με τον τύπο του λουλουδιού είναι μοναδικός για κάθε
#    εγγραφή, αρκεί να προσθέσουμε στο iris2 μια νέα στήλη με περιεχόμενο 12 φορές το διάνυσμα 1:50.
iris2c<-mutate(iris2,ID=rep(1:50, each=4,times=3) )
#iris3b <- iris_with_ID %>%
 # gather("Sepal.Length","Sepal.Width","Petal.Length","Petal.Width", key="measure",value="value")
#    Γενικά, για να δουλέψει το spead ή το pivot.wider, πρέπει κάθε set "απλωμένων" τιμών να αντιστοιχεί
#    σε μοναδικό συνδυασμό τιμών των υπολοίπων στηλών.

#    Δώστε και τις τρεις εναλλακτικές λύσεις.




#14. Μεταβλητές: και σε ζεύγη τύπου (κλειδί, τιμή) και σε στήλες (τελείως messy!)
#    Πολλές φορές μεταβλητές αποθηκεύονται και σε γραμμές και σε στήλες... Δείτε το παρακάτω παράδειγμα
#    όπου τα δεδομένα είναι τελείως messy! Τελικός στόχος είναι να έχουμε εγγραφές που να προσδιορίζονται
#    μοναδικά από το όνομα του ασθενή και την επίσκεψη (δηλαδή, κάθε επίσκεψη θα έχει μια σειρά από
#    μετρήσεις).

patient <- c("Γιώργος", "Γιώργος", "Νατάσα", "Νατάσα", "Ισμήνη", "Ισμήνη")
measure <- c("μεγ_πίεση", "μικρή_πίεση", "μεγ_πίεση", "μικρή_πίεση", "μεγ_πίεση", "μικρή_πίεση")
visit1 <- c(170, 100, 135, 85, 120, 80)
visit2 <- c(150, 90, 110, 70, 140, 90)
df <- data.frame(patient, measure, visit1, visit2)
df

#14α Πρώτα τοποθετήστε όλες τις τιμές των επισκέψεων σε μια στήλη:
#    patient     measure  visit value
# 1  Γιώργος   μεγ_πίεση visit1   170
# 2  Γιώργος μικρή_πίεση visit1   100
# 3   Νατάσα   μεγ_πίεση visit1   135
# 4   Νατάσα μικρή_πίεση visit1    85
# 5   Ισμήνη   μεγ_πίεση visit1   120
# 6   Ισμήνη μικρή_πίεση visit1    80
# 7  Γιώργος   μεγ_πίεση visit2   150
# 8  Γιώργος μικρή_πίεση visit2    90
# 9   Νατάσα   μεγ_πίεση visit2   110
# 10  Νατάσα μικρή_πίεση visit2    70
# 11  Ισμήνη   μεγ_πίεση visit2   140
# 12  Ισμήνη μικρή_πίεση visit2    90

df2 <- df %>%
          gather("visit1","visit2",key="visit",value = "value")
df2
#14β Τώρα δημιουργείστε χωριστές στήλες για τη μεγάλη και τη μικρή πίεση.
#   patient  visit μεγ_πίεση μικρή_πίεση
# 1 Γιώργος visit1       170         100
# 2 Γιώργος visit2       150          90
# 3  Ισμήνη visit1       120          80
# 4  Ισμήνη visit2       140          90
# 5  Νατάσα visit1       135          85
# 6  Νατάσα visit2       110          70
df3 <- df2 %>% spread(measure,value)
df3
