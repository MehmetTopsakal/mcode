function [xyzlist]=read_xyz(file)

copyfile(file,'read_xyz_tmp_file')

[s,natoms] = unix('awk "NR==1" read_xyz_tmp_file');  
natoms = sscanf(natoms,'%d',1); 

[s,labels] = unix('awk "NR>=3" read_xyz_tmp_file | awk ''{ print $1}'' ');  
labels = sscanf(labels,'%s'); labels = labels' ;

[s,positions] = unix('awk "NR>=3" read_xyz_tmp_file | awk ''{ print $2" "$3"  "$4}'' ');  
positions = sscanf(positions,'%f', [3 natoms] ); positions = positions' ;

unix(' rm -f read_xyz_tmp_file ') ;

for a=1:natoms

switch lower(labels(a))
     case 'h'                    
       anumbers(a)=1;            
     case 'he'                  
       anumbers(a)=2;            
     case 'li'                   
       anumbers(a)=3;           
     case 'be'                   
       anumbers(a)=4;          
     case 'b'                    
       anumbers(a)=5;           
     case 'c'                    
       anumbers(a)=6;            
     case 'n'                    
       anumbers(a)=7;          
     case 'o'                    
       anumbers(a)=8;           
     case 'f'                   
       anumbers(a)=9;           
     case 'ne'                   
       anumbers(a)=10;          
     case 'na'                  
       anumbers(a)=11;           
     case 'mg'                   
       anumbers(a)=12;           
     case 'al'                   
       anumbers(a)=13;           
     case 'si'                   
       anumbers(a)=14;           
     case 'p'                    
       anumbers(a)=15;           
     case 's'                    
       anumbers(a)=16;           
     case 'cl'                   
       anumbers(a)=17;           
     case 'ar'                   
       anumbers(a)=18;           
     case 'k'                   
       anumbers(a)=19;            
     case 'ca'                    
       anumbers(a)=20;            
     case 'sc'                    
       anumbers(a)=21;            
     case 'ti'                    
       anumbers(a)=22;            
     case 'v'                     
       anumbers(a)=23;            
     case 'cr'                    
       anumbers(a)=24;            
     case 'mn'                    
       anumbers(a)=25;            
     case 'fe'                  
       anumbers(a)=26;            
     case 'co'                    
       anumbers(a)=27;            
     case 'ni'                    
       anumbers(a)=28;            
     case 'cu'                    
       anumbers(a)=29;            
     case 'zn'                    
       anumbers(a)=30;            
     case 'ga'                    
       anumbers(a)=31;            
     case 'ge'                    
       anumbers(a)=32;            
     case 'as'                  
       anumbers(a)=33;           
     case 'se'                  
       anumbers(a)=34;          
     case 'br'                  
       anumbers(a)=35; 
     case 'kr'
       anumbers(a)=36;
end

anumbers = anumbers' ;

xyzlist = { labels, positions, anumbers } ;

end
end
