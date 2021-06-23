function draw_dos(energy_limit_down,energy_limit_up) 
%
% usage example :
%
if nargin < 2,  energy_limit_down=-5; end
if nargin < 1,  energy_limit_up=5; end


[s,line1] = unix(' awk "NR==1" DOSCAR ');
line1 = sscanf(line1,'%d');

[s,line6] = unix(' awk "NR==6" DOSCAR ');
line6 = sscanf(line6,'%g'); efermi=line6(4);

[s,line7] = unix(' awk "NR==7" DOSCAR ');
line7 = sscanf(line7,'%g');


if size(line7,1)==3 % ISPIN = 1 case

[o,tdos] = unix(sprintf('awk "NR==7,NR==%d" DOSCAR ',line6(3)+6));
tdos = sscanf(tdos,'%f',[3 line6(3)]); tdos = tdos';

energy=tdos(:,1) ; dos=tdos(:,2);

figure('Color','w'); %subplot(2,1,1);
%  plot(energy-efermi,dos,'-o','Color','r','LineWidth',2,'MarkerEdgeColor','b','MarkerFaceColor','b', 'MarkerSize',1); grid on;
%  %legend_text = ['Total DOS'] ; legend(legend_text,1) ; legend('boxon'); hold on
%  title(' Total DOS ','FontWeight','bold','FontSize',15,'FontName','Times','Color',[0.6 0.2 0]);
%  xlabel('Energy (eV)','FontWeight','bold','FontSize',15,'FontName','Times','Color',[0.6 0.2 0]);
%  ylabel('States / eV','FontWeight','bold','FontSize',15,'FontName','Times','Color',[0.6 0.2 0]);
%  axis tight;

subplot(2,1,2);
plot(energy-efermi,dos,'-o','Color','r','LineWidth',2,'MarkerEdgeColor','b','MarkerFaceColor','b', 'MarkerSize',1); grid on;
%legend_text = ['Total DOS'] ; legend(legend_text,1) ; legend('boxon'); hold on
%title(' Total DOS ','FontWeight','bold','FontSize',15,'FontName','Times','Color',[0.6 0.2 0]);
xlabel('Energy (eV)','FontWeight','bold','FontSize',15,'FontName','Times','Color',[0.6 0.2 0]);
ylabel('States / eV','FontWeight','bold','FontSize',15,'FontName','Times','Color',[0.6 0.2 0]);
xlim([energy_limit_down energy_limit_up]);


else % ISPIN = 2 case

[o,tdos] = unix(sprintf('awk "NR==7,NR==%d" DOSCAR ',line6(3)+6));
tdos = sscanf(tdos,'%f',[5 line6(3)]); tdos = tdos';

energy=tdos(:,1) ; dosup=tdos(:,2); dosdown=tdos(:,3);

figure('Color','w'); %subplot(2,1,1);
%  plot(energy-efermi,dosup,'-o','Color','r','LineWidth',2,'MarkerEdgeColor','r','MarkerFaceColor','r', 'MarkerSize',2); grid on; hold on
%  plot(energy-efermi,-dosdown,'-o','Color','b','LineWidth',2,'MarkerEdgeColor','b','MarkerFaceColor','b', 'MarkerSize',2); grid on;
%  legend('DOS-up','DOS-down',1) ; legend('boxoff'); hold on
%  title(' Total DOS (up+down) ','FontWeight','bold','FontSize',15,'FontName','Times','Color',[0.6 0.2 0]);
%  xlabel('Energy (eV)','FontWeight','bold','FontSize',15,'FontName','Times','Color',[0.6 0.2 0]);
%  ylabel('States / eV','FontWeight','bold','FontSize',15,'FontName','Times','Color',[0.6 0.2 0]);
%  xlim([min(energy-efermi)*0.9 max(energy-efermi)*0.9]);% axis tight; 

subplot(2,1,2);
plot(energy-efermi,dosup+dosdown,'-o','Color','r','LineWidth',2,'MarkerEdgeColor','b','MarkerFaceColor','b', 'MarkerSize',1); grid on;
%plot(energy-efermi,-dosdown,'-o','Color','b','LineWidth',2,'MarkerEdgeColor','b','MarkerFaceColor','b', 'MarkerSize',2); grid on;
legend('DOS-up','DOS-down',1) ; legend('boxoff'); hold on
%title(' Total DOS (up+down) ','FontWeight','bold','FontSize',15,'FontName','Times','Color',[0.6 0.2 0]);
xlabel('Energy (eV)','FontWeight','bold','FontSize',15,'FontName','Times','Color',[0.6 0.2 0]);
ylabel('States / eV','FontWeight','bold','FontSize',15,'FontName','Times','Color',[0.6 0.2 0]);
xlim([energy_limit_down energy_limit_up]);% 

end


print -depsc dos.eps

end

%  
%  
%  
%  
%  
%  
%  
%  ndos=1000;
%  
%  natoms=( 127 +  2 + 62 );
%  
%  
%  ! cat DOSCAR | awk "NF==10"  | awk '{print $1}'  > E
%  ! cat DOSCAR | awk "NF==10"  | awk '{print $2}'  >  S_DOS
%  ! cat DOSCAR | awk "NF==10"  | awk '{print $3}'  > PX_DOS
%  ! cat DOSCAR | awk "NF==10"  | awk '{print $4}'  > PY_DOS
%  ! cat DOSCAR | awk "NF==10"  | awk '{print $5}'  > PZ_DOS
%  
%  
%  E=load('E'); Energy=reshape(E,ndos,natoms); Energy=Energy(:,1);
%  
%  
%  % s-orbital DOS %%%%%%%%%%%%%%%%%%%%%%%%%%
%  S_DOSdata=load('S_DOS'); S_DOS1=reshape(S_DOSdata,ndos,natoms);
%  
%  for s=1:ndos
%  SDOS(s)=(sum(S_DOS1(s,:)));
%  end
%  
%  SDOS=reshape(SDOS,ndos,1) ; SDOS=[Energy, SDOS];
%  
%  save -ascii s-dos.dat SDOS
%  
%  % px-orbital DOS %%%%%%%%%%%%%%%%%%%%%%%%%%
%  PX_DOSdata=load('PX_DOS'); PX_DOS1=reshape(PX_DOSdata,ndos,natoms);
%  
%  for px=1:ndos
%  PXDOS(px)=(sum(PX_DOS1(px,:)));
%  end
%  
%  PXDOS=reshape(PXDOS,ndos,1) ; PXDOS=[Energy, PXDOS];
%  
%  save -ascii px-dos.dat PXDOS
%  
%  % py-orbital DOS %%%%%%%%%%%%%%%%%%%%%%%%%%
%  PY_DOSdata=load('PY_DOS'); PY_DOS1=reshape(PY_DOSdata,ndos,natoms);
%  
%  for py=1:ndos
%  PYDOS(py)=(sum(PY_DOS1(py,:)));
%  end
%  
%  PYDOS=reshape(PYDOS,ndos,1) ; PYDOS=[Energy, PYDOS];
%  
%  save -ascii py-dos.dat PYDOS
%  
%  % py-orbital DOS %%%%%%%%%%%%%%%%%%%%%%%%%%
%  PZ_DOSdata=load('PZ_DOS'); PZ_DOS1=reshape(PZ_DOSdata,ndos,natoms);
%  
%  for pz=1:ndos
%  PZDOS(pz)=(sum(PZ_DOS1(pz,:)));
%  end
%  
%  PZDOS=reshape(PZDOS,ndos,1) ; PZDOS=[Energy, PZDOS];
%  
%  
%  save -ascii pz-dos.dat PZDOS
%  
%  ! rm -rf E S_DOS PX_DOS PY_DOS PZ_DOS

