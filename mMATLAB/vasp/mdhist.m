function [energies]=mdhist(interval,azimuth,elevation,plot_scale) 
%
% usage example > mdhist(20,50,30,10)
%

if nargin < 4,  plot_scale = 10 ;      
end
if nargin < 3,   elevation = 60 ;      
end
if nargin < 2,     azimuth = 25 ;      
end
if nargin < 1,    interval = 1 ;       
end


% ======================================================================= %
% Run-time parameters:
% ======================================================================= %
%  clear all ; format long
%   interval = 100 ; 
%   azimuth = 60 ; 
%   elevation = 20 ;
%   plot_scale = 10 ;
background_color =  [ 1 1 1 ] ;
% ['interval=' num2str(interval) ', azimuth= ' num2str(azimuth) ', elevation=' num2str(elevation) ', plot_scale=' num2str(plot_scale) ]

% ======================================================================= %
% Reading OUTCAR.
% ======================================================================= %
disp('|| Reading OUTCAR......');
% convert xml to txt
unix(' awk ''{ print }'' vasprun.xml > vasprun.txt ');


[o,startlines] = unix('grep -n ''<varray name="positions" >'' vasprun.txt | awk -F ":" ''{print ($1+1)}'' '); 
startlines = sscanf(startlines,'%d'); 

[o,nions] = unix(' awk ''/pseudopotential/,/initialpos/'' vasprun.txt | grep ''<rc><c>'' | awk ''{print $2}'' | awk -F ''<''  ''{print $1}'' '); 
nions = sscanf(nions,'%d'); ntype = size(nions,1) ; stoplines = startlines+sum(nions)-1 ; 

[o,lattice] = unix(' awk ''/initialpos/,/volume/'' vasprun.txt | grep ''<v>'' | awk ''{print $2"  "$3"  "$4}'' '); 
lattice = sscanf(lattice,'%g',[3 3]); lattice = lattice';


% ======================================================================= %
% Read initial and final positions.
% ======================================================================= %
disp('|| Reading initail and final positions......');
% (POSCAR)
[o,poscar] = unix(sprintf('awk "NR==%d,NR==%d" vasprun.txt | awk ''{print $2"  "$3"  "$4}'' ',startlines(1),stoplines(1)));
poscar = sscanf(poscar,'%g',[3 sum(nions)]); poscar = poscar';
    
for p=1:size(poscar,1) ;
    xt = poscar(p,1)*lattice(1,1) + poscar(p,2)*lattice(2,1) + poscar(p,3)*lattice(3,1) ;
    yt = poscar(p,1)*lattice(1,2) + poscar(p,2)*lattice(2,2) + poscar(p,3)*lattice(3,2) ;
    zt = poscar(p,1)*lattice(1,3) + poscar(p,2)*lattice(2,3) + poscar(p,3)*lattice(3,3) ;
    poscar_cart(p,1) = xt; poscar_cart(p,2) = yt; poscar_cart(p,3) = zt;
end ; poscar = poscar_cart;

% (CONTCAR)
[o,contcar] = unix(sprintf('awk "NR==%d,NR==%d" vasprun.txt | awk ''{print $2"  "$3"  "$4}'' ',max(startlines),min(stoplines)));
contcar = sscanf(contcar,'%g',[3 sum(nions)]); contcar = contcar';
    
for p=1:size(poscar,1) ;
    xt = contcar(p,1)*lattice(1,1) + contcar(p,2)*lattice(2,1) + contcar(p,3)*lattice(3,1) ;
    yt = contcar(p,1)*lattice(1,2) + contcar(p,2)*lattice(2,2) + contcar(p,3)*lattice(3,2) ;
    zt = contcar(p,1)*lattice(1,3) + contcar(p,2)*lattice(2,3) + contcar(p,3)*lattice(3,3) ;
    contcar_cart(p,1) = xt; contcar_cart(p,2) = yt; contcar_cart(p,3) = zt;
end ; contcar = contcar_cart;


% ======================================================================= %
% Read MD positions.
% ======================================================================= %
disp('|| Reading Molecular Dynamics positions......');
startlines = startlines(2:size(startlines,1)-1) ; niterations = size(startlines) ;
 stoplines = stoplines(2:size(stoplines,1)-1)   ;
 
s=1;
for i=interval:interval:size(startlines,1)
    [o,positions] = unix(sprintf('awk "NR==%d,NR==%d" vasprun.txt | awk ''{print $2"  "$3"  "$4}'' ',startlines(i),stoplines(i)));
    positions = sscanf(positions,'%g',[3 sum(nions)]); positions = positions';
    
    for p=1:size(positions,1) ;
    xt = positions(p,1)*lattice(1,1) + positions(p,2)*lattice(2,1) + positions(p,3)*lattice(3,1) ;
    yt = positions(p,1)*lattice(1,2) + positions(p,2)*lattice(2,2) + positions(p,3)*lattice(3,2) ;
    zt = positions(p,1)*lattice(1,3) + positions(p,2)*lattice(2,3) + positions(p,3)*lattice(3,3) ;
    positions_cart(p,1) = xt; positions_cart(p,2) = yt; positions_cart(p,3) = zt;
    end ; positions = positions_cart;

    stage{s} = positions ; s=s+1 ;
end

% ======================================================================= %
% Read atom labels.
% ======================================================================= %
unix(' awk ''/pseudopotential/,/initialpos/'' vasprun.txt | awk ''{print NR "\t" $0}'' > .labels.txt ');
[o,labellines] = unix('grep -n ''<rc><c>'' .labels.txt | awk -F ":" ''{print $1}'' '); 
labellines = sscanf(labellines,'%d'); 

for i=1:size(labellines,1)
    [o,label] = unix(sprintf('awk "NR==%d" .labels.txt | awk  ''{print $3}'' | awk -F ''>'' ''{print $3}'' ',labellines(i))); 
    label = label(1:size(label,2)-1); labels{i} = label ;    
end ; unix(' rm -f .labels.txt ');

% ======================================================================= %
% Read MD energies.
% ======================================================================= %
disp('|| Reading MD energies......');
%  [o,energylines] = unix(' grep -n ''<i name="bandstr">'' vasprun.txt |  awk -F ":" ''{print ($1+4)}'' ');
%  energylines = sscanf(energylines,'%d'); energylines = reshape(energylines,2,size(energylines,1)/2)' ;
%  
%  [o,poscar_energy] = unix(sprintf('awk "NR==%d" vasprun.txt | awk  ''{print $3}'' ', energylines(1,2)));
%  poscar_energy = sscanf(poscar_energy,'%g') ;
%  
%  re=1;
%  for i=1:interval:size(energylines,1)
%      [o,energy] = unix(sprintf('awk "NR==%d" vasprun.txt | awk  ''{print $3}'' ', energylines(re,2))); 
%      energy = sscanf(energy,'%g') ; energies(re) = energy ; re = re + 1 ;
%  end ; 
%  
%  scaled_energies = energies - poscar_energy ; % energies = scaled_energies ;
%  
%  unix(' rm -f vasprun.txt ');
[o,energies] = unix(' grep F OSZICAR | awk -F "E0" ''{print $2}'' | awk ''{print $2}'' ');
energies = sscanf(energies,'%g'); energies = energies - min(energies) ;


%======================================================================= %
% Atomic properties
% ======================================================================= %
for a=1:ntype
switch labels{a}
case 'H';   ainfo{a}=[01,0.46,1.00000,0.80000,0.80000]; 
case 'He';  ainfo{a}=[02,1.22,0.98907,0.91312,0.81091]; 
case 'Li';  ainfo{a}=[03,1.57,0.52731,0.87953,0.45670]; 
case 'Be';  ainfo{a}=[04,1.12,0.37147,0.84590,0.48292]; 
case 'B';   ainfo{a}=[05,0.81,0.12490,0.63612,0.05948]; 
case 'C';   ainfo{a}=[06,0.77,0.50430,0.28659,0.16236]; 
case 'N';   ainfo{a}=[07,0.74,0.69139,0.72934,0.90280]; 
case 'O';   ainfo{a}=[08,0.74,0.99997,0.01328,0.00000]; 
case 'F';   ainfo{a}=[09,0.72,0.69139,0.72934,0.90280]; 
case 'Ne';  ainfo{a}=[10,1.60,0.99954,0.21788,0.71035];
case 'Na';  ainfo{a}=[11,1.91,0.97955,0.86618,0.23787];
case 'Mg';  ainfo{a}=[12,1.60,0.98773,0.48452,0.08470];
case 'Al';  ainfo{a}=[13,1.43,0.50718,0.70056,0.84062];
case 'Si';  ainfo{a}=[14,1.18,0.10596,0.23226,0.98096];
case 'P';   ainfo{a}=[15,1.10,0.75557,0.61256,0.76425];
case 'S';   ainfo{a}=[16,1.04,1.00000,0.98071,0.00000];
case 'Cl';  ainfo{a}=[17,0.99,0.19583,0.98828,0.01167];
case 'Ar';  ainfo{a}=[18,1.92,0.81349,0.99731,0.77075];
case 'K';   ainfo{a}=[19,2.35,0.63255,0.13281,0.96858];
case 'Ca';  ainfo{a}=[20,1.97,0.35642,0.58863,0.74498];
case 'Sc';  ainfo{a}=[21,1.64,0.71209,0.38930,0.67279];
case 'Ti';  ainfo{a}=[22,1.47,0.24705,0.71764,0.34902];
case 'V';   ainfo{a}=[23,1.35,0.90000,0.10000,0.00000];
case 'Cr';  ainfo{a}=[24,1.29,0.00000,0.00000,0.62000];
case 'Mn';  ainfo{a}=[25,1.37,0.66148,0.03412,0.62036];
case 'Fe';  ainfo{a}=[26,1.26,0.71051,0.44662,0.00136];
case 'Co';  ainfo{a}=[27,1.25,0.00000,0.00000,0.68666];
case 'Ni';  ainfo{a}=[28,1.25,0.72032,0.73631,0.74339];
case 'Cu';  ainfo{a}=[29,1.28,0.13390,0.28022,0.86606];
case 'Zn';  ainfo{a}=[30,1.37,0.56123,0.56445,0.50799];
case 'Ga';  ainfo{a}=[31,1.53,0.62292,0.89293,0.45486];
case 'Ge';  ainfo{a}=[32,1.22,0.49557,0.43499,0.65193];
case 'As';  ainfo{a}=[33,1.21,0.45814,0.81694,0.34249];
case 'Se';  ainfo{a}=[34,1.04,0.60420,0.93874,0.06122];
case 'Br';  ainfo{a}=[35,1.14,0.49645,0.19333,0.01076];
case 'Kr';  ainfo{a}=[36,1.98,0.98102,0.75805,0.95413];
case 'Rb';  ainfo{a}=[37,2.50,1.00000,0.00000,0.60000];
case 'Sr';  ainfo{a}=[38,2.15,0.00000,1.00000,0.15259];
case 'Y';   ainfo{a}=[39,1.82,0.40259,0.59739,0.55813];
case 'Zr';  ainfo{a}=[40,1.60,0.00000,1.00000,0.00000];
case 'Nb';  ainfo{a}=[41,1.47,0.29992,0.70007,0.46459];
case 'Mo';  ainfo{a}=[42,1.40,0.70584,0.52602,0.68925];
case 'Tc';  ainfo{a}=[43,1.35,0.80574,0.68699,0.79478];
case 'Ru';  ainfo{a}=[44,1.34,0.81184,0.72113,0.68089];
case 'Rh';  ainfo{a}=[45,1.34,0.80748,0.82205,0.67068];
case 'Pd';  ainfo{a}=[46,1.37,0.75978,0.76818,0.72454];
case 'Ag';  ainfo{a}=[47,1.44,0.72032,0.73631,0.74339];
case 'Cd';  ainfo{a}=[48,1.52,0.95145,0.12102,0.86354];
case 'In';  ainfo{a}=[49,1.67,0.84378,0.50401,0.73483];
case 'Sn';  ainfo{a}=[50,1.58,0.60764,0.56052,0.72926];
case 'Sb';  ainfo{a}=[51,1.41,0.84627,0.51498,0.31315];
case 'Te';  ainfo{a}=[52,1.37,0.67958,0.63586,0.32038];
case 'I';   ainfo{a}=[53,1.33,0.55914,0.12200,0.54453];
case 'Xe';  ainfo{a}=[54,2.18,0.60662,0.63218,0.97305];
case 'Cs';  ainfo{a}=[55,2.72,0.05872,0.99922,0.72578];
case 'Ba';  ainfo{a}=[56,2.24,0.11835,0.93959,0.17565];
case 'La';  ainfo{a}=[57,1.88,0.35340,0.77057,0.28737];
case 'Ce';  ainfo{a}=[58,1.82,0.82055,0.99071,0.02374];
case 'Pr';  ainfo{a}=[59,1.82,0.99130,0.88559,0.02315];
case 'Nd';  ainfo{a}=[60,1.82,0.98701,0.55560,0.02744];
case 'Pm';  ainfo{a}=[61,1.81,0.00000,0.00000,0.96000];
case 'Sm';  ainfo{a}=[62,1.81,0.99042,0.02403,0.49195];
case 'Eu';  ainfo{a}=[63,2.06,0.98367,0.03078,0.83615];
case 'Gd';  ainfo{a}=[64,1.79,0.75325,0.01445,1.00000];
case 'Tb';  ainfo{a}=[65,1.77,0.44315,0.01663,0.99782];
case 'Dy';  ainfo{a}=[66,1.77,0.19390,0.02374,0.99071];
case 'Ho';  ainfo{a}=[67,1.76,0.02837,0.25876,0.98608];
case 'Er';  ainfo{a}=[68,1.75,0.28688,0.45071,0.23043];
case 'Tm';  ainfo{a}=[69,1.00,0.00000,0.00000,0.88000];
case 'Yb';  ainfo{a}=[70,1.94,0.15323,0.99165,0.95836];
case 'Lu';  ainfo{a}=[71,1.72,0.15097,0.99391,0.71032];
case 'Hf';  ainfo{a}=[72,1.59,0.70704,0.70552,0.35090];
case 'Ta';  ainfo{a}=[73,1.47,0.71952,0.60694,0.33841];
case 'W';   ainfo{a}=[74,1.41,0.55616,0.54257,0.50178];
case 'Re';  ainfo{a}=[75,1.37,0.70294,0.69401,0.55789];
case 'Os';  ainfo{a}=[76,1.35,0.78703,0.69512,0.47379];
case 'Ir';  ainfo{a}=[77,1.36,0.78975,0.81033,0.45049];
case 'Pt';  ainfo{a}=[78,1.39,0.79997,0.77511,0.75068];
case 'Au';  ainfo{a}=[79,1.44,0.99628,0.70149,0.22106];
case 'Hg';  ainfo{a}=[80,1.55,0.82940,0.72125,0.79823];
case 'Tl';  ainfo{a}=[81,1.71,0.58798,0.53854,0.42649];
case 'Pb';  ainfo{a}=[82,1.75,0.32386,0.32592,0.35729];
case 'Bi';  ainfo{a}=[83,1.82,0.82428,0.18732,0.97211];
case 'Po';  ainfo{a}=[84,1.77,0.00000,0.00000,1.00000];
case 'At';  ainfo{a}=[85,0.62,0.00000,0.00000,1.00000];
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

% Plot POSCAR
disp('|| plotting......');
figure('Color',background_color) ; 
h1 = subplot(4,1,[1 3]) ;
positions = poscar ;
parfor a=1:size(positions,1)
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
       if (bond_length < 2.2)
           line( [pos1(1) pos2(1)], [pos1(2) pos2(2)], [pos1(3) pos2(3)] ,...
               'LineWidth',plot_scale/5,'LineStyle','-'); hold on;
       end
   end
end


axis equal ; axis off; view(azimuth,elevation) ; 
legend_text = ['step = ' num2str(1)] ; legend(legend_text,1) ; legend('boxon'),


h2 = subplot(4,1,4); 
plot((1:size(energies)),energies);
%xlim([ 1 niterations(1) ]); ylim([ min(energies) max(energies)]);
axis tight
xlabel('MD step ' , 'FontWeight','bold','FontSize',15,'FontName','Times',...
     'Color',[0.6 0.2 0]); 
ylabel('E_0 (eV) ', 'FontWeight','bold','FontSize',10,'FontName','Times',...
     'Color',[0.6 0.2 0]);   
 
 
frame = getframe(1); fim = frame2im(frame); [im,map] = rgb2ind(fim,256,'nodither');



stg=1; img=1;
for p=interval:interval:size(startlines,1)
cla(h1) ; h1 = subplot(4,1,[1 3]) ;
positions = stage{stg}(:,1:3) ;
parfor a=1:size(positions,1)
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
legend_text = ['step = ' num2str(p)] ; legend(legend_text,1) ; legend('boxon'),


frame = getframe(1); fim = frame2im(frame);
%  h = myaa; frame = getframe(1) ; close(h); fim = frame2im(frame);
im(:,:,1,img) = rgb2ind(fim,map,'nodither'); stg = stg + 1 ; img = img + 1 ;
end



cla(h1) ; h1 = subplot(4,1,[1 3]) ;
positions = contcar ;
parfor a=1:size(positions,1)
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
legend_text = ['FINAL POSITIONS ' ] ; legend(legend_text,1) ; legend('boxon'),


frame = getframe(1); fim = frame2im(frame);

im(:,:,1,img) = rgb2ind(fim,map,'nodither');


imwrite(im,map,'MD.gif','DelayTime',1,'LoopCount',1) ;

disp('|| FINISHED !');

end