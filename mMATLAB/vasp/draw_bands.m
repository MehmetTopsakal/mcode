function draw_bands(ymin,ymax,format)
%
% usage 
%

if nargin < 3, format =  0      ; end
if nargin < 2,   ymax =  6      ; end
if nargin < 1,   ymin = -6      ; end

figure

[s,nspin] = unix('grep ISPIN OUTCAR | awk ''{print $3}''');
nspin = sscanf(nspin,'%d') ;

%  [s,kline] = unix('grep  NKPTS OUTCAR | awk ''{print $4"  "$15}''');
%  [kline,c] = sscanf(kline,'%d') ; nkpoints = kline(1) ; nbands = kline(2) ;

[s,nkpoints] = unix('grep  NKPTS OUTCAR | awk ''{print $4}''');
nkpoints = sscanf(nkpoints,'%d') ;

[s,nbands] = unix('grep  NKPTS OUTCAR | awk ''{print $NF}''');
nbands = sscanf(nbands,'%d') ;

[s,efline] = unix('grep -n " E-fermi :" OUTCAR  | awk ''END{print}'' | awk ''{print $1 "  " $4 }'' | awk -F ":" ''{print $1"  "$2}''');
[efline,c] = sscanf(efline,'%f') ; fermi = efline(2) ; efline = efline(1) ;


if  nspin==1 ; % ISPIN = 1 case
    
    elstart = efline+3 ; elstop  = nkpoints*(nbands+3)+1 ;
    fid = fopen('limits.tmp', 'w'); fprintf(fid, '%d %d', [elstart,elstop]); fclose(fid); 
    unix('awk "NR>=`cat limits.tmp | awk ''{print $1}''`" OUTCAR | awk "NR<=`cat limits.tmp | awk ''{print $2}''`" > data.tmp');
    unix(' rm -f limits.tmp ') ; % we can avoid this file as we did for kpoints....
    fid = fopen('data.tmp', 'r');
    for kp=1:nkpoints
        null = fscanf(fid,'%s', 3); kpoints_path(kp,:) = fscanf (fid, '%g', [1 3]); null = fscanf(fid,'%s', 5);
        readdata = fscanf(fid,'%f', [3 nbands]); readdata = readdata' ;
        energy(:,kp) = readdata(:,2); occupation(:,kp) = readdata(:,3);
    end
    fclose(fid); unix('rm -f data.tmp') ;
    

[s,nelectrons] = unix('grep NELECT OUTCAR | awk ''{print $3}''');
nelectrons = sscanf(nelectrons,'%d') ;

% define K-points path %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% we need kpoints in reciprocal positions so:
[a,kpoints_path] = unix('awk ''/ k-points in units of 2pi/, / k-points in reciprocal lattice and weights:/'' OUTCAR | awk "NF==4" | awk ''{print $1 "  " $2 "   " $3  }'' ');
kpoints_path = sscanf(kpoints_path,'%g', [3 nkpoints] ) ; kpoints_path = kpoints_path' ;

kpoints_track(1) = 0 ;
for k=1:size(kpoints_path,1)-1; k0=kpoints_path(k,:); k1=kpoints_path(k+1,:);
    dx=k0(1)-k1(1); dy=k0(2)-k1(2); dz=k0(3)-k1(3);
    kpoints_track(k+1) = kpoints_track(k) + sqrt(dx*dx+dy*dy+dz*dz);
end

 
% Find bandgap value %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
n_valance_band=nelectrons/2;
valance_band=energy(n_valance_band:n_valance_band,:);
conductance_band=energy(n_valance_band+1:n_valance_band+1,:);
BandGap=min(conductance_band)-max(valance_band);
%shift=max(valance_band)+(BandGap/2);

% Find energy bounds %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


% Plot first band figure %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
subplot(1,3,1) ;
shift=fermi;
for i=1:nbands;
    plot(kpoints_track,energy(i,:)-shift,'Marker','*','MarkerFaceColor',...
        [1 0 0],'MarkerEdgeColor',[0 0 1],'MarkerSize',2,'LineWidth',2,...
        'LineStyle','-','Color',[1 0 0]); hold on ;
end

% Create fermi line
fermil(1:nkpoints,1)=0; plot(kpoints_track,fermil,'LineWidth',2,...
    'LineStyle','-.','Color',[0 0.5 0]);
xlim([0 max(kpoints_track)]);
highest_energy=max(energy(nbands,:))-shift+1 ; lowest_energy=min(energy(1,:))-shift-1;
ylim([(lowest_energy) (highest_energy)]);
set(gca,'XTick',zeros(1,0));
% Create ylabels
ylabel('Energy (eV)','FontWeight','bold','FontSize',18,'FontName','Times',...
    'Color',[0.6 0.2 0]);
band_gap_text = ['E_g = ' num2str(BandGap)];
xlabel(band_gap_text,'FontWeight','bold','FontSize',18,'FontName','Times',...
    'Color',[0.6 0.2 0]);
%xlim([0 max(kpoints_track)]);
%ylim([ymin ymax]);


% Plot second band figure %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
subplot(1,3,2) ;
shift=fermi;
for i=1:nbands;
    plot(kpoints_track,energy(i,:)-shift,'Marker','*','MarkerFaceColor',...
        [1 0 0],'MarkerEdgeColor',[0 0 1],'MarkerSize',2,'LineWidth',2,...
        'LineStyle','-','Color',[1 0 0]); hold on ;
end

% Create fermi line
fermil(1:nkpoints,1)=0; plot(kpoints_track,fermil,'LineWidth',2,...
    'LineStyle','-.','Color',[0 0.5 0]);
xlim([0 max(kpoints_track)]);
highest_energy=max(energy(nbands,:))-shift+1 ; lowest_energy=min(energy(1,:))-shift-1;
ylim([(lowest_energy) (highest_energy)]);
set(gca,'XTick',zeros(1,0));
% Create ylabels
ylabel('Energy (eV)','FontWeight','bold','FontSize',18,'FontName','Times',...
    'Color',[0.6 0.2 0]);
band_gap_text = ['E_g = ' num2str(BandGap)];
xlabel(band_gap_text,'FontWeight','bold','FontSize',18,'FontName','Times',...
    'Color',[0.6 0.2 0]);
xlim([0 max(kpoints_track)]);
ylim([ymin ymax]);


% Plot third band figure %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
subplot(1,3,3) ;
shift=max(valance_band)+(BandGap/2);
for i=1:nbands;
    plot(kpoints_track,energy(i,:)-shift,'Marker','*','MarkerFaceColor',...
        [1 0 0],'MarkerEdgeColor',[0 0 1],'MarkerSize',4,'LineWidth',2,...
        'LineStyle','-','Color',[1 0 0]); hold on ;
end

% Create fermi line
fermil(1:nkpoints,1)=0; plot(kpoints_track,fermil,'LineWidth',2,...
    'LineStyle','-.','Color',[0 0.5 0]);
xlim([0 max(kpoints_track)]);
ylim([ymin ymax]);
set(gca,'XTick',zeros(1,0));
% Create ylabels
ylabel('Energy (eV)','FontWeight','bold','FontSize',18,'FontName','Times',...
    'Color',[0.6 0.2 0]);
band_gap_text = ['E_g = ' num2str(BandGap)];
xlabel(band_gap_text,'FontWeight','bold','FontSize',18,'FontName','Times',...
    'Color',[0.6 0.2 0]);


%  % if someone needs vertical lines for special points....
%  special_point_M = [
%  kpoints_track(20),(ymin)-1
%  kpoints_track(20),(ymax)+1
%  ] ; plot(special_point_M(:,1),special_point_M(:,2),'LineWidth',1,'Color',[1 0 0]); hold on ;
%  
%  special_point_K = [
%  kpoints_track(40),(ymin)-1
%  kpoints_track(40),(ymax)+1
%  ] ; plot(special_point_K(:,1),special_point_K(:,2),'LineWidth',1,'Color',[1 0 0]); hold on ;



unix('> bands.dat');

shift=fermi;
for b=1:nbands
bdata= [kpoints_track' (energy(b,:)-shift)'];
save -ascii bdata.tmp bdata
unix('cat bdata.tmp >> bands.dat'); 
unix('echo " " >> bands.dat'); 
end

unix('rm bdata.tmp');


filename = ['bands.ps']; print( '-r250','-depsc2',filename)    
    
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%     
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  


else           % ISPIN = 2 case
    
    elstart = efline+5 ; elstop  = 2*nkpoints*(nbands+3)+1 ;
    fid = fopen('limits.tmp', 'w'); fprintf(fid, '%d %d', [elstart,elstop]); fclose(fid);
    unix('awk "NR>=`cat limits.tmp | awk ''{print $1}''`" OUTCAR | awk "NR<=`cat limits.tmp | awk ''{print $2}''`" > data.tmp');
    unix(' rm -f limits.tmp ') ; % we can avoid this file as we did for kpoints....
    fid = fopen('data.tmp', 'r');
    for kp=1:nkpoints
        null = fscanf(fid,'%s', 3); kpoints_path(kp,:) = fscanf (fid, '%g', [1 3]); null = fscanf(fid,'%s', 5);
        readdata = fscanf(fid,'%f', [3 nbands]); readdata = readdata' ;
        energy_up(:,kp) = readdata(:,2); occupation_up(:,kp) = readdata(:,3);
    end
    null = fscanf(fid,'%s', 3);
    for kp=1:nkpoints
        null = fscanf(fid,'%s', 3); kpoints_path(kp,:) = fscanf (fid, '%g', [1 3]); null = fscanf(fid,'%s', 5);
        readdata = fscanf(fid,'%f', [3 nbands]); readdata = readdata' ;
        energy_down(:,kp) = readdata(:,2); occupation_down(:,kp) = readdata(:,3);
    end
    fclose(fid); unix('rm -f data.tmp') ;
    
    
% define K-points path %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% we need kpoints in reciprocal positions so:
[a,kpoints_path] = unix('awk ''/ k-points in units of 2pi/, / k-points in reciprocal lattice and weights:/'' OUTCAR | awk "NF==4" | awk ''{print $1 "  " $2 "   " $3  }'' ');
kpoints_path = sscanf(kpoints_path,'%g', [3 nkpoints] ) ; kpoints_path = kpoints_path' ;

kpoints_track(1) = 0 ;
for k=1:size(kpoints_path,1)-1; k0=kpoints_path(k,:); k1=kpoints_path(k+1,:);
    dx=k0(1)-k1(1); dy=k0(2)-k1(2); dz=k0(3)-k1(3);
    kpoints_track(k+1) = kpoints_track(k) + sqrt(dx*dx+dy*dy+dz*dz);
end


subplot(1,3,1) ; %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

for i=1:nbands;
    plot(kpoints_track,energy_up(i,:)-fermi,'Marker','*','MarkerFaceColor',...
        [1 0 0],'MarkerEdgeColor',[1 0 0],'MarkerSize',1,'LineWidth',2,...
        'LineStyle','-','Color',[1 0 0]); hold on ;
end

for i=1:nbands;
    plot(kpoints_track,energy_down(i,:)-fermi,'Marker','.','MarkerFaceColor',...
        [0 0 1],'MarkerEdgeColor',[0 0 1],'MarkerSize',1,'LineWidth',2,...
        'LineStyle','-.','Color',[0 0 1]); hold on ;
end

% Create fermi line
fermil(1:nkpoints,1)=0; plot(kpoints_track,fermil,'LineWidth',2,...
    'LineStyle','-.','Color',[0 0.5 0]);
xlim([0 max(kpoints_track)]); %ylim([ymin ymax]);
set(gca,'XTick',zeros(1,0));
ylabel('Energy (eV)','FontWeight','bold','FontSize',18,'FontName','Times',...
    'Color',[0.6 0.2 0]);
text = ['Spin up+down'];
xlabel(text,'FontWeight','bold','FontSize',15,'FontName','Times',...
    'Color',[0.6 0.2 0]);


subplot(1,3,2) ; %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

for i=1:nbands;
    plot(kpoints_track,energy_up(i,:)-fermi,'Marker','*','MarkerFaceColor',...
        [1 0 0],'MarkerEdgeColor',[1 0 0],'MarkerSize',1,'LineWidth',2,...
        'LineStyle','-','Color',[1 0 0]); hold on ;
end

% find UP band gap
vumin=1 ; cumin=1 ;
for ub=1:nbands;
minub(ub)=min(energy_up(ub,:)-fermi);
       if minub(ub) < 0;
           valance_umins(vumin)=minub(ub); vumin = vumin+1 ;
       else conduction_umins(cumin)=minub(ub); cumin = cumin+1 ;
   end
end

vumax=1 ; cumax=1 ;
for ub=1:nbands;
maxub(ub)=max(energy_down(ub,:)-fermi);
       if maxub(ub) < 0;
           valance_umaxs(vumax)=maxub(ub); vumax = vumax+1 ;
       else conduction_umaxs(cumax)=maxub(ub); cumax = cumax+1 ;
   end
end

up_band_gap=min(conduction_umins)-max(valance_umaxs);


% Create fermi line
fermil(1:nkpoints,1)=0; plot(kpoints_track,fermil,'LineWidth',2,...
    'LineStyle','-.','Color',[0 0.5 0]);
xlim([0 max(kpoints_track)]);
ylim([ymin ymax]);
set(gca,'XTick',zeros(1,0));
band_gap_text = ['E_g(up) = ' num2str(up_band_gap)];
xlabel(band_gap_text,'FontWeight','bold','FontSize',12,'FontName','Times',...
    'Color',[0.6 0.2 0]);


subplot(1,3,3) ; %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


for i=1:nbands;
    plot(kpoints_track,energy_down(i,:)-fermi,'Marker','*','MarkerFaceColor',...
        [0 0 1],'MarkerEdgeColor',[0 0 1],'MarkerSize',1,'LineWidth',2,...
        'LineStyle','-.','Color',[0 0 1]); hold on ;
end

% find DOWN band gap
vdmin=1 ; cdmin=1 ;
for db=1:nbands;
mindb(db)=min(energy_down(db,:)-fermi);
       if mindb(db) < 0;
           valance_dmins(vdmin)=mindb(db); vdmin = vumin+1 ;
       else conduction_dmins(cdmin)=mindb(db); cdmin = cdmin+1 ;
   end
end

vdmax=1 ; cdmax=1 ;
for db=1:nbands;
maxdb(db)=max(energy_down(db,:)-fermi);
       if maxdb(db) < 0;
           valance_dmaxs(vdmax)=maxdb(db); vdmax = vdmax+1 ;
       else conduction_dmaxs(cdmax)=maxdb(db); cdmax = cdmax+1 ;
   end
end

down_band_gap=min(conduction_dmins)-max(valance_dmaxs);

% Create fermi line
fermil(1:nkpoints,1)=0; plot(kpoints_track,fermil,'LineWidth',2,...
    'LineStyle','-.','Color',[0 0.5 0]);
xlim([0 max(kpoints_track)]);
ylim([ymin ymax]);
set(gca,'XTick',zeros(1,0));
band_gap_text = ['E_g(down) = ' num2str(down_band_gap)];
xlabel(band_gap_text,'FontWeight','bold','FontSize',12,'FontName','Times',...
    'Color',[0.6 0.2 0]);

%  % if someone needs vertical lines for special points....
%  special_point_M = [
%  kpoints_track(20),(ymin)-1
%  kpoints_track(20),(ymax)+1
%  ] ; plot(special_point_M(:,1),special_point_M(:,2),'LineWidth',1,'Color',[1 0 0]); hold on ;
%  
%  special_point_K = [
%  kpoints_track(40),(ymin)-1
%  kpoints_track(40),(ymax)+1
%  ] ; plot(special_point_K(:,1),special_point_K(:,2),'LineWidth',1,'Color',[1 0 0]); hold on ;

filename = ['bands.ps']; print( '-r250','-depsc2',filename)




end



end % function
