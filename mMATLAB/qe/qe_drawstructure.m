function qe_drawstructure(file,az,el,mind)
%
% usage example qe_drawstructure('scf.out',0,0,0.15)
%

% read file
%  [lat,pos]=read_poscar(file);
[celldm,lattice,positions]=qe_readlattice(file)

% plot lattice
figure('Color','w')

line([0 lattice(1,1)], [0 lattice(1,2)], [0 lattice(1,3)],'LineStyle','-','Color','r'); hold on;
line([0 lattice(2,1)], [0 lattice(2,2)], [0 lattice(2,3)],'LineStyle','-','Color','g'); hold on;
line([0 lattice(3,1)], [0 lattice(3,2)], [0 lattice(3,3)],'LineStyle','-','Color','b'); hold on;

% plot positionsitions
for a=1:size(positions,1)
    positionsx=positions(a,1) ; positionsy=positions(a,2) ; positionsz=positions(a,3) ;
    plot3(positionsx,positionsy,positionsz,...
    'MarkerFaceColor','r','MarkerEdgeColor','g','Marker','o','MarkerSize',6*1,...
    'LineStyle','none'); hold on;
end

% plot bonds
for ii=1:size(positions)
    for jj=1:size(positions)
    positions1=positions(ii,1:3); positions2=positions(jj,1:3); bond_length=norm(positions1-positions2);
    if (bond_length < mind); line( [positions1(1) positions2(1)], [positions1(2) positions2(2)], [positions1(3) positions2(3)] ,...
    'LineStyle','-','LineWidth',1); hold on;
end; end; end
%  legend
% axes
axis equal ; axis off; grid on ; box on; view(az,el); 



% export figure
filename = [file '.eps']; print( '-r250','-depsc',filename)

end

