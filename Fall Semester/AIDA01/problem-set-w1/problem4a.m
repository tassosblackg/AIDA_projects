N=100
theta=[-1,-0.5,0,0.5,1]
P_theta= 1/5
p =[ 1/5, 1/5,1/5,1/5,1/5]
s_2 =0.5
t=[0:0.5:N]
% get an element from theta pseudo-randomly
indx=randi([1, length(theta)]);


e = sqrt(s_2)*randn(1,length(t));
x = sin(theta(indx)*t) +e;




A = [0, 0, 0 ,0 ,0]
% Posterior prob
%p_theta ~ = (1/sqrt(2*pi*s_2))*exp(-1/2*s_2)*(x-sin(theta*t))^2

for j = 1:length(theta)
  for i = 1:length(t)
    if i == 1
      A(j) = (1/sqrt(2*pi*s_2))*exp(-1/2*s_2)*(x(i)-sin(theta(j)*t(i)))^2;
    else
       A(j) = A(j)*((1/sqrt(2*pi*s_2))*exp(-1/2*s_2)*(x(i)-sin(theta(j)*t(i)))^2);
    end
  end
  A(j) = P_theta * A(j)
end

figure(1)
plot(t,x)

figure(2)
axis([-1.5 1.5 0 0.3])
bar(theta, p)


figure(3)
bar(theta, A)

[max_val max_ind]=max(A)
