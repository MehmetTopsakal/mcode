function qe_drawpdos(state,x1,x2,y1,y2)

if nargin < 1,   disp('  ');    disp('USAGE : qe_drawpdos(state,x1,x2,y1,y2) '); disp('  ');    ; end

if nargin < 3,   x2 =   6      ; end
if nargin < 2,   x1 =  -6      ; end

figure('Color','w'); 

nscfout='nscf.out';
[fermi]=qe_getfermi(nscfout); 

! existanceofpdosdos=`ls | grep pdos.dos | wc -l` ; if [ "$existanceofpdosdos" -gt "0" ]; then echo "ATTENTION !!!, using available pdos.dos file";  else  qe_collectpdos ; fi

[natom,ndos,nspin,states,tdos,pdoss]=qe_readpdos; states



% nonmagnetic
if  nspin==0
disp('not implemented yet')
end

% magnetic
if  nspin==1
E = tdos(:,1) ; dos_up = tdos(:,2); dos_dw = tdos(:,3); 
pdos1=pdoss{state}; pdos_up1 = pdos1(:,2); pdos_dw1 = pdos1(:,3); 

subplot(6,1,[1 2]); 
shift=0;
plot(E-fermi(1)-shift,dos_up,'-','Color','k','LineWidth',1); grid on; hold on; 
plot(E-fermi(1)-shift,-dos_dw,'-','Color','k','LineWidth',1); grid on; hold on;
plot(E-fermi(1)-shift,pdos_up1,'-','Color','b','LineWidth',1); grid on; hold on; 
plot(E-fermi(1)-shift,-pdos_dw1,'-','Color','b','LineWidth',1); grid on; hold on;
ylabel('DOS','FontWeight','bold','FontSize',13,'FontName','Times','Color',[0.6 0.2 0]);
axis tight; %xlim([x1 x2]); %ylim([y1 y2]);



subplot(6,1,[3 6]); 
shift=0;
plot(E-fermi(1)-shift,dos_up,'-','Color','k','LineWidth',1); grid on; hold on; 
plot(E-fermi(1)-shift,-dos_dw,'-','Color','k','LineWidth',1); grid on; hold on;
plot(E-fermi(1)-shift,pdos_up1,'-','Color','b','LineWidth',1); grid on; hold on; 
plot(E-fermi(1)-shift,-pdos_dw1,'-','Color','b','LineWidth',1); grid on; hold on;
ylabel('DOS','FontWeight','bold','FontSize',13,'FontName','Times','Color',[0.6 0.2 0]);
xlabel('Energy (eV)','FontWeight','bold','FontSize',13,'FontName','Times','Color',[0.6 0.2 0]);
axis tight; 
xlim([x1 x2]);
if nargin < 4,   y2 =   6      ; end
if nargin < 3,   y1 =  -6      ; end
ylim([y1 y2]);
print -depsc pdos.eps
end





end % function