clear all ;

% ======================================================================= %
% Run-time parameters:
% ======================================================================= %
azimuth = 45 ; elevation = 10 ;
plot_scale = 10 ; % for bond lengths, atom radius...
background_color =  [ 1 1 1 ] ;


% ======================================================================= %
% Reading OUTCAR.
% ======================================================================= %
[o,startlines] = unix('grep -n "TOTAL-FORCE " OUTCAR | awk -F ":" ''{print ($1+2)}'' '); 
startlines = sscanf(startlines,'%d'); niteration = size(startlines,1) ;


[o,nions] = unix('grep "ions per type" OUTCAR | awk -F "=" ''{print $2}'' '); 
nions = sscanf(nions,'%d'); ntype = size(nions,1) ; stoplines = startlines+sum(nions)-1 ; 


for i=1:size(startlines,1)
    [o,posandforce] = unix(sprintf('awk "NR==%d,NR==%d" OUTCAR',startlines(i),stoplines(i)));
    posandforce = sscanf(posandforce,'%g',[6 sum(nions)]); posandforce = posandforce';
    stage{i} = posandforce ;
end


[o,labellines] = unix('grep -n "VRHFIN" OUTCAR | awk -F ":" ''{print $1}'' '); 
labellines = sscanf(labellines,'%d'); 

for i=1:size(labellines,1)
    [o,label] = unix(sprintf('awk "NR==%d" OUTCAR | awk -F "=" ''{print $2}'' | awk -F ":" ''{print $1}'' ',labellines(i))); 
    label = label(1:size(label,2)-1); labels{i} = label ;
end


[o,energies] = unix('grep "  energy  without entropy=" OUTCAR  | awk ''{print $7}'' ');
energies = sscanf(energies,'%g'); 


% ======================================================================= %
% Atomic properties
% ======================================================================= %
for a=1:ntype
switch labels{a}
case 'H';   ainfo{a}=[1,0.32,1.000,1.000,1.000]; 
case 'He';  ainfo{a}=[2,0.93,0.851,1.000,1.000]; 
case 'Li';  ainfo{a}=[3,1.23,0.800,0.502,1.000]; 
case 'Be';  ainfo{a}=[4,0.90,0.761,1.000,0.000]; 
case 'B';   ainfo{a}=[5,0.82,1.000,0.710,0.710]; 
case 'C';   ainfo{a}=[6,0.77,0.565,0.565,0.565]; 
case 'N';   ainfo{a}=[7,0.75,0.188,0.314,0.973]; 
case 'O';   ainfo{a}=[8,0.73,1.000,0.051,0.051]; 
case 'F';   ainfo{a}=[9,0.72,0.565,0.878,0.314]; 
case 'Ne';  ainfo{a}=[10,0.71,0.702,0.890,0.961];
case 'Na';  ainfo{a}=[11,1.54,0.671,0.361,0.949];
case 'Mg';  ainfo{a}=[12,1.36,0.541,1.000,0.000];
case 'Al';  ainfo{a}=[13,1.18,0.749,0.651,0.651];
case 'Si';  ainfo{a}=[14,1.11,0.941,0.784,0.627];
case 'P';   ainfo{a}=[15,1.06,1.000,0.502,0.000];
case 'S';   ainfo{a}=[16,1.02,1.000,1.000,0.188];
case 'Cl';  ainfo{a}=[17,0.99,0.122,0.941,0.122];
case 'Ar';  ainfo{a}=[18,0.98,0.502,0.820,0.890];
case 'K';   ainfo{a}=[19,2.03,0.561,0.251,0.831];
case 'Ca';  ainfo{a}=[20,1.74,0.239,1.000,0.000];
case 'Sc';  ainfo{a}=[21,1.44,0.902,0.902,0.902];
case 'Ti';  ainfo{a}=[22,1.32,0.749,0.761,0.780];
case 'V';   ainfo{a}=[23,1.22,0.651,0.651,0.671];
case 'Cr';  ainfo{a}=[24,1.18,0.541,0.600,0.780];
case 'Mn';  ainfo{a}=[25,1.17,0.612,0.478,0.780];
case 'Fe';  ainfo{a}=[26,1.17,0.878,0.400,0.200];
case 'Co';  ainfo{a}=[27,1.16,0.941,0.565,0.627];
case 'Ni';  ainfo{a}=[28,1.15,0.314,0.816,0.314];
case 'Cu';  ainfo{a}=[29,1.17,0.784,0.502,0.200];
case 'Zn';  ainfo{a}=[30,1.25,0.490,0.502,0.690];
case 'Ga';  ainfo{a}=[31,1.26,0.761,0.561,0.561];
case 'Ge';  ainfo{a}=[32,1.22,0.400,0.561,0.561];
case 'As';  ainfo{a}=[33,1.20,0.741,0.502,0.890];
case 'Se';  ainfo{a}=[34,1.16,1.000,0.631,0.000];
case 'Br';  ainfo{a}=[35,1.14,0.651,0.161,0.161];
case 'Kr';  ainfo{a}=[36,1.89,0.361,0.722,0.820];
case 'Rb';  ainfo{a}=[37,2.16,0.439,0.180,0.690];
case 'Sr';  ainfo{a}=[38,1.91,0.000,1.000,0.000];
case 'Y';   ainfo{a}=[39,1.62,0.580,1.000,1.000];
case 'Zr';  ainfo{a}=[40,1.45,0.580,0.878,0.878];
case 'Nb';  ainfo{a}=[41,1.34,0.451,0.761,0.788];
case 'Mo';  ainfo{a}=[42,1.30,0.329,0.710,0.710];
case 'Tc';  ainfo{a}=[43,1.27,0.231,0.620,0.620];
case 'Ru';  ainfo{a}=[44,1.25,0.141,0.561,0.561];
case 'Rh';  ainfo{a}=[45,1.25,0.039,0.490,0.549];
case 'Pd';  ainfo{a}=[46,1.28,0.000,0.412,0.522];
case 'Ag';  ainfo{a}=[47,1.34,0.753,0.753,0.753];
case 'Cd';  ainfo{a}=[48,1.41,1.000,0.851,0.561];
case 'In';  ainfo{a}=[49,1.44,0.651,0.459,0.451];
case 'Sn';  ainfo{a}=[50,1.41,0.400,0.502,0.502];
case 'Sb';  ainfo{a}=[51,1.40,0.620,0.388,0.710];
case 'Te';  ainfo{a}=[52,1.36,0.831,0.478,0.000];
case 'I';   ainfo{a}=[53,1.33,0.580,0.000,0.580];
case 'Xe';  ainfo{a}=[54,1.31,0.259,0.620,0.690];
case 'Cs';  ainfo{a}=[55,2.35,0.341,0.090,0.561];
case 'Ba';  ainfo{a}=[56,1.98,0.000,0.788,0.000];
case 'La';  ainfo{a}=[57,1.25,0.439,0.831,1.000];
case 'Ce';  ainfo{a}=[58,1.65,1.000,1.000,0.780];
case 'Pr';  ainfo{a}=[59,1.65,0.851,1.000,0.780];
case 'Nd';  ainfo{a}=[60,1.64,0.780,1.000,0.780];
case 'Pm';  ainfo{a}=[61,1.63,0.639,1.000,0.780];
case 'Sm';  ainfo{a}=[62,1.62,0.561,1.000,0.780];
case 'Eu';  ainfo{a}=[63,1.85,0.380,1.000,0.780];
case 'Gd';  ainfo{a}=[64,1.61,0.271,1.000,0.780];
case 'Tb';  ainfo{a}=[65,1.59,0.188,1.000,0.780];
case 'Dy';  ainfo{a}=[66,1.59,0.122,1.000,0.780];
case 'Ho';  ainfo{a}=[67,1.58,0.000,1.000,0.612];
case 'Er';  ainfo{a}=[68,1.57,0.000,0.902,0.459];
case 'Tm';  ainfo{a}=[69,1.56,0.000,0.831,0.322];
case 'Yb';  ainfo{a}=[70,1.70,0.000,0.749,0.220];
case 'Lu';  ainfo{a}=[71,1.56,0.000,0.671,0.141];
case 'Hf';  ainfo{a}=[72,1.44,0.302,0.761,1.000];
case 'Ta';  ainfo{a}=[73,1.34,0.302,0.651,1.000];
case 'W';   ainfo{a}=[74,1.30,0.129,0.580,0.839];
case 'Re';  ainfo{a}=[75,1.28,0.149,0.490,0.671];
case 'Os';  ainfo{a}=[76,1.26,0.149,0.400,0.588];
case 'Ir';  ainfo{a}=[77,1.27,0.090,0.329,0.529];
case 'Pt';  ainfo{a}=[78,1.30,0.816,0.816,0.878];
case 'Au';  ainfo{a}=[79,1.34,1.000,0.820,0.137];
case 'Hg';  ainfo{a}=[80,1.49,0.722,0.722,0.816];
case 'Tl';  ainfo{a}=[81,1.48,0.651,0.329,0.302];
case 'Pb';  ainfo{a}=[82,1.47,0.341,0.349,0.380];
case 'Bi';  ainfo{a}=[83,1.46,0.620,0.310,0.710];
case 'Po';  ainfo{a}=[84,1.53,0.671,0.361,0.000];
case 'At';  ainfo{a}=[85,1.47,0.459,0.310,0.271];
otherwise;  ainfo{a}=[0,2,0.5,0.5,0.5];
end
end


n=1;
for t=1:ntype
    howmany=nions(t) ;
    label_list(n:n+howmany-1,1)=ainfo{t}(1) ;
    label_list(n:n+howmany-1,2)=ainfo{t}(2) ;
    label_list(n:n+howmany-1,3)=ainfo{t}(3) ;
    label_list(n:n+howmany-1,4)=ainfo{t}(4) ;
    label_list(n:n+howmany-1,5)=ainfo{t}(5) ;     
    n=n+howmany;
end



% ======================================================================= %
% Plotting
% ======================================================================= %
figure('Color',background_color) ; subplot(2,1,1) ;
positions = stage{1}(:,1:3) ;
for a=1:size(positions,1)
    plot3(positions(a,1),positions(a,2),positions(a,3),...
        'MarkerFaceColor',[label_list(a,3) label_list(a,4) label_list(a,5)],...
        'MarkerEdgeColor',[label_list(a,3) label_list(a,4) label_list(a,5)],'Marker','o',...
        'MarkerSize',plot_scale*label_list(a,2),...
        'LineStyle','none'); hold on;
end

for ii=1:size(positions)
    for jj=1:size(positions)
        pos1=positions(ii,1:3); pos2=positions(jj,1:3);
        bond_length=norm(pos1-pos2);
        if (bond_length < 2)
            line( [pos1(1) pos2(1)], [pos1(2) pos2(2)], [pos1(3) pos2(3)] ,...
                'LineWidth',plot_scale/5,'LineStyle','-'); hold on;
        end
    end
end



axis equal ; axis off; view(azimuth,elevation) ; 
subplot(2,1,2) ; bar((1:size(stage,2)),energies-min(energies));

frame = getframe(1); fim = frame2im(frame);
[im,map] = rgb2ind(fim,256,'nodither');



n=1;
for s=1:size(stage,2); 
clf ; subplot(2,1,1) ;
positions = stage{s}(:,1:3) ;
for a=1:size(positions,1)
    plot3(positions(a,1),positions(a,2),positions(a,3),...
        'MarkerFaceColor',[label_list(a,3) label_list(a,4) label_list(a,5)],...
        'MarkerEdgeColor',[label_list(a,3) label_list(a,4) label_list(a,5)],'Marker','o',...
        'MarkerSize',plot_scale*label_list(a,2),...
        'LineStyle','none'); hold on;
end

for ii=1:size(positions)
    for jj=1:size(positions)
        pos1=positions(ii,1:3); pos2=positions(jj,1:3);
        bond_length=norm(pos1-pos2);
        if (bond_length < 2)
            line( [pos1(1) pos2(1)], [pos1(2) pos2(2)], [pos1(3) pos2(3)] ,...
                'LineWidth',plot_scale/5,'LineStyle','-'); hold on;
        end
    end
end

axis equal ; axis off; view(azimuth,elevation) ; 
legend_text = ['step = ' num2str(s)] ; legend(legend_text,1) ;
subplot(2,1,2) ; bar((1:s),energies(1:s)-min(energies)); 
xlim([ 1 size(stage,2) ]); ylim([ min(energies-min(energies)) max(energies-min(energies))  ]);
xlabel('Step #' , 'FontWeight','bold','FontSize',15,'FontName','Times',...
      'Color',[0.6 0.2 0]); 
ylabel('\Delta Energy (eV) ', 'FontWeight','bold','FontSize',15,'FontName','Times',...
      'Color',[0.6 0.2 0]);   
frame = getframe(1); fim = frame2im(frame);
%  h = myaa; frame = getframe(1) ; close(h); fim = frame2im(frame);
im(:,:,1,n) = rgb2ind(fim,map,'nodither'); n = n+1 ; 
end


imwrite(im,map,'MD.gif','DelayTime',0,'LoopCount',inf) ;

