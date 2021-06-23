function mplot(file,colx,coly,x_label,y_label) 
%
% usage example > mplot('total-analiz.dat',5,1,'Energy','Lattice_x')
%
if nargin < 5,  y_label='  '; end
if nargin < 4,  x_label='  '; end
if nargin < 3,  coly=2;       end
if nargin < 2,  colx=1;       end


%x_label='  '; y_label='  '; colx=1; coly=2;

[s,alldata] = unix(sprintf('cat %s | awk ''{print $%d"  "$%d}'' ',file,colx,coly));
alldata     = sscanf(alldata,'%f'); 
alldata = reshape(alldata,2,size(alldata,1)/2); alldata = alldata';

X = alldata(:,1) ; Y = alldata(:,2) ; 

figure('Color','w'); subplot(2,1,1);
plot(X,Y,'--rs','LineWidth',2,'MarkerEdgeColor','k','MarkerFaceColor','b', 'MarkerSize',6); grid on;
title('  ','FontWeight','bold','FontSize',15,'FontName','Times','Color',[0.6 0.2 0]);
xlabel(x_label,'FontWeight','bold','FontSize',15,'FontName','Times','Color',[0.6 0.2 0]);
ylabel(y_label,'FontWeight','bold','FontSize',15,'FontName','Times','Color',[0.6 0.2 0]);
%legend_text = ['step = ' num2str(1)] ; legend(legend_text,1) ; legend('boxon'),
axis tight;


filename = ['mplot.eps']; print( '-r250','-depsc2',filename)



end
