function draw_structure(file,az,el)
%
% usage 
%


if nargin < 3, el = 45 ; end ; if nargin < 2, az = 45 ; end
if nargin < 1 ; disp('   '); ls ; file = input('Please enter the filename for drawing : ', 's');
disp('   '); disp('   '); end


bond_length_thr = 2.2

plotheight=100;
plotwidth=100;
subplotsx=1;
subplotsy=1;   
leftedge=1.2;
rightedge=0.4;   
topedge=1;
bottomedge=1.5;
spacex=0.2;
spacey=0.2;
fontsize=5;  
sub_pos=subplot_pos(plotwidth,plotheight,leftedge,rightedge,bottomedge,topedge,subplotsx,subplotsy,spacex,spacey);

f=figure('visible','on');
clf(f);
set(gcf, 'PaperUnits', 'centimeters');
set(gcf, 'PaperSize', [plotwidth plotheight]);
set(gcf, 'PaperPositionMode', 'manual');
set(gcf, 'PaperPosition', [0 0 plotwidth plotheight]);

ax=axes('position',sub_pos{1,1},'XGrid','off','XMinorGrid','off','FontSize',fontsize,'Box','on','Layer','top');

% read file
[lat,pos]=read_poscar(file);

% plot lattice
figure('Color','w')

line([0 lat(1,1)], [0 lat(1,2)], [0 lat(1,3)],'LineStyle','-','Color','r'); hold on;
line([0 lat(2,1)], [0 lat(2,2)], [0 lat(2,3)],'LineStyle','-','Color','g'); hold on;
line([0 lat(3,1)], [0 lat(3,2)], [0 lat(3,3)],'LineStyle','-','Color','b'); hold on;

% plot positions
for a=1:size(pos,1)
    posx=pos(a,1) ; posy=pos(a,2) ; posz=pos(a,3) ; [anumber,aradius,acolor] = ainfo(pos(a,7)) ;
    plot3(posx,posy,posz,...
    'MarkerFaceColor',acolor,'MarkerEdgeColor',acolor,'Marker','o','MarkerSize',12*aradius,...
    'LineStyle','none'); hold on;
end

% plot bonds
for ii=1:size(pos)
    for jj=1:size(pos)
    pos1=pos(ii,1:3); pos2=pos(jj,1:3); bond_length=norm(pos1-pos2);
    if (bond_length < bond_length_thr); line( [pos1(1) pos2(1)], [pos1(2) pos2(2)], [pos1(3) pos2(3)] ,...
    'LineStyle','-','LineWidth',2); hold on;
end; end; end
legend
% axes
axis equal ; axis off; grid on ; box on; view(az,el); 


if ii>1
set(ax,'xticklabel',[]);
end
 
if i>1
set(ax,'yticklabel',[]);
end


% export figure
%  filename = [file '.eps']; print( '-r250','-depsc',filename)
filename=[file];
print(gcf, '-depsc2','-loose',[filename,'.eps']);
[a,b]=system(['convert -density 200 ',filename,'.eps ',filename,'.png']);
[a,b]=system(sprintf(' rm -f %s.eps ',filename)); 
end

