class1= [0.5, 0.1, 0.2, 0.4, 0.3, 0.2, 0.2, 0.1, 0.35, 0.25];
class2= [0.9, 0.8, 0.75, 1.0];
mean1=mean(class1);
std1 = std(class1);

mean2=mean(class2);
std2=std(class2);

t=[-1.5:0.01:1.5];

y1=normpdf(t,mean1,std1);
y2=normpdf(t,mean2,std2);

figure(1)


plot(t,y1,"r","linewidth", 2)
%title ("x & y labels & ticklabels");
hold on;
plot(t,y2,"g","linewidth", 2)
legend('class1','class2')

% class1 with x =0.6
p1_06 = (1/sqrt(2*pi*std1) )*exp(-((0.6-mean1)^2)/(2*std1))
% exei lathos thelei desmeymeni pithanotita gia na ypologiseis
