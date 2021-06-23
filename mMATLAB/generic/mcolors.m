function [anumber,aradius,acolor,alabel] = ainfo(input)

%
% usage: 
%

input; 

switch input
     case {1,'1','H','h'}          ; values=[1,0.32,1.000,1.000,1.000];  alabel ='H';   
     case {2,'2','He','he'}        ; values=[2,0.93,0.851,1.000,1.000];  alabel ='He';  
     case {3,'3','Li','li'}        ; values=[3,1.23,0.800,0.502,1.000];  alabel ='Li';  
     case {4,'4','Be','be'}        ; values=[4,0.90,0.761,1.000,0.000];  alabel ='Be';  
     case {5,'5','B','b'}          ; values=[5,0.82,1.000,0.710,0.710];  alabel ='B';   
     case {6,'6','C','c'}          ; values=[6,1,0.6,0.2,0.0];        alabel ='C';   %   case {6,'6','C','c'}          ; values=[6,0.77,0.2,0.2,0.9];        alabel ='C';     
     case {7,'7','N','n'}          ; values=[7,0.75,0.188,0.314,0.973];  alabel ='N';   
     case {8,'8','O','o'}          ; values=[8,2,1.000,0.051,0.051];  alabel ='O'; %     case {8,'8','O','o'}          ; values=[8,0.73,1.000,0.051,0.051];  alabel ='O';   
     case {9,'9','F','f'}          ; values=[9,0.72,0.565,0.878,0.314];  alabel ='F';   
     case {10,'10','Ne','ne'}      ; values=[10,0.71,0.702,0.890,0.961]; alabel ='Ne';  
     case {11,'11','Na','na'}      ; values=[11,1.54,0.671,0.361,0.949]; alabel ='Na';  
     case {12,'12','Mg','mg'}      ; values=[12,1.36,0.541,1.000,0.000]; alabel ='Mg';  
     case {13,'13','Al','al'}      ; values=[13,1.18,0.749,0.651,0.651]; alabel ='Al';  
     case {14,'14','Si','si'}      ; values=[14,1.11,0.941,0.784,0.627]; alabel ='Si';  
     case {15,'15','P','p'}        ; values=[15,1.06,1.000,0.502,0.000]; alabel ='P';   
     case {16,'16','S','s'}        ; values=[16,1.02,1.000,1.000,0.188]; alabel ='S';   
     case {17,'17','Cl','cl'}      ; values=[17,0.99,0.122,0.941,0.122]; alabel ='Cl';  
     case {18,'18','Ar','ar'}      ; values=[18,0.98,0.502,0.820,0.890]; alabel ='Ar';  
     case {19,'19','K','k'}        ; values=[19,2.03,0.561,0.251,0.831]; alabel ='K';   
     case {20,'20','Ca','ca'}      ; values=[20,1.74,0.239,1.000,0.000]; alabel ='Ca';  
     case {21,'21','Sc','sc'}      ; values=[21,1.44,0.902,0.902,0.902]; alabel ='Sc';  
     case {22,'22','Ti','ti'}      ; values=[22,1.32,0.749,0.761,0.780]; alabel ='Ti';  
     case {23,'23','V','v'}        ; values=[23,1.22,0.651,0.651,0.671]; alabel ='V';   
     case {24,'24','Cr','cr'}      ; values=[24,1.18,0.541,0.600,0.780]; alabel ='Cr';  
     case {25,'25','Mn','mn'}      ; values=[25,1.17,0.612,0.478,0.780]; alabel ='Mn';  
     case {26,'26','Fe','fe'}      ; values=[26,1.17,0.878,0.400,0.200]; alabel ='Fe';  
     case {27,'27','Co','co'}      ; values=[27,1.16,0.941,0.565,0.627]; alabel ='Co';  
     case {28,'28','Ni','ni'}      ; values=[28,1.15,0.314,0.816,0.314]; alabel ='Ni';  
     case {29,'29','Cu','cu'}      ; values=[29,1.17,0.784,0.502,0.200]; alabel ='Cu';  
     case {30,'30','Zn','zn'}      ; values=[30,1.25,0.490,0.502,0.690]; alabel ='Zn';  
     case {31,'31','Ga','ga'}      ; values=[31,1.26,0.761,0.561,0.561]; alabel ='Ga';  
     case {32,'32','Ge','ge'}      ; values=[32,1.22,0.400,0.561,0.561]; alabel ='Ge';  
     case {33,'33','As','as'}      ; values=[33,1.20,0.741,0.502,0.890]; alabel ='As';  
     case {34,'34','Se','se'}      ; values=[34,1.16,1.000,0.631,0.000]; alabel ='Se';  
     case {35,'35','Br','br'}      ; values=[35,1.14,0.651,0.161,0.161]; alabel ='Br';  
     case {36,'36','Kr','kr'}      ; values=[36,1.89,0.361,0.722,0.820]; alabel ='Kr';  
     case {37,'37','Rb','rb'}      ; values=[37,2.16,0.439,0.180,0.690]; alabel ='Rb';  
     case {38,'38','Sr','sr'}      ; values=[38,1.91,0.000,1.000,0.000]; alabel ='Sr';  
     case {39,'39','Y','y'}        ; values=[39,1.62,0.580,1.000,1.000]; alabel ='Y';   
     case {40,'40','Zr','zr'}      ; values=[40,1.45,0.580,0.878,0.878]; alabel ='Zr';  
     case {41,'41','Nb','nb'}      ; values=[41,1.34,0.451,0.761,0.788]; alabel ='Nb';  
     case {42,'42','Mo','mo'}      ; values=[42,1.30,0.329,0.710,0.710]; alabel ='Mo';  
     case {43,'43','Tc','tc'}      ; values=[43,1.27,0.231,0.620,0.620]; alabel ='Tc';  
     case {44,'44','Ru','ru'}      ; values=[44,1.25,0.141,0.561,0.561]; alabel ='Ru';  
     case {45,'45','Rh','rh'}      ; values=[45,1.25,0.039,0.490,0.549]; alabel ='Rh';  
     case {46,'46','Pd','pd'}      ; values=[46,1.28,0.000,0.412,0.522]; alabel ='Pd';  
     case {47,'47','Ag','ag'}      ; values=[47,1.34,0.753,0.753,0.753]; alabel ='Ag';  
     case {48,'48','Cd','cd'}      ; values=[48,1.41,1.000,0.851,0.561]; alabel ='Cd';  
     case {49,'49','In','in'}      ; values=[49,1.44,0.651,0.459,0.451]; alabel ='In';  
     case {50,'50','Sn','sn'}      ; values=[50,1.41,0.400,0.502,0.502]; alabel ='Sn';  
     case {51,'51','Sb','sb'}      ; values=[51,1.40,0.620,0.388,0.710]; alabel ='Sb';  
     case {52,'52','Te','te'}      ; values=[52,1.36,0.831,0.478,0.000]; alabel ='Te';  
     case {53,'53','I','i'}        ; values=[53,1.33,0.580,0.000,0.580]; alabel ='I';   
     case {54,'54','Xe','xe'}      ; values=[54,1.31,0.259,0.620,0.690]; alabel ='Xe';  
     case {55,'55','Cs','cs'}      ; values=[55,2.35,0.341,0.090,0.561]; alabel ='Cs';  
     case {56,'56','Ba','ba'}      ; values=[56,1.98,0.000,0.788,0.000]; alabel ='Ba';  
     case {57,'57','La','la'}      ; values=[57,1.25,0.439,0.831,1.000]; alabel ='La';  
     case {58,'58','Ce','ce'}      ; values=[58,1.65,1.000,1.000,0.780]; alabel ='Ce';  
     case {59,'59','Pr','pr'}      ; values=[59,1.65,0.851,1.000,0.780]; alabel ='Pr';  
     case {60,'60','Nd','nd'}      ; values=[60,1.64,0.780,1.000,0.780]; alabel ='Nd';  
     case {61,'61','Pm','pm'}      ; values=[61,1.63,0.639,1.000,0.780]; alabel ='Pm';  
     case {62,'62','Sm','sm'}      ; values=[62,1.62,0.561,1.000,0.780]; alabel ='Sm';  
     case {63,'63','Eu','eu'}      ; values=[63,1.85,0.380,1.000,0.780]; alabel ='Eu';  
     case {64,'64','Gd','gd'}      ; values=[64,1.61,0.271,1.000,0.780]; alabel ='Gd';  
     case {65,'65','Tb','tb'}      ; values=[65,1.59,0.188,1.000,0.780]; alabel ='Tb';  
     case {66,'66','Dy','dy'}      ; values=[66,1.59,0.122,1.000,0.780]; alabel ='Dy';  
     case {67,'67','Ho','ho'}      ; values=[67,1.58,0.000,1.000,0.612]; alabel ='Ho';  
     case {68,'68','Er','er'}      ; values=[68,1.57,0.000,0.902,0.459]; alabel ='Er';  
     case {69,'69','Tm','tm'}      ; values=[69,1.56,0.000,0.831,0.322]; alabel ='Tm';  
     case {70,'70','Yb','yb'}      ; values=[70,1.70,0.000,0.749,0.220]; alabel ='Yb';  
     case {71,'71','Lu','lu'}      ; values=[71,1.56,0.000,0.671,0.141]; alabel ='Lu';  
     case {72,'72','Hf','hf'}      ; values=[72,1.44,0.302,0.761,1.000]; alabel ='Hf';  
     case {73,'73','Ta','ta'}      ; values=[73,1.34,0.302,0.651,1.000]; alabel ='Ta';  
     case {74,'74','W','w'}        ; values=[74,1.30,0.129,0.580,0.839]; alabel ='W' ;   
     case {75,'75','Re','re'}      ; values=[75,1.28,0.149,0.490,0.671]; alabel ='Re';  
     case {76,'76','Os','os'}      ; values=[76,1.26,0.149,0.400,0.588]; alabel ='Os';  
     case {77,'77','Ir','ir'}      ; values=[77,1.27,0.090,0.329,0.529]; alabel ='Ir';  
     case {78,'78','Pt','pt'}      ; values=[78,1.30,0.816,0.816,0.878]; alabel ='Pt';  
     case {79,'79','Au','au'}      ; values=[79,1.34,1.000,0.820,0.137]; alabel ='Au';  
     case {80,'80','Hg','hg'}      ; values=[80,1.49,0.722,0.722,0.816]; alabel ='Hg';  
     case {81,'81','Tl','tl'}      ; values=[81,1.48,0.651,0.329,0.302]; alabel ='Tl';  
     case {82,'82','Pb','pb'}      ; values=[82,1.47,0.341,0.349,0.380]; alabel ='Pb';  
     case {83,'83','Bi','bi'}      ; values=[83,1.46,0.620,0.310,0.710]; alabel ='Bi';  
     case {84,'84','Po','po'}      ; values=[84,1.53,0.671,0.361,0.000]; alabel ='Po';  
     case {85,'85','At','at'}      ; values=[85,1.47,0.459,0.310,0.271]; alabel ='At';  
     otherwise                     ; values=[100,2,0.5,0.5,0.5];         alabel ='H'; ;  
end

anumber = values(1) ;
aradius = values(2) ;

acolor  = [ values(3) values(4) values(5) ];

end