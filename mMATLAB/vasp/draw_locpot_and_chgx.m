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



subplot(5,1,[1 2]) ;

plot(lattice,profile,'LineWidth',2,'Color',[0 0 1]); hold all ;
plot(lattice+(max(lattice)),profile,'LineWidth',2,'Color',[0 0 1]); hold all ; 
plot(positions,zeros(size(positions),1),'MarkerFaceColor',[1 0 0],'MarkerSize',8,'Marker','o','LineStyle','none'); hold all;
plot(positions+(max(lattice)),zeros(size(positions),1),'MarkerFaceColor',[1 0 0],'MarkerSize',8,'Marker','o','LineStyle','none'); hold all;
plot([0,max(lattice*2)],[0,0],'LineWidth',2,'LineStyle','-.','Color',[0 0.5 0]); grid on; hold all; % Fermi line
%ylim([(min(profile)-1) (1+max(profile)) ]);
ylim([-5 (1+max(profile)) ]);
xlim([1 (1+max(lattice*1.5)) ]);


%  xlabel(['\Phi_1 = ' num2str(workfunction1, '%.3f') ' , \Phi_2 = ' num2str(workfunction2, '%.3f') ' , \Phi_{1-2} = ' num2str(workfunction1-workfunction2, '%.3f') ' (eV)'],...
%  'FontWeight','bold','FontSize',14,'FontName','Times','Color',[0.6 0.2 0]);
ylabel(['V(z) (eV)'],'FontWeight','bold','FontSize',18,'FontName','Times','Color',[0.6 0.2 0]);
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


subplot(5,1,[3 4]) ;

plot(lattice,profile,'LineWidth',2,'Color',[0 0 1]); hold all ;
plot(lattice+(max(lattice)),profile,'LineWidth',2,'Color',[0 0 1]); hold all ; 
plot(positions,zeros(size(positions),1),'MarkerFaceColor',[1 0 0],'MarkerSize',8,'Marker','o','LineStyle','none'); hold all;
plot(positions+(max(lattice)),zeros(size(positions),1),'MarkerFaceColor',[1 0 0],'MarkerSize',8,'Marker','o','LineStyle','none'); hold all;
plot([0,max(lattice*2)],[0,0],'LineWidth',2,'LineStyle','-.','Color',[0 0.5 0]); grid on; hold all; % Fermi line
ylim([(min(profile)) (max(profile)*1.05) ]);
xlim([1 (1+max(lattice*1.5)) ]);


%  xlabel(['\Phi_1 = ' num2str(workfunction1, '%.3f') ' , \Phi_2 = ' num2str(workfunction2, '%.3f') ' , \Phi_{1-2} = ' num2str(workfunction1-workfunction2, '%.3f') ' (eV)'],...
%  'FontWeight','bold','FontSize',14,'FontName','Times','Color',[0.6 0.2 0]);
ylabel(['\lambda (e/Angst.)'],'FontWeight','bold','FontSize',18,'FontName','Times','Color',[0.6 0.2 0]);
% xlabel(['Heigth (A)'],'FontWeight','bold','FontSize',18,'FontName','Times','Color',[0.6 0.2 0]);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

subplot(5,1,5) ;

plot(lattice,profile,'LineWidth',2,'Color',[0 0 1]); hold all ;
plot(lattice+(max(lattice)),profile,'LineWidth',2,'Color',[0 0 1]); hold all ; 
plot(positions,zeros(size(positions),1),'MarkerFaceColor',[1 0 0],'MarkerSize',8,'Marker','o','LineStyle','none'); hold all;
plot(positions+(max(lattice)),zeros(size(positions),1),'MarkerFaceColor',[1 0 0],'MarkerSize',8,'Marker','o','LineStyle','none'); hold all;
plot([0,max(lattice*2)],[0,0],'LineWidth',2,'LineStyle','-.','Color',[0 0.5 0]); grid on; hold all; % Fermi line
ylim([(min(profile)) 0.00015 ]); % ylim([(min(profile)) (1+max(profile))/2000 ]);
xlim([1 (1+max(lattice*1.5)) ]);



%  xlabel(['\Phi_1 = ' num2str(workfunction1, '%.3f') ' , \Phi_2 = ' num2str(workfunction2, '%.3f') ' , \Phi_{1-2} = ' num2str(workfunction1-workfunction2, '%.3f') ' (eV)'],...
%  'FontWeight','bold','FontSize',14,'FontName','Times','Color',[0.6 0.2 0]);
ylabel(['\lambda (e/A)'],'FontWeight','bold','FontSize',18,'FontName','Times','Color',[0.6 0.2 0]);
xlabel(['Heigth (A)'],'FontWeight','bold','FontSize',18,'FontName','Times','Color',[0.6 0.2 0]);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%




print -depsc LOCPOT_and_CHG.eps