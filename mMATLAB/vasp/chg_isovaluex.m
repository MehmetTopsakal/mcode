function chg_isovalue(plane,level_min,level_max,level_division)

disp('  ');
disp('  ');
disp('Usage:  chg_isovalue(plane,levelstep,level_min,level_max,level_division) ');
disp('  ');
disp('  ');

figure


if nargin < 4, level_division  = 100      ; end
if nargin < 3, level_max       = 1.00       ; end
if nargin < 2, level_min       = 0.00       ; end
if nargin < 1, plane           = 'xy'       ; end



% read CHGCAR
[lattice,atoms,positions,chg_matrix]=read_chg('CHGCAR'); [grid_x,grid_y,grid_z]=size(chg_matrix);


% grid positions
x_line_direct=0:1/grid_x:(1-(1/grid_x)); y_line_direct=0:1/grid_y:(1-(1/grid_y)); z_line_direct=0:1/grid_z:(1-(1/grid_z));
for z=1:grid_z
    for y=1:grid_y
        for x=1:grid_x
            g_positions{x,y,z}=[ x_line_direct(x) y_line_direct(y) z_line_direct(z)];
            xt = g_positions{x,y,z}(1)*lattice(1,1) + g_positions{x,y,z}(2)*lattice(2,1) + g_positions{x,y,z}(3)*lattice(3,1) ;
            yt = g_positions{x,y,z}(1)*lattice(1,2) + g_positions{x,y,z}(2)*lattice(2,2) + g_positions{x,y,z}(3)*lattice(3,2) ;
            zt = g_positions{x,y,z}(1)*lattice(1,3) + g_positions{x,y,z}(2)*lattice(2,3) + g_positions{x,y,z}(3)*lattice(3,3) ;
            g_positions_cart{x,y,z} = [xt yt zt];  end; end; end




 
% plot atoms
for p=1:size(positions,1) ;
xt = positions(p,1)*lattice(1,1) + positions(p,2)*lattice(2,1) + positions(p,3)*lattice(3,1) ;
yt = positions(p,1)*lattice(1,2) + positions(p,2)*lattice(2,2) + positions(p,3)*lattice(3,2) ;
zt = positions(p,1)*lattice(1,3) + positions(p,2)*lattice(2,3) + positions(p,3)*lattice(3,3) ;
positions_cart(p,1) = xt; positions_cart(p,2) = yt; positions_cart(p,3) = zt;
end ; positions = [positions_cart];



% empty plane matrices
xy_slide = zeros(grid_x,grid_y); xz_slide = zeros(grid_x,grid_z); yz_slide = zeros(grid_y,grid_z);









if plane=='xy' ; % project onto x-y plane >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

% plot latticetice vectors and atoms
line([0 lattice(1,1)], [0 lattice(1,2)], [0 lattice(1,3)],'LineStyle','-','Color','r'); hold on;
line([0 lattice(2,1)], [0 lattice(2,2)], [0 lattice(2,3)],'LineStyle','-','Color','g'); hold on;
line([0 lattice(3,1)], [0 lattice(3,2)], [0 lattice(3,3)],'LineStyle','-','Color','b'); hold on;

for a=1:size(positions,1)
    positionsx=positions(a,1) ; positionsy=positions(a,2) ; positionsz=positions(a,3) ; 
    plot3(positionsx,positionsy,positionsz,...
    'MarkerFaceColor','k','MarkerEdgeColor','k','Marker','o','MarkerSize',10,...
    'LineStyle','none'); hold on;
end
view([0 90]); 

% make projection
for z=1:grid_z
    for y=1:grid_y
        for x=1:grid_x

            XY_mesh(x,y)=g_positions_cart{x,y,1}(1); 
            YX_mesh(y,x)=g_positions_cart{x,y,1}(2);
            xy_slide(x,y)=xy_slide(x,y)+chg_matrix(x,y,z); 
end; end; end ; xy_slide = xy_slide/(grid_x*grid_y*grid_z); 

zLevs = [max(max(xy_slide))*level_min : (max(max(xy_slide))-min(min(xy_slide)))/level_division : max(max(xy_slide))*level_max ] ;
contour(XY_mesh,YX_mesh',xy_slide,zLevs,'LineWidth',2); 
box('on'); grid('on');  axis equal ; axis tight ; 
xlabel('Lattice-x') ; ylabel('Lattice-y') ; zlabel('Lattice-z') ; 
colorbar % colorbar('off');






elseif plane=='xz' ; % project onto x-z plane >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
%  
%  % plot latticetice vectors and atoms
%  line([0 lattice(1,1)], [0 lattice(1,2)], [0 lattice(1,3)],'LineStyle','-','Color','r'); hold on;
%  line([0 lattice(2,1)], [0 lattice(2,2)], [0 lattice(2,3)],'LineStyle','-','Color','g'); hold on;
%  line([0 lattice(3,1)], [0 lattice(3,2)], [0 lattice(3,3)],'LineStyle','-','Color','b'); hold on;
%  
%  for a=1:size(positions,1)
%      positionsx=positions(a,1) ; positionsy=positions(a,2) ; positionsz=positions(a,3) ; 
%      plot3(positionsx,positionsy,positionsz,...
%      'MarkerFaceColor','k','MarkerEdgeColor','k','Marker','o','MarkerSize',10,...
%      'LineStyle','none'); hold on;
%  end
%  view([90 0]); 

% make projection
for y=1:grid_y
    for x=1:grid_x
        for z=1:grid_z

            XZ_mesh(x,z)=g_positions_cart{x,1,z}(1); 
            ZX_mesh(z,x)=g_positions_cart{x,1,z}(3);
            xz_slide(x,z)=xz_slide(x,z)+chg_matrix(x,y,z); 
end; end; end ; xz_slide = xz_slide/(grid_x*grid_y*grid_z); 


zLevs = [max(max(xz_slide))*level_min : (max(max(xz_slide))-min(min(xz_slide)))/level_division : max(max(xz_slide))*level_max ] ;
contour(XZ_mesh,ZX_mesh',xz_slide,zLevs,'LineWidth',2); 
view([0 90]) ; box('on'); grid('on');  axis equal ; axis tight ; 
xlabel('Lattice-x') ; ylabel('Lattice-z') ; zlabel('Lattice-y') ; 
colorbar % colorbar('off');






elseif plane=='yz' ; % project onto y-z plane >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
%  
%  % plot latticetice vectors and atoms
%  line([0 lattice(1,1)], [0 lattice(1,2)], [0 lattice(1,3)],'LineStyle','-','Color','r'); hold on;
%  line([0 lattice(2,1)], [0 lattice(2,2)], [0 lattice(2,3)],'LineStyle','-','Color','g'); hold on;
%  line([0 lattice(3,1)], [0 lattice(3,2)], [0 lattice(3,3)],'LineStyle','-','Color','b'); hold on;
%  
%  for a=1:size(positions,1)
%      positionsx=positions(a,1) ; positionsy=positions(a,2) ; positionsz=positions(a,3) ; 
%      plot3(positionsx,positionsy,positionsz,...
%      'MarkerFaceColor','k','MarkerEdgeColor','k','Marker','o','MarkerSize',10,...
%      'LineStyle','none'); hold on;
%  end
%  view([90 0]); 

% make projection
for x=1:grid_x
    for y=1:grid_y
        for z=1:grid_z

            YZ_mesh(y,z)=g_positions_cart{1,y,z}(2); 
            ZY_mesh(z,y)=g_positions_cart{1,y,z}(3);
            yz_slide(y,z)=yz_slide(y,z)+chg_matrix(x,y,z); 
end; end; end ; yz_slide = yz_slide/(grid_x*grid_y*grid_z); 


zLevs = [max(max(yz_slide))*level_min : (max(max(yz_slide))-min(min(yz_slide)))/level_division : max(max(yz_slide))*level_max ] ;
contour(YZ_mesh,ZY_mesh',yz_slide,zLevs,'LineWidth',2); 
view([0 90]) ; box('on'); grid('on');  axis equal ; axis tight ; 
xlabel('Lattice-y') ; ylabel('Lattice-z') ; zlabel('Lattice-x') ; 
colorbar % colorbar('off');

end

filename = ['contour.eps'];
print( '-r250','-depsc',filename)


end

