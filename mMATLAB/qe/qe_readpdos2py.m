function qe_readpdos2py
%   

% atom uzerinden topluyor , s pxpypz d1d2d3d4d5 f1f2f3f4f5f6f7 diye

[s,line1] = unix('awk "NR==1" pdos.dos  ');
line1 = sscanf(line1,'%d');
natom=line1(1); ndos=line1(2); nspin=line1(3)+1; nstate=line1(4);

%  fermis=[0 0 0 0];
fermi = 0;


%  if exist('scf.out') == 2 
%  disp('getting Fermi energy from scf.out ')
%  fermi=qe_getfermi('scf.out');
%  end
%  
%  if exist('nscf.out') == 2 
%  disp('getting Fermi energy from nscf.out ')
%  fermi=qe_getfermi('nscf.out');
%  end
%  
%  if exist('nscf_dos.out') == 2 
%  disp('getting Fermi energy from nscf_dos.out ')
%  fermi=qe_getfermi('nscf_dos.out');
%  end
%  
%  if exist('nscf_bands.out') == 2 
%  disp('getting Fermi energy from nscf_bands.out ')
%  fermi=qe_getfermi('nscf_bands.out');
%  end


%  disp('Fermi energies from scf.out, nscf.out, nscf_dos.out, nscf-bands are :');
%  fermis

if  nspin==1
    [o,st] = system(sprintf(' head -n %d pdos.dos | awk "NR>1"',nstate+1));
    st = sscanf(st,'%d'); st=reshape(st,2,nstate); st=st';
    
    b=nstate+2;
    [o,tdosp] = system(sprintf(' awk "NR==%d,NR==%d" pdos.dos ',b,(b+ndos-1))); b=b+ndos;
    tdosp = sscanf(tdosp,'%g'); tdosp=reshape(tdosp,3,ndos); tdosp=tdosp'; Ep = tdosp(:,1); tdosp=[ tdosp(:,2) zeros(ndos,1) ]; 

Et=[]; tdost=[];  
%  disp(' I have found pwscf.dos ! Reading it as E2, tdos2 ') 
if exist('pwscf.dos') == 2 
[s,tdost] = unix('awk "NR>1" pwscf.dos | awk ''{ print $1" "$2" "$3}'' ');  
tdost = sscanf(tdost,'%f'); 
tdost = reshape(tdost,3,size(tdost,1)/3);
tdost = tdost'; Et=tdost(:,1); tdost = [ tdost(:,2) zeros(size(Et,1),1) ] ;
end
    
for z=1:max(st(:,1))
pd{z}=zeros(ndos,32);
end
    
    for s=1:nstate
        
        if st(s,2)==0     %s
            ncol=3;
               [o,r] = system(sprintf(' awk "NR==%d,NR==%d" pdos.dos ',b,(b+ndos-1))); b=b+ndos;
               r = sscanf(r,'%g'); r=reshape(r,ncol,ndos); r=r'; 
               pd{st(s,1)}(:,1)=r(:,2)+pd{st(s,1)}(:,1);
        elseif st(s,2)==1 %p
            ncol=5;
               [o,r] = system(sprintf(' awk "NR==%d,NR==%d" pdos.dos ',b,(b+ndos-1))); b=b+ndos;
               r = sscanf(r,'%g'); r=reshape(r,ncol,ndos); r=r'; 
               pd{st(s,1)}(:,2)=r(:,3)+pd{st(s,1)}(:,2); pd{st(s,1)}(:,3)=r(:,4)+pd{st(s,1)}(:,3); pd{st(s,1)}(:,4)=r(:,5)+pd{st(s,1)}(:,4);
        elseif st(s,2)==2 %d
            ncol=7;
               [o,r] = system(sprintf(' awk "NR==%d,NR==%d" pdos.dos ',b,(b+ndos-1))); b=b+ndos;
               r = sscanf(r,'%g'); r=reshape(r,ncol,ndos); r=r'; 
               pd{st(s,1)}(:,5)=r(:,3)+pd{st(s,1)}(:,5); pd{st(s,1)}(:,6)=r(:,4)+pd{st(s,1)}(:,6); pd{st(s,1)}(:,7)=r(:,5)+pd{st(s,1)}(:,7); pd{st(s,1)}(:,8)=r(:,6)+pd{st(s,1)}(:,8); pd{st(s,1)}(:,9)=r(:,7)+pd{st(s,1)}(:,9);
        elseif st(s,2)==3 %f
            ncol=9;
               [o,r] = system(sprintf(' awk "NR==%d,NR==%d" pdos.dos ',b,(b+ndos-1))); b=b+ndos;
               r = sscanf(r,'%g'); r=reshape(r,ncol,ndos); r=r'; 
               pd{st(s,1)}(:,10)=r(:,3)+pd{st(s,1)}(:,10); pd{st(s,1)}(:,11)=r(:,4)+pd{st(s,1)}(:,11); pd{st(s,1)}(:,12)=r(:,5)+pd{st(s,1)}(:,12); pd{st(s,1)}(:,13)=r(:,6)+pd{st(s,1)}(:,13); pd{st(s,1)}(:,14)=r(:,7)+pd{st(s,1)}(:,14); pd{st(s,1)}(:,15)=r(:,6)+pd{st(s,1)}(:,15); pd{st(s,1)}(:,16)=r(:,7)+pd{st(s,1)}(:,16);
        else
            disp('Something is wrong !!!');
                error(' ');
        end         
end
end 
 
 


 
 
if  nspin==2
    [o,st] = system(sprintf(' head -n %d pdos.dos | awk "NR>1"',nstate+1));
    st = sscanf(st,'%d'); st=reshape(st,2,nstate); st=st';
    
    b=nstate+2;
    [o,tdosp] = system(sprintf(' awk "NR==%d,NR==%d" pdos.dos ',b,(b+ndos-1))); b=b+ndos;
    tdosp = sscanf(tdosp,'%g'); tdosp=reshape(tdosp,5,ndos); tdosp=tdosp'; Ep = tdosp(:,1); tdosp=[ tdosp(:,2) tdosp(:,3)]; 

Et=[]; tdost=[];   
if exist('pwscf.dos') == 2
%  disp(' I have found pwscf.dos ! Reading it as E2, tdos2 ') 
[s,tdost] = unix('awk "NR>1" pwscf.dos | awk ''{ print $1" "$2" "$3}'' ');  
tdost = sscanf(tdost,'%f'); 
tdost = reshape(tdost,3,size(tdost,1)/3);
tdost = tdost'; Et=tdost(:,1); tdost = [ tdost(:,2) tdost(:,3) ] ;
end
    
for z=1:max(st(:,1))
pd{z}=zeros(ndos,32);
end
    
    for s=1:nstate
        
        if st(s,2)==0     %s
            ncol=5;
               [o,r] = system(sprintf(' awk "NR==%d,NR==%d" pdos.dos ',b,(b+ndos-1))); b=b+ndos;
               r = sscanf(r,'%g'); r=reshape(r,ncol,ndos); r=r'; 
               pd{st(s,1)}(:,1)=r(:,2)+pd{st(s,1)}(:,1);
               pd{st(s,1)}(:,1+16)=r(:,3)+pd{st(s,1)}(:,1+16);               
        elseif st(s,2)==1 %p
            ncol=9;
               [o,r] = system(sprintf(' awk "NR==%d,NR==%d" pdos.dos ',b,(b+ndos-1))); b=b+ndos;
               r = sscanf(r,'%g'); r=reshape(r,ncol,ndos); r=r'; 
               pd{st(s,1)}(:,2)=r(:,4)+pd{st(s,1)}(:,2); pd{st(s,1)}(:,3)=r(:,6)+pd{st(s,1)}(:,3); pd{st(s,1)}(:,4)=r(:,8)+pd{st(s,1)}(:,4);
               pd{st(s,1)}(:,2+16)=r(:,5)+pd{st(s,1)}(:,2+16); pd{st(s,1)}(:,3+16)=r(:,7)+pd{st(s,1)}(:,3+16); pd{st(s,1)}(:,4+16)=r(:,9)+pd{st(s,1)}(:,4+16);               
        elseif st(s,2)==2 %d
            ncol=13;
               [o,r] = system(sprintf(' awk "NR==%d,NR==%d" pdos.dos ',b,(b+ndos-1))); b=b+ndos;
               r = sscanf(r,'%g'); r=reshape(r,ncol,ndos); r=r'; 
               pd{st(s,1)}(:,5)=r(:,4)+pd{st(s,1)}(:,5); pd{st(s,1)}(:,6)=r(:,6)+pd{st(s,1)}(:,6); pd{st(s,1)}(:,7)=r(:,8)+pd{st(s,1)}(:,7); pd{st(s,1)}(:,8)=r(:,10)+pd{st(s,1)}(:,8); pd{st(s,1)}(:,9)=r(:,12)+pd{st(s,1)}(:,9);
               pd{st(s,1)}(:,5+16)=r(:,5)+pd{st(s,1)}(:,5+16); pd{st(s,1)}(:,6+16)=r(:,7)+pd{st(s,1)}(:,6+16); pd{st(s,1)}(:,7+16)=r(:,9)+pd{st(s,1)}(:,7+16); pd{st(s,1)}(:,8+16)=r(:,11)+pd{st(s,1)}(:,8+16); pd{st(s,1)}(:,9+16)=r(:,13)+pd{st(s,1)}(:,9+16);               
        elseif st(s,2)==3 %f
            ncol=17;
               [o,r] = system(sprintf(' awk "NR==%d,NR==%d" pdos.dos ',b,(b+ndos-1))); b=b+ndos;
               r = sscanf(r,'%g'); r=reshape(r,ncol,ndos); r=r'; 
               pd{st(s,1)}(:,10)=r(:,4)+pd{st(s,1)}(:,10); pd{st(s,1)}(:,11)=r(:,6)+pd{st(s,1)}(:,11); pd{st(s,1)}(:,12)=r(:,8)+pd{st(s,1)}(:,12); pd{st(s,1)}(:,13)=r(:,10)+pd{st(s,1)}(:,13); pd{st(s,1)}(:,14)=r(:,12)+pd{st(s,1)}(:,14); pd{st(s,1)}(:,15)=r(:,14)+pd{st(s,1)}(:,15); pd{st(s,1)}(:,16)=r(:,16)+pd{st(s,1)}(:,16);
               pd{st(s,1)}(:,10+16)=r(:,5)+pd{st(s,1)}(:,10+16); pd{st(s,1)}(:,11+16)=r(:,7)+pd{st(s,1)}(:,11+16); pd{st(s,1)}(:,12+16)=r(:,9)+pd{st(s,1)}(:,12+16); pd{st(s,1)}(:,13+16)=r(:,11)+pd{st(s,1)}(:,13+16); pd{st(s,1)}(:,14+16)=r(:,13)+pd{st(s,1)}(:,14+16); pd{st(s,1)}(:,15+16)=r(:,15)+pd{st(s,1)}(:,15+16); pd{st(s,1)}(:,16+16)=r(:,17)+pd{st(s,1)}(:,16+16);
        else
            disp('Something is wrong !!!');
                error(' ');
        end         
end
end  
 

%  
%  % to pdos.mat

size(pd{1})

st=1;
for k=1:size(pd,2)
pdos_all(st:st+size(Ep,1)-1,:)=pd{k};
st = st+size(Ep,1);
end

dim(1)=nspin;
dim(2)=natom;
dim(3)=ndos;
dim(4)=nstate;

tf = isempty(Et); 
if tf==1; Et = Ep; tdost = tdosp; end


size(pdos_all)


save -7 pdos.mat dim Ep tdosp fermi Et tdost pdos_all



end 



