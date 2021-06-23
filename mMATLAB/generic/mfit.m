 function [minimum,fit,res] = mfit(file,column_x,column_y,order,format,lower_boundary,upper_boundary)
 %
 % usage 
 %

 if nargin < 7, upper_boundary = 1.05 ; end 
 if nargin < 6, lower_boundary = 0.95 ; end 
 if nargin < 5, format =  'MATLAB'    ; end
 if nargin < 4,  order =  4           ; end
 if nargin < 3,  error('myApp:argChk', 'Wrong number of input arguments') ; end

%   if nargin < 7, upper_boundary = 1.05 ; end 
%   if nargin < 6, lower_boundary = 0.95 ; end 
%   if nargin < 5, format =  'MATLAB'    ; end
%   if nargin < 4, order  =  4           ; end
%   if nargin < 3,  error('myApp:argChk', 'Wrong number of input arguments') ; end


%==========================================================================
%      read data and make fitting.
%==========================================================================

system(sprintf(' cat %s | sed ''/#/d'' > mfit.tmp ',file)) ;
data = load('mfit.tmp'); delete mfit.tmp ;


data = [ data(:,column_x) data(:,column_y)] ;


% interpolate available data and find a minimum.
xmin = min(data(:,1)) ; xmax = max(data(:,1)) ;
xi=[xmin:(xmax-xmin)/200:xmax] ; yi=interp1(data(:,1),data(:,2),xi,'spline');
min_yi=min(yi); min_xi=xi(:,find(yi==min_yi)); 

% define effective range
e = 1 ; eff_min=(min_xi*lower_boundary) ; eff_max=(min_xi*upper_boundary);
x=[eff_min:(eff_max-eff_min)/1000:eff_max] ;
for n=1:size(data,1)
    if data(n,1) < eff_min ;  continue  ;  end
    if data(n,1) > eff_max ;  continue  ;  end
    eff_data(e,:)=data(n,:); e = e + 1 ;
end

[p,s] = polyfit(eff_data(:,1),eff_data(:,2),order);
y = polyval(p,x); [ymin_fit i] = min(y); xmin_fit = x(i);

fit=p ; minimum = [xmin_fit ymin_fit]; res = s.normr;



switch lower(format)
   case {'o','octave'}

%==========================================================================
%      plotting part - OCTAVE version
%==========================================================================

figure('Color',[1 1 1]) ; 

subplot(2,7,[1 3])

plot(data(:,1),data(:,2),'LineStyle','none','Marker','o','markerfacecolor','blue','markeredgecolor','auto','MarkerSize',10,'Color',[1 0 0]);

hold on ; 

yi = polyval(p,xi); plot(xi,yi,'-','LineWidth',2);
ex = (xmax - xmin)/20 ; ey = abs((max(data(:,2)) - min(data(:,2)))/20) ; 
xlim([ (xmin-ex)  (xmax+ex) ]); 
ylim([ (min(data(:,2)-ey))   (max(data(:,2)+ey)) ]);

x_axis_text = ['Data(:,' num2str(column_x) ')'];
xlabel(x_axis_text , 'FontWeight','bold','FontSize',15,'FontName','Times',...
    'Color',[0.6 0.2 0]); 




y_axis_text = ['Data(:,' num2str(column_y) ')'];
ylabel(y_axis_text , 'FontWeight','bold','FontSize',15,'FontName','Times',...
    'Color',[0.6 0.2 0]); 


subplot(2,7,[5 7])

plot(data(:,1),data(:,2),'LineStyle','none','Marker','o','markerfacecolor','blue','markeredgecolor','auto','MarkerSize',10,'Color',[1 0 0]);

hold on ; 

xi=[xmin:(xmax-xmin)/1000:xmax] ; yi = polyval(p,xi); plot(xi,yi,'-','LineWidth',2);
ex = abs((max(eff_data(:,1)) - min(eff_data(:,1)))/20) ; 
ey = abs((max(eff_data(:,2)) - min(eff_data(:,2)))/20) ; 
xlim([ (min(eff_data(:,1))-ex)  (max(eff_data(:,1))+ex) ]); 
ylim([ (min(eff_data(:,2))-ey)  (max(eff_data(:,2))+ey) ]);

x_axis_text = ['Data(:,' num2str(column_x) ')'];
xlabel(x_axis_text , 'FontWeight','bold','FontSize',15,'FontName','Times',...
    'Color',[0.6 0.2 0]); 


y_axis_text = ['Data(:,' num2str(column_y) ')'];
ylabel(y_axis_text , 'FontWeight','bold','FontSize',15,'FontName','Times',...
    'Color',[0.6 0.2 0]); 


min_data_y=min(data(:,2)); min_data_x=data(find(data(:,2)==min_data_y),1); 
line_1 = [ '|| DATA_{min} = (' num2str(sprintf(' %.3f' , min_data_x)) ','  num2str(sprintf(' %.3f' , min_data_y)) ')' ];
line_2 = [ '; FIT_{min} = (' num2str(sprintf(' %.3f' , xmin_fit)) ','  num2str(sprintf(' %.3f' , ymin_fit))   ];
line_3 = [ '; (FIT-DATA) = (' num2str(sprintf(' %.3f' , xmin_fit-min_data_x)) ','  num2str(sprintf(' %.3f' , ymin_fit-min_data_y)) ')' ' ; NormOfRes. = ' num2str(sprintf(' %.3f' , s.normr)) ' ||' ];


%  % draw textbox
%  annotation('textbox',[0 0.2 1 0.30],...
%      'String',[line_1 line_2 line_3],...
%      'LineStyle', 'none','FontName','Monospaced','FontWeight','bold','FontSize',8,'FitBoxToText','on', 'BackgroundColor',[1 0.6941 0.3922]);


filename = [ 'mfit_' num2str(order) 'o.eps']; print( '-r250','-depsc2',filename);

   case {'m','matlab'}

%==========================================================================
%      plotting part - MATLAB version
%==========================================================================

figure('Color',[1 1 1]) ; 

subplot(2,7,[1 3])

hl1 = line(data(:,1),data(:,2),'Marker','square','MarkerFaceColor',[1 0 0],...
    'MarkerEdgeColor',[0 0 1],...
    'MarkerSize',5,...
    'LineStyle',':',...
    'Color',[1 0 0]);

hold on ; 

yi = polyval(p,xi); plot(xi,yi,'-');
ex = (xmax - xmin)/20 ; ey = abs((max(data(:,2)) - min(data(:,2)))/20) ; 
xlim([ (xmin-ex)  (xmax+ex) ]); 
ylim([ (min(data(:,2)-ey))   (max(data(:,2)+ey)) ]);

x_axis_text = ['Data(:,' num2str(column_x) ')'];
xlabel(x_axis_text , 'FontWeight','bold','FontSize',15,'FontName','Times',...
    'Color',[0.6 0.2 0]); 

ax1 = gca;
set(ax1,'XColor','r','YColor','r')
ax2 = axes('Position',get(ax1,'Position'),...
           'XAxisLocation','top',...
           'YAxisLocation','left',...
           'Color','none',...
           'XColor','k','YColor','k');
       
hl2 = line(data(:,1)/xmin_fit,data(:,2),'LineStyle','none','Parent',ax2);
xlim([ (xmin-ex)/xmin_fit  (xmax+ex)/xmin_fit ]); 
ylim([ (min(data(:,2)-ey))   (max(data(:,2)+ey)) ]);


y_axis_text = ['Data(:,' num2str(column_y) ')'];
ylabel(y_axis_text , 'FontWeight','bold','FontSize',15,'FontName','Times',...
    'Color',[0.6 0.2 0]); 


subplot(2,7,[5 7])

hl1 = line(data(:,1),data(:,2),'Marker','square','MarkerFaceColor',[1 0 0],...
    'MarkerEdgeColor',[0 0 1],...
    'MarkerSize',5,...
    'LineStyle',':',...
    'Color',[1 0 0]);

hold on ; 

xi=[xmin:(xmax-xmin)/1000:xmax] ; yi = polyval(p,xi); plot(xi,yi,'-');
ex = abs((max(eff_data(:,1)) - min(eff_data(:,1)))/20) ; 
ey = abs((max(eff_data(:,2)) - min(eff_data(:,2)))/20) ; 
xlim([ (min(eff_data(:,1))-ex)  (max(eff_data(:,1))+ex) ]); 
ylim([ (min(eff_data(:,2))-ey)  (max(eff_data(:,2))+ey) ]);

x_axis_text = ['Data(:,' num2str(column_x) ')'];
xlabel(x_axis_text , 'FontWeight','bold','FontSize',15,'FontName','Times',...
    'Color',[0.6 0.2 0]); 


ax1 = gca;
set(ax1,'XColor','r','YColor','r')
ax2 = axes('Position',get(ax1,'Position'),...
           'XAxisLocation','top',...
           'YAxisLocation','left',...
           'Color','none',...
           'XColor','k','YColor','k');
       
hl2 = line(data(:,1)/xmin_fit,data(:,2),'LineStyle','none','Parent',ax2);
xlim([ (min(eff_data(:,1))-ex)/xmin_fit  (max(eff_data(:,1))+ex)/xmin_fit ]); 
ylim([ (min(eff_data(:,2))-ey)  (max(eff_data(:,2))+ey) ]);

y_axis_text = ['Data(:,' num2str(column_y) ')'];
ylabel(y_axis_text , 'FontWeight','bold','FontSize',15,'FontName','Times',...
    'Color',[0.6 0.2 0]); 


min_data_y=min(data(:,2)); min_data_x=data(find(data(:,2)==min_data_y),1); 
line_1 = [ '|| DATA_{min} = (' num2str(sprintf(' %.4f' , min_data_x)) ','  num2str(sprintf(' %.4f' , min_data_y)) ')' ];
line_2 = [ '; FIT_{min} = (' num2str(sprintf(' %.4f' , xmin_fit)) ','  num2str(sprintf(' %.4f' , ymin_fit)) ')'  ];
line_3 = [ '; (FIT-DATA) = (' num2str(sprintf(' %.4f' , xmin_fit-min_data_x)) ','  num2str(sprintf(' %.4f' , ymin_fit-min_data_y)) ')' ' ; NormOfRes. = ' num2str(sprintf(' %.3f' , s.normr)) ' ||' ];


% draw textbox
annotation('textbox',[0 0.2 1 0.30],...
    'String',[line_1 line_2 line_3],...
    'LineStyle', 'none','FontName','Monospaced','FontWeight','bold','FontSize',8,'FitBoxToText','on', 'BackgroundColor',[1 0.6941 0.3922]);


filename = [ 'mfit_' num2str(order) 'o.eps']; print( '-r250','-depsc2',filename);


% =========================================================================
   otherwise
       
      disp('Unknown output format: MATLAB or OCTAVE ???.')
end




end
