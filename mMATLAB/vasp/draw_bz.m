function  draw_bz


figure


%  [s,direct_lattice] = unix('awk ''/direct lattice vectors/, /  length of vectors/'' OUTCAR | awk "NR==2,NR==4" | awk ''{print $1"  "$2"  "$3}''');
%  direct_lattice = sscanf(direct_lattice,'%g', [3 3] ); direct_lattice = direct_lattice' ;

[s,reciprocal_lattice] = unix('awk ''/reciprocal lattice vectors/, /  length of vectors/'' OUTCAR | awk "NR==2,NR==4" | awk ''{print $4"  "$5"  "$6}''');
reciprocal_lattice = sscanf(reciprocal_lattice,'%g', [3 3] ); reciprocal_lattice = reciprocal_lattice' ;

reciprocal_lattice

[s,nkpoints] = unix('grep  NKPTS OUTCAR | awk ''{print $4}''');
nkpoints = sscanf(nkpoints,'%d') ;

[s,kpoints] = unix('awk ''/k-points in units of 2pi/, /k-points in reciprocal/'' OUTCAR | awk "NF==4"');
kpoints = sscanf(kpoints,'%f', [4 nkpoints] ); kpoints = kpoints' ;



subplot(1,6,[1 2])
line([0 reciprocal_lattice(1,1)], [0 reciprocal_lattice(1,2)], [0 reciprocal_lattice(1,3)],'LineStyle','-','LineWidth',2,'Color','r'); hold on;
line([0 reciprocal_lattice(2,1)], [0 reciprocal_lattice(2,2)], [0 reciprocal_lattice(2,3)],'LineStyle','-','LineWidth',2,'Color','g'); hold on;
line([0 reciprocal_lattice(3,1)], [0 reciprocal_lattice(3,2)], [0 reciprocal_lattice(3,3)],'LineStyle','-','LineWidth',2,'Color','b'); hold on;

for a=1:size(kpoints,1)
    plot3(kpoints(a,1),kpoints(a,2),kpoints(a,3),...
	'Marker','o','MarkerFaceColor','k',...
        'MarkerSize',(kpoints(a,4)+0.4)*10,...
        'LineStyle','none'); hold on;
end
axis equal ; axis off; grid on ; box on; view(0, 90);


subplot(1,6,[3 4])
line([0 reciprocal_lattice(1,1)], [0 reciprocal_lattice(1,2)], [0 reciprocal_lattice(1,3)],'LineStyle','-','LineWidth',2,'Color','r'); hold on;
line([0 reciprocal_lattice(2,1)], [0 reciprocal_lattice(2,2)], [0 reciprocal_lattice(2,3)],'LineStyle','-','LineWidth',2,'Color','g'); hold on;
line([0 reciprocal_lattice(3,1)], [0 reciprocal_lattice(3,2)], [0 reciprocal_lattice(3,3)],'LineStyle','-','LineWidth',2,'Color','b'); hold on;

%  line([0 direct_lattice(1,1)], [0 direct_lattice(1,2)], [0 direct_lattice(1,3)],'LineStyle','-','LineWidth',2,'Color','r'); hold on;
%  line([0 direct_lattice(2,1)], [0 direct_lattice(2,2)], [0 direct_lattice(2,3)],'LineStyle','-','LineWidth',2,'Color','g'); hold on;
%  line([0 direct_lattice(3,1)], [0 direct_lattice(3,2)], [0 direct_lattice(3,3)],'LineStyle','-','LineWidth',2,'Color','b'); hold on;

for a=1:size(kpoints,1)
    plot3(kpoints(a,1),kpoints(a,2),kpoints(a,3),...
	'Marker','o','MarkerFaceColor','k',...
        'MarkerSize',(kpoints(a,4)+0.4)*10,...
        'LineStyle','none'); hold on;
end
axis equal ; axis off; grid on ; box on; view(90,0);


subplot(1,6,[5 6])
line([0 reciprocal_lattice(1,1)], [0 reciprocal_lattice(1,2)], [0 reciprocal_lattice(1,3)],'LineStyle','-','LineWidth',2,'Color','r'); hold on;
line([0 reciprocal_lattice(2,1)], [0 reciprocal_lattice(2,2)], [0 reciprocal_lattice(2,3)],'LineStyle','-','LineWidth',2,'Color','g'); hold on;
line([0 reciprocal_lattice(3,1)], [0 reciprocal_lattice(3,2)], [0 reciprocal_lattice(3,3)],'LineStyle','-','LineWidth',2,'Color','b'); hold on;

%  line([0 direct_lattice(1,1)], [0 direct_lattice(1,2)], [0 direct_lattice(1,3)],'LineStyle','-','LineWidth',2,'Color','r'); hold on;
%  line([0 direct_lattice(2,1)], [0 direct_lattice(2,2)], [0 direct_lattice(2,3)],'LineStyle','-','LineWidth',2,'Color','g'); hold on;
%  line([0 direct_lattice(3,1)], [0 direct_lattice(3,2)], [0 direct_lattice(3,3)],'LineStyle','-','LineWidth',2,'Color','b'); hold on;

for a=1:size(kpoints,1)
    plot3(kpoints(a,1),kpoints(a,2),kpoints(a,3),...
	'Marker','o','MarkerFaceColor','k',...
        'MarkerSize',(kpoints(a,4)+0.4)*10,...
        'LineStyle','none'); hold on;
end
axis equal ; axis off; grid on ; box on; view(45,45);



filename = ['BZ.eps'];
print( '-r250','-depsc',filename)



end