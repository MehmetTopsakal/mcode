clear all ; figure ; 

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
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


subplot(3,1,1) ;

plot(lattice,profile,'LineWidth',2 ); hold all ; 
plot(positions,zeros(size(positions),1),'MarkerFaceColor',[1 0 0],'MarkerSize',10,'Marker','o','LineStyle','none'); hold all;
plot([0,max(lattice)],[0,0],'LineWidth',2,'LineStyle','-.','Color',[0 0.5 0]); grid on; hold all; % Fermi line
axis([0 max(lattice) min(profile)*0.3 max(profile+0.5) ])


%  xlabel(['\Phi_1 = ' num2str(workfunction1, '%.3f') ' , \Phi_2 = ' num2str(workfunction2, '%.3f') ' , \Phi_{1-2} = ' num2str(workfunction1-workfunction2, '%.3f') ' (eV)'],...
%  'FontWeight','bold','FontSize',14,'FontName','Times','Color',[0.6 0.2 0]);
ylabel(['Energy (eV)'],'FontWeight','bold','FontSize',18,'FontName','Times','Color',[0.6 0.2 0]);
% xlabel(['Heigth (A)'],'FontWeight','bold','FontSize',18,'FontName','Times','Color',[0.6 0.2 0]);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

[lattice,atoms,positions,chg_matrix]=read_chg('CHGCAR') ; 
[grid_x,grid_y,grid_z]=size(chg_matrix);
% local potential along z-axis.
lattice_z = 0:lattice(3,3)/(grid_z-1):lattice(3,3) ;
positions_z = positions(:,3)*lattice(3,3);
lattice=lattice_z ; positions=positions_z;
% average LOCPOT in x-y directions.
sumxy = sum(sum(chg_matrix,1),2) ; 
profile = reshape(sumxy(1,1,:),grid_z,1)/(grid_x*grid_y*grid_z) ;


subplot(3,1,2) ;

plot(lattice,profile,'LineWidth',2 ); hold all ; 
plot(positions,zeros(size(positions),1),'MarkerFaceColor',[1 0 0],'MarkerSize',10,'Marker','o','LineStyle','none'); hold all;
plot([0,max(lattice)],[0,0],'LineWidth',2,'LineStyle','-.','Color',[0 0.5 0]); grid on; hold all; % Fermi line
axis([0 max(lattice) -0.25 max(profile+0.5) ])


%  xlabel(['\Phi_1 = ' num2str(workfunction1, '%.3f') ' , \Phi_2 = ' num2str(workfunction2, '%.3f') ' , \Phi_{1-2} = ' num2str(workfunction1-workfunction2, '%.3f') ' (eV)'],...
%  'FontWeight','bold','FontSize',14,'FontName','Times','Color',[0.6 0.2 0]);
ylabel(['Energy (eV)'],'FontWeight','bold','FontSize',18,'FontName','Times','Color',[0.6 0.2 0]);
% xlabel(['Heigth (A)'],'FontWeight','bold','FontSize',18,'FontName','Times','Color',[0.6 0.2 0]);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

subplot(3,1,3) ;

plot(lattice,profile,'LineWidth',2 ); hold all ; 
plot(positions,zeros(size(positions),1),'MarkerFaceColor',[1 0 0],'MarkerSize',10,'Marker','o','LineStyle','none'); hold all;
plot([0,max(lattice)],[0,0],'LineWidth',2,'LineStyle','-.','Color',[0 0.5 0]); grid on; hold all; % Fermi line
axis([0 max(lattice) -0.25 max(profile)/1000 ])


%  xlabel(['\Phi_1 = ' num2str(workfunction1, '%.3f') ' , \Phi_2 = ' num2str(workfunction2, '%.3f') ' , \Phi_{1-2} = ' num2str(workfunction1-workfunction2, '%.3f') ' (eV)'],...
%  'FontWeight','bold','FontSize',14,'FontName','Times','Color',[0.6 0.2 0]);
ylabel(['Energy (eV)'],'FontWeight','bold','FontSize',18,'FontName','Times','Color',[0.6 0.2 0]);
xlabel(['Heigth (A)'],'FontWeight','bold','FontSize',18,'FontName','Times','Color',[0.6 0.2 0]);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%




print -depsc LOCPOT_and_CHG.eps