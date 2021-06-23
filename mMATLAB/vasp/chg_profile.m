function chg_profile(direction,start,stop,ymax)
%
% usage chg_profile(direction,start,stop)
%

[lattice,atoms,positions,chg_matrix]=read_chg('CHGCAR');  
[grid_x,grid_y,grid_z] = size(chg_matrix); 

if nargin < 4, ymax      = 0.00001      ; end
if nargin < 3, stop      = 0.75      ; end
if nargin < 2, start     = 0.25      ; end
if nargin < 1, direction = 'z'       ; end

    if direction=='x' ; ngrid=grid_x ; length = lattice(1,1) ; summ = sum(sum(chg_matrix,2),3) ; pos = positions(:,1)*length ;
line_profile = reshape(summ(:,1,1),ngrid,1)/grid_x/grid_y/grid_z ; total_charge=sum(line_profile) ;
elseif direction=='y' ; ngrid=grid_y ; length = lattice(2,2) ; summ = sum(sum(chg_matrix,1),3) ; pos = positions(:,2)*length ; 
 line_profile = reshape(summ(1,:,1),ngrid,1)/grid_x/grid_y/grid_z ; total_charge=sum(line_profile) ;
elseif direction=='z' ; ngrid=grid_z ; length = lattice(3,3) ; summ = sum(sum(chg_matrix,1),2) ; pos = positions(:,3)*length ; 
 line_profile = reshape(summ(1,1,:),ngrid,1)/grid_x/grid_y/grid_z ; total_charge=sum(line_profile) ;
end


positions_dir = 0:length/(ngrid-1):length ;



figure
subplot(2,1,1) ; 
area(positions_dir,line_profile,'FaceColor',[1 0.6 0.78],'LineWidth',2) ; hold all ; 
plot(positions(:,3)*lattice(3,3),zeros(size(positions),1),'MarkerFaceColor',[1 0 0],...
'MarkerSize',10,'Marker','o','LineStyle','none'); 
xlim([0 length]) ;
ylim([min(line_profile) (max(line_profile)*1.10)]) ;
ylabel('\lambda (e/Angst.)' , 'FontWeight','bold','FontSize',15,'FontName','Times',...
      'Color',[0.6 0.2 0]); 

subplot(2,1,2) ; 
area(positions_dir,line_profile,'FaceColor',[1 0.6 0.78],'LineWidth',1) ; hold all ; 
plot(positions(:,3)*lattice(3,3),zeros(size(positions),1),'MarkerFaceColor',[1 0 0],...
'MarkerSize',10,'Marker','o','LineStyle','none'); 
xlim([0 length]) ;
ylim([min(line_profile) ymax]) ;
ylabel('\lambda (e/Angst.)' , 'FontWeight','bold','FontSize',15,'FontName','Times',...
      'Color',[0.6 0.2 0]); 

peak_1_range = [length*start-1,length*start+1] ; peak_2_range = [length*stop-1,length*stop+1] ; 
  
  peak_1_start = round(((peak_1_range(1))/length)*ngrid) ; 
  peak_1_stop  = round(((peak_1_range(2))/length)*ngrid) ; 
  min1 = min(line_profile(peak_1_start:peak_1_stop,1)) ; min1 = find(line_profile==min1); 
  peak_2_start = round(((peak_2_range(1))/length)*ngrid) ; 
  peak_2_stop  = round(((peak_2_range(2))/length)*ngrid) ; 
  min2 = min(line_profile(peak_2_start:peak_2_stop,1)) ; min2 = find(line_profile==min2); 
  
  hold on ; plot((min1/ngrid)*length,line_profile(min1),'Marker','*','Color',[1 0 0],'MarkerSize',10) ;
  hold on ; plot((min2/ngrid)*length,line_profile(min2),'Marker','*','Color',[1 0 0],'MarkerSize',10) ;
  
  peak_1_start =  1 ; peak_1_stop  = min1 ; 
  peak_1_integral = sum(line_profile(peak_1_start:peak_1_stop,1)) ;
  peak_2_start =  peak_1_stop+1 ; peak_2_stop  =  min2 ;
  peak_2_integral = sum(line_profile(peak_2_start:peak_2_stop,1)) ;
  peak_3_start =  peak_2_stop+1 ; peak_3_stop  =  ngrid  ;
  peak_3_integral = sum(line_profile(peak_3_start:peak_3_stop,1)) ;
  
  
  charge_sum = peak_1_integral + peak_2_integral + peak_3_integral ;
  peak13 = peak_1_integral + peak_3_integral ;
  
  % Create ylabel
  label_txt=['peak1=' num2str(peak_1_integral,'%.3f') ', peak2=' num2str(peak_2_integral,'%.3f')...
  ', peak3=' num2str(peak_3_integral,'%.3f') ', total=' num2str(charge_sum,'%.3f') ',  peak1+peak3=' num2str(peak13,'%.3f') '' ] ; xlabel(label_txt);
  


print -depsc chg_profile.eps



end

