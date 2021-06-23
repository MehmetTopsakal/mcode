function [fit_x0, fit_y0, fit_E0] = minxy(key)



figure


if nargin < 1,  key=1; end ; 

if key==1
%  ! vdc
data=load('total-analiz.dat'); 
data=[data(:,5) data(:,6) data(:,1)];                                           
end



if key==2
unix(' vdc ');
data=load('total-analiz.dat'); 
data=[data(:,5) data(:,6) data(:,1)];                                          
end



if key==3
data=load('values.dat');                                      
end





min_x=min(data(:,1)); 
max_x=max(data(:,1)); 
min_y=min(data(:,2)); 
max_y=max(data(:,2)); 
min_E=min(data(:,3));


%---- fit to equation --------------------------------------------------- %%%    
for n=1:size(data,1)
    A1(n,1)=data(n,1)^2; 
    A1(n,2)=data(n,1); 
    A1(n,3)=data(n,2)^2; 
    A1(n,4)=data(n,2); 
    A1(n,5)=data(n,1)*data(n,2); 
    A1(n,6)=1;
end
a1=inv(A1'*A1)*(A1'*data(:,3));



[xf,yf]=meshgrid(min_x:0.00005:max_x,min_y:0.00005:max_y);

zf=a1(1)*xf.^2+a1(2)*xf.^1+a1(3)*yf.^2+a1(4)*yf.^1+a1(5)*xf.*yf+a1(6);
[fny0,fnx0]=find(zf==min(min(zf)));

fit_x0=xf(1,fnx0)   ;
fit_y0=yf(fny0,1)   ;
fit_E0=min(min(zf)) ;

 
%--- elastic_constants -------------------------------------------------- %%%
% Poisson's ratios 
nuxy=a1(5)*fit_x0/(2*a1(3)*fit_y0);
nuyx=a1(5)*fit_y0/(2*a1(1)*fit_x0);
 
% in-plane stiffness
kappa_ex=2*(a1(1)-(a1(5)^2)/(4*a1(3)))*fit_x0^2; kappa_ey=2*(a1(3)-(a1(5)^2)/(4*a1(1)))*fit_y0^2;
eV=1.602176487e-19; area=(fit_x0*fit_y0)*10^(-20); 
in_plane_stiffness_x = (eV*kappa_ex)/area ;
in_plane_stiffness_y = (eV*kappa_ey)/area ;

% Young's modulus
thickness=(3.35*10^(-10));
Young_modulus_x = in_plane_stiffness_x/thickness;
Young_modulus_y = in_plane_stiffness_y/thickness;



%--- plot values     -------------------------------------------------- %%%
[xf,yf]=meshgrid(min_x:(max_x-min_x)/25:max_x,min_y:(max_x-min_x)/25:max_y);
zf=a1(1)*xf.^2+a1(2)*xf.^1+a1(3)*yf.^2+a1(4)*yf.^1+a1(5)*xf.*yf+a1(6);


subplot(7,2,[1 3 5 7 9]);
meshc(xf,yf,zf); view([-40 20]); box('on'); grid('on'); hold on;
plot3(data(:,1),data(:,2),data(:,3),'MarkerSize',20,'Marker','.',...
    'LineStyle','none','Color',[1 0 0]);

xlim([min(min(xf)) max(max(xf))]) ; ylim([min(min(yf)) max(max(yf))]);
axis tight


subplot(7,2,[2 4 6 8 10]);
contour3(xf,yf,zf,50); 
view([0 90]); box('on'); grid('on'); hold on;
plot3(data(:,1),data(:,2),data(:,3),'MarkerSize',10,'Marker','.','LineStyle','none','Color',[1 0 0]);
plot3(fit_x0,fit_y0,fit_E0,'MarkerSize',10,'Marker','+','LineStyle','none','Color',[0 0 0]);

xlabel('Lattice_x') ; ylabel('Lattice_y') ; 
xlim([min(min(xf)) max(max(xf))]) ; ylim([min(min(yf)) max(max(yf))]);
axis equal; axis tight; 

subplot(8,1,7); axis off;

text1 = [ 'CALC. min.: x_{(data min.)} = ' num2str(min_x, '%.4f') ' ,  y_{(data min.)} = ' num2str(min_y, '%.4f') ' ,  E_{calc.} = ' num2str(min_E, '%.6f') ' (eV)' ];
text2 = [ 'FIT : x_{(fit)} = ' num2str(fit_x0, '%.4f') ' ,  y_{(fit)} = ' num2str(fit_y0, '%.4f') ' ,  E_{(fit)} = ' num2str(fit_E0, '%.6f') ' (eV) ,  E_{fit}-E_{calc.} = ' num2str(1000*(fit_E0-min_E), '%.2f') ' (meV)'];
text3 = [ 'x_{(data min.)}/x_{(fit)} = ' num2str(min_x/fit_x0, '%.3f') ' , y_{(data min.)}/y_{(fit)} = ' num2str(min_y/fit_y0, '%.3f') ' , x_{(data max.)}/x_{(fit)} = ' num2str(max_x/fit_x0, '%.3f') ' ,  y_{(data max.)}/y_{(fit)} = ' num2str(max_y/fit_y0, '%.3f')  ];

h = text( -0.1,  0.9, text1); set(h,'FontName','Monospaced','FontSize',7) ;
h = text( -0.1,  0.4, text2); set(h,'FontName','Monospaced','FontSize',8,'FontWeight','bold') ;
h = text( -0.1,  0.0, text3); set(h,'FontName','Monospaced','FontSize',7) ;


%  print( '-r150','-dpdf','plot_2.eps')
print( '-r150','-depsc','minxy.eps')


file = fopen('minxy.out','w');
fprintf(file,'%.5f %.5f %.8f \n',fit_x0,fit_y0,fit_E0); 
fclose(file);



end
