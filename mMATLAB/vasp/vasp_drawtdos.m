function vasp_drawtdos(x1,x2,y1,y2)

if nargin < 1,   disp('  ');    disp('USAGE : vasp_drawtdos(x1,x2,y1,y2) '); disp('  ');    ; end

if nargin < 2,   x2 =   6      ; end
if nargin < 1,   x1 =  -6      ; end

figure('Color','w'); 


%  [natom,ndos,nspin,fermi,tdos,pdoss]=vasp_readpdos;
[nspin,E,tdos,fermi]=vasp_readtdos;


% nonmagnetic
if  nspin==1
dos = tdos(:,1);

subplot(6,1,[1 2]); 
shift=0;
plot(E-fermi-shift,dos,'-','Color','k','LineWidth',1); grid on; hold on; 
ylabel('DOS','FontWeight','bold','FontSize',13,'FontName','Times','Color',[0.6 0.2 0]);
axis tight; %xlim([x1 x2]); %ylim([y1 y2]);



subplot(6,1,[3 6]); 
shift=0;
plot(E-fermi-shift,dos,'-','Color','k','LineWidth',1); grid on; hold on; 
ylabel('DOS','FontWeight','bold','FontSize',13,'FontName','Times','Color',[0.6 0.2 0]);
xlabel('Energy (eV)','FontWeight','bold','FontSize',13,'FontName','Times','Color',[0.6 0.2 0]);
axis tight; 
xlim([x1 x2]);
if nargin < 4,   y2 =   6      ; end
if nargin < 3,   y1 =   0      ; end
ylim([y1 y2]);
print -dpsc dos.ps
end


% magnetic
if  nspin==2
dos_up = tdos(:,1); dos_dw = tdos(:,2);

subplot(6,1,[1 2]); 
shift=0;
plot(E-fermi-shift,dos_up,'-','Color','k','LineWidth',1); grid on; hold on; 
plot(E-fermi-shift,-dos_dw,'-','Color','k','LineWidth',1); grid on; hold on;
ylabel('DOS','FontWeight','bold','FontSize',13,'FontName','Times','Color',[0.6 0.2 0]);
axis tight; %xlim([x1 x2]); %ylim([y1 y2]);



subplot(6,1,[3 6]); 
shift=0;
plot(E-fermi-shift,dos_up,'-','Color','k','LineWidth',1); grid on; hold on; 
plot(E-fermi-shift,-dos_dw,'-','Color','k','LineWidth',1); grid on; hold on;
ylabel('DOS','FontWeight','bold','FontSize',13,'FontName','Times','Color',[0.6 0.2 0]);
xlabel('Energy (eV)','FontWeight','bold','FontSize',13,'FontName','Times','Color',[0.6 0.2 0]);
axis tight; 
xlim([x1 x2]);
if nargin < 4,   y2 =   6      ; end
if nargin < 3,   y1 =  -6      ; end
ylim([y1 y2]);
print -dpsc dos.ps
end





end % function