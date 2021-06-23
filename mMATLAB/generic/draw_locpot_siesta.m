function draw_locpot(p_up,p_down)
%
% usage 
%

if nargin < 2,   p_down =  0.85     ; end
if nargin < 1,   p_up   =  0.15     ; end


figure ; subplot(2,1,1) ;


[lattice,positions]=read_poscar('POSCAR'); 
[s,fermi] = unix('head -n 1 *.EIG | awk ''{print $1}'' '); fermi = sscanf(fermi,'%f') ;
profile=load('graphene.PAV'); profile(:,1)=profile(:,1)/1.889725; profile(:,2)=profile(:,2)-fermi;

% vacuum energy
vacuum1=round(size(profile,1)*p_up); vacuum2=round(size(profile,1)*p_down); 
workfunction1=profile(vacuum1,2) 
workfunction2=profile(vacuum2,2) 

plot(profile(:,1),profile(:,2),'LineWidth',2 ); hold all ; 
plot([0,max(profile(:,1))],[0,0],'LineWidth',2,'LineStyle','-.','Color',[0 0.5 0]); grid on; hold all; % Fermi line
plot(positions(:,3),zeros(size(positions(:,3)))+min(profile(:,2))-1,'MarkerFaceColor',[1 0 0],'MarkerSize',7,'Marker','o','LineStyle','none'); hold all;


axis([ min(profile(:,1)-0) max(profile(:,1)+0) min(profile(:,2)-1) max(profile(:,2)+5)])

%  xlabel(['Height (Ang.) '],'FontWeight','bold','FontSize',14,'FontName','Times','Color',[0.6 0.2 0]);
%  ylabel(['Energy (eV)'],'FontWeight','bold','FontSize',18,'FontName','Times','Color',[0.6 0.2 0]);

xlabel(['\Phi_1 = ' num2str(workfunction1, '%.3f') ' , \Phi_2 = ' num2str(workfunction2, '%.3f') ' , \Phi_{1-2} = ' num2str(workfunction1-workfunction2, '%.3f') ' (eV)'],...
'FontWeight','bold','FontSize',14,'FontName','Times','Color',[0.6 0.2 0]);
ylabel(['Energy (eV)'],'FontWeight','bold','FontSize',18,'FontName','Times','Color',[0.6 0.2 0]);




print -dpdf LOCPOT.eps

end % function

