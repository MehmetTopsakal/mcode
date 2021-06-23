function [lat_new,pos_new] = unitcell_rotation(lat_old,pos_old,u,theta,az,el)
%
% usage : [lat_new,pos_new] = unitcell_rotation(lat_old,pos_old,[0 0 1],15,0,90)
%


%  lat_old = 2.511480000*[
%   1.000000   0.000000   0.000000
%  -0.500000   0.866025   0.000000
%   0.000000   0.000000   1.191781
%  ];
%  
%  
%  pos_old = [
%  0.00000      1.45000      5.99999
%  1.25574      0.72500      5.99999];




lat_new = rodrigues_rot(lat_old,u,theta);
pos_new = rodrigues_rot(pos_old,u,theta);


figure


subplot(1,2,1)
lat=lat_old; pos=pos_old;
line([0 lat(1,1)], [0 lat(1,2)], [0 lat(1,3)],'LineWidth',5,'LineStyle','-','Color','r'); hold on;
line([0 lat(2,1)], [0 lat(2,2)], [0 lat(2,3)],'LineWidth',5,'LineStyle','-','Color','g'); hold on;
line([0 lat(3,1)], [0 lat(3,2)], [0 lat(3,3)],'LineWidth',5,'LineStyle','-','Color','b'); hold on;
for pp=1:size(pos,1)
plot3(pos(pp,1),pos(pp,2),pos(pp,3),'MarkerFaceColor','k','MarkerEdgeColor','k','Marker','o','MarkerSize',10)
end
axis equal ; axis off; grid on ; box on; view(az,el);  




subplot(1,2,2)
lat=lat_new; pos=pos_new;
line([0 lat(1,1)], [0 lat(1,2)], [0 lat(1,3)],'LineWidth',5,'LineStyle','-','Color','r'); hold on;
line([0 lat(2,1)], [0 lat(2,2)], [0 lat(2,3)],'LineWidth',5,'LineStyle','-','Color','g'); hold on;
line([0 lat(3,1)], [0 lat(3,2)], [0 lat(3,3)],'LineWidth',5,'LineStyle','-','Color','b'); hold on;
for pp=1:size(pos,1)
plot3(pos(pp,1),pos(pp,2),pos(pp,3),'MarkerFaceColor','k','MarkerEdgeColor','k','Marker','o','MarkerSize',10)
end
axis equal ; axis off; grid on ; box on; view(az,el);  



print -depsc plot.eps


end

