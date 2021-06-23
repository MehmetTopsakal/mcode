function draw_locpot(p_up,p_down)
%
% usage 
%

if nargin < 2,   p_down =  0.85     ; end
if nargin < 1,   p_up   =  0.15     ; end


% read LOCPOT file
[lattice,atoms,positions,chg_matrix]=read_chg('LOCPOT') ; 
[grid_x,grid_y,grid_z]=size(chg_matrix);

% extract fermi energy from DOSCAR
[s,fermi] = unix('awk "NR==6" DOSCAR | awk ''{print $4}''');
fermi = sscanf(fermi,'%f') ;

% local potential along z-axis.
lattice_z = 0:lattice(3,3)/(grid_z-1):lattice(3,3) ;
positions_z = positions(:,3)*lattice(3,3);

lattice=lattice_z ; positions=positions_z;


% average LOCPOT in x-y directions.
sumxy = sum(sum(chg_matrix,1),2) ; 
profile = reshape(sumxy(1,1,:),grid_z,1)/(grid_x*grid_y)-fermi ;




% vacuum energy
vacuum1=round(size(profile,1)*p_up); vacuum2=round(size(profile,1)*p_down); 
workfunction1=profile(vacuum1) ;
workfunction2=profile(vacuum2) ;



% plots
figure; subplot(2,1,1) ;
 
plot(lattice,profile,'LineWidth',2 ); hold all ; 
plot(positions,zeros(size(positions))+min(profile)-0.25,'MarkerFaceColor',[1 0 0],'MarkerSize',7,'Marker','o','LineStyle','none'); hold all;
plot([0,max(lattice)],[0,0],'LineWidth',2,'LineStyle','-.','Color',[0 0.5 0]); grid on; hold all; % Fermi line
xlabel(['height (A)'],'FontWeight','bold','FontSize',18,'FontName','Times','Color',[0.6 0.2 0]);
ylabel(['Energy (eV)'],'FontWeight','bold','FontSize',18,'FontName','Times','Color',[0.6 0.2 0]);

axis([ 0 max(lattice) min(profile-1) max(profile+2)])

subplot(2,1,2) ;
 
%plot(lattice,profile,'LineWidth',2 ); hold all ; 
profile_s=smooth(lattice,profile,0.06,'rloess'); plot(lattice,profile_s,'LineWidth',2 ); hold all ; 
plot(positions,zeros(size(positions))-0,'MarkerFaceColor',[1 0 0],'MarkerSize',7,'Marker','o','LineStyle','none'); hold all;
plot([0,max(lattice)],[0,0],'LineWidth',2,'LineStyle','-.','Color',[0 0.5 0]); grid on; hold all; % Fermi line
plot(max(lattice)*(vacuum1/size(profile,1)),workfunction1,'Marker','.','Color',[0 0.5 0],'MarkerSize',20); % 
plot(max(lattice)*(vacuum2/size(profile,1)),workfunction2,'Marker','.','Color',[0 0.5 0],'MarkerSize',20); % 
%axis([0 max(lattice) 2.6 4.2 ]) 
axis([0 max(lattice) -0.5 max(profile+0.1) ])


xlabel(['\Phi_1 = ' num2str(workfunction1, '%.3f') ' , \Phi_2 = ' num2str(workfunction2, '%.3f') ' , \Phi_{1-2} = ' num2str(workfunction1-workfunction2, '%.3f') ' (eV)'],...
'FontWeight','bold','FontSize',14,'FontName','Times','Color',[0.6 0.2 0]);
ylabel(['Energy (eV)'],'FontWeight','bold','FontSize',18,'FontName','Times','Color',[0.6 0.2 0]);


print -dpdf LOCPOT.eps

end % function
