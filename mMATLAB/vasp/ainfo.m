function [anumber,aradius,acolor,alabel] = ainfo(input)

%
% usage: 
%

input; 

switch input
     case {1,'1','H','h'}          ; values=[01,0.46,1.00000,0.80000,0.80000]; alabel ='H';   
     case {2,'2','He','he'}        ; values=[02,1.22,0.98907,0.91312,0.81091]; alabel ='He';  
     case {3,'3','Li','li'}        ; values=[03,1.57,0.52731,0.87953,0.45670]; alabel ='Li';  
     case {4,'4','Be','be'}        ; values=[04,1.12,0.37147,0.84590,0.48292]; alabel ='Be';  
     case {5,'5','B','b'}          ; values=[05,0.81,0.12490,0.63612,0.05948]; alabel ='B';   
     case {6,'6','C','c'}          ; values=[06,0.77,0.50430,0.28659,0.16236]; alabel ='C';     
     case {7,'7','N','n'}          ; values=[07,0.74,0.69139,0.72934,0.90280]; alabel ='N';   
     case {8,'8','O','o'}          ; values=[08,0.74,0.99997,0.01328,0.00000]; alabel ='O';   
     case {9,'9','F','f'}          ; values=[09,0.72,0.69139,0.72934,0.90280]; alabel ='F';   
     case {10,'10','Ne','ne'}      ; values=[10,1.60,0.99954,0.21788,0.71035]; alabel ='Ne';  
     case {11,'11','Na','na'}      ; values=[11,1.91,0.97955,0.86618,0.23787]; alabel ='Na';  
     case {12,'12','Mg','mg'}      ; values=[12,1.60,0.98773,0.48452,0.08470]; alabel ='Mg';  
     case {13,'13','Al','al'}      ; values=[13,1.43,0.50718,0.70056,0.84062]; alabel ='Al';  
     case {14,'14','Si','si'}      ; values=[14,1.18,0.10596,0.23226,0.98096]; alabel ='Si';  
     case {15,'15','P','p'}        ; values=[15,1.10,0.75557,0.61256,0.76425]; alabel ='P';   
     case {16,'16','S','s'}        ; values=[16,1.04,1.00000,0.98071,0.00000]; alabel ='S';   
     case {17,'17','Cl','cl'}      ; values=[17,0.99,0.19583,0.98828,0.01167]; alabel ='Cl';  
     case {18,'18','Ar','ar'}      ; values=[18,1.92,0.81349,0.99731,0.77075]; alabel ='Ar';  
     case {19,'19','K','k'}        ; values=[19,2.35,0.63255,0.13281,0.96858]; alabel ='K';   
     case {20,'20','Ca','ca'}      ; values=[20,1.97,0.35642,0.58863,0.74498]; alabel ='Ca';  
     case {21,'21','Sc','sc'}      ; values=[21,1.64,0.71209,0.38930,0.67279]; alabel ='Sc';  
     case {22,'22','Ti','ti'}      ; values=[22,1.47,0.24705,0.71764,0.34902]; alabel ='Ti';  
     case {23,'23','V','v'}        ; values=[23,1.35,0.90000,0.10000,0.00000]; alabel ='V';   
     case {24,'24','Cr','cr'}      ; values=[24,1.29,0.00000,0.00000,0.62000]; alabel ='Cr';  
     case {25,'25','Mn','mn'}      ; values=[25,1.37,0.66148,0.03412,0.62036]; alabel ='Mn';  
     case {26,'26','Fe','fe'}      ; values=[26,1.26,0.71051,0.44662,0.00136]; alabel ='Fe';  
     case {27,'27','Co','co'}      ; values=[27,1.25,0.00000,0.00000,0.68666]; alabel ='Co';  
     case {28,'28','Ni','ni'}      ; values=[28,1.25,0.72032,0.73631,0.74339]; alabel ='Ni';  
     case {29,'29','Cu','cu'}      ; values=[29,1.28,0.13390,0.28022,0.86606]; alabel ='Cu';  
     case {30,'30','Zn','zn'}      ; values=[30,1.37,0.56123,0.56445,0.50799]; alabel ='Zn';  
     case {31,'31','Ga','ga'}      ; values=[31,1.53,0.62292,0.89293,0.45486]; alabel ='Ga';  
     case {32,'32','Ge','ge'}      ; values=[32,1.22,0.49557,0.43499,0.65193]; alabel ='Ge';  
     case {33,'33','As','as'}      ; values=[33,1.21,0.45814,0.81694,0.34249]; alabel ='As';  
     case {34,'34','Se','se'}      ; values=[34,1.04,0.60420,0.93874,0.06122]; alabel ='Se';  
     case {35,'35','Br','br'}      ; values=[35,1.14,0.49645,0.19333,0.01076]; alabel ='Br';  
     case {36,'36','Kr','kr'}      ; values=[36,1.98,0.98102,0.75805,0.95413]; alabel ='Kr';  
     case {37,'37','Rb','rb'}      ; values=[37,2.50,1.00000,0.00000,0.60000]; alabel ='Rb';  
     case {38,'38','Sr','sr'}      ; values=[38,2.15,0.00000,1.00000,0.15259]; alabel ='Sr';  
     case {39,'39','Y','y'}        ; values=[39,1.82,0.40259,0.59739,0.55813]; alabel ='Y';   
     case {40,'40','Zr','zr'}      ; values=[40,1.60,0.00000,1.00000,0.00000]; alabel ='Zr';  
     case {41,'41','Nb','nb'}      ; values=[41,1.47,0.29992,0.70007,0.46459]; alabel ='Nb';  
     case {42,'42','Mo','mo'}      ; values=[42,1.40,0.70584,0.52602,0.68925]; alabel ='Mo';  
     case {43,'43','Tc','tc'}      ; values=[43,1.35,0.80574,0.68699,0.79478]; alabel ='Tc';  
     case {44,'44','Ru','ru'}      ; values=[44,1.34,0.81184,0.72113,0.68089]; alabel ='Ru';  
     case {45,'45','Rh','rh'}      ; values=[45,1.34,0.80748,0.82205,0.67068]; alabel ='Rh';  
     case {46,'46','Pd','pd'}      ; values=[46,1.37,0.75978,0.76818,0.72454]; alabel ='Pd';  
     case {47,'47','Ag','ag'}      ; values=[47,1.44,0.72032,0.73631,0.74339]; alabel ='Ag';  
     case {48,'48','Cd','cd'}      ; values=[48,1.52,0.95145,0.12102,0.86354]; alabel ='Cd';  
     case {49,'49','In','in'}      ; values=[49,1.67,0.84378,0.50401,0.73483]; alabel ='In';  
     case {50,'50','Sn','sn'}      ; values=[50,1.58,0.60764,0.56052,0.72926]; alabel ='Sn';  
     case {51,'51','Sb','sb'}      ; values=[51,1.41,0.84627,0.51498,0.31315]; alabel ='Sb';  
     case {52,'52','Te','te'}      ; values=[52,1.37,0.67958,0.63586,0.32038]; alabel ='Te';  
     case {53,'53','I','i'}        ; values=[53,1.33,0.55914,0.12200,0.54453]; alabel ='I';   
     case {54,'54','Xe','xe'}      ; values=[54,2.18,0.60662,0.63218,0.97305]; alabel ='Xe';  
     case {55,'55','Cs','cs'}      ; values=[55,2.72,0.05872,0.99922,0.72578]; alabel ='Cs';  
     case {56,'56','Ba','ba'}      ; values=[56,2.24,0.11835,0.93959,0.17565]; alabel ='Ba';  
     case {57,'57','La','la'}      ; values=[57,1.88,0.35340,0.77057,0.28737]; alabel ='La';  
     case {58,'58','Ce','ce'}      ; values=[58,1.82,0.82055,0.99071,0.02374]; alabel ='Ce';  
     case {59,'59','Pr','pr'}      ; values=[59,1.82,0.99130,0.88559,0.02315]; alabel ='Pr';  
     case {60,'60','Nd','nd'}      ; values=[60,1.82,0.98701,0.55560,0.02744]; alabel ='Nd';  
     case {61,'61','Pm','pm'}      ; values=[61,1.81,0.00000,0.00000,0.96000]; alabel ='Pm';  
     case {62,'62','Sm','sm'}      ; values=[62,1.81,0.99042,0.02403,0.49195]; alabel ='Sm';  
     case {63,'63','Eu','eu'}      ; values=[63,2.06,0.98367,0.03078,0.83615]; alabel ='Eu';  
     case {64,'64','Gd','gd'}      ; values=[64,1.79,0.75325,0.01445,1.00000]; alabel ='Gd';  
     case {65,'65','Tb','tb'}      ; values=[65,1.77,0.44315,0.01663,0.99782]; alabel ='Tb';  
     case {66,'66','Dy','dy'}      ; values=[66,1.77,0.19390,0.02374,0.99071]; alabel ='Dy';  
     case {67,'67','Ho','ho'}      ; values=[67,1.76,0.02837,0.25876,0.98608]; alabel ='Ho';  
     case {68,'68','Er','er'}      ; values=[68,1.75,0.28688,0.45071,0.23043]; alabel ='Er';  
     case {69,'69','Tm','tm'}      ; values=[69,1.00,0.00000,0.00000,0.88000]; alabel ='Tm';  
     case {70,'70','Yb','yb'}      ; values=[70,1.94,0.15323,0.99165,0.95836]; alabel ='Yb';  
     case {71,'71','Lu','lu'}      ; values=[71,1.72,0.15097,0.99391,0.71032]; alabel ='Lu';  
     case {72,'72','Hf','hf'}      ; values=[72,1.59,0.70704,0.70552,0.35090]; alabel ='Hf';  
     case {73,'73','Ta','ta'}      ; values=[73,1.47,0.71952,0.60694,0.33841]; alabel ='Ta';  
     case {74,'74','W','w'}        ; values=[74,1.41,0.55616,0.54257,0.50178]; alabel ='W' ;   
     case {75,'75','Re','re'}      ; values=[75,1.37,0.70294,0.69401,0.55789]; alabel ='Re';  
     case {76,'76','Os','os'}      ; values=[76,1.35,0.78703,0.69512,0.47379]; alabel ='Os';  
     case {77,'77','Ir','ir'}      ; values=[77,1.36,0.78975,0.81033,0.45049]; alabel ='Ir';  
     case {78,'78','Pt','pt'}      ; values=[78,1.39,0.79997,0.77511,0.75068]; alabel ='Pt';  
     case {79,'79','Au','au'}      ; values=[79,1.44,0.99628,0.70149,0.22106]; alabel ='Au';  
     case {80,'80','Hg','hg'}      ; values=[80,1.55,0.82940,0.72125,0.79823]; alabel ='Hg';  
     case {81,'81','Tl','tl'}      ; values=[81,1.71,0.58798,0.53854,0.42649]; alabel ='Tl';  
     case {82,'82','Pb','pb'}      ; values=[82,1.75,0.32386,0.32592,0.35729]; alabel ='Pb';  
     case {83,'83','Bi','bi'}      ; values=[83,1.82,0.82428,0.18732,0.97211]; alabel ='Bi';  
     case {84,'84','Po','po'}      ; values=[84,1.77,0.00000,0.00000,1.00000]; alabel ='Po';  
     case {85,'85','At','at'}      ; values=[85,0.62,0.00000,0.00000,1.00000]; alabel ='At';  
     otherwise                     ; values=[100,2,0.5,0.5,0.5];         alabel ='H'; ;  
end

anumber = values(1) ;
aradius = values(2) ;

acolor  = [ values(3) values(4) values(5) ];

end

%  
%  function [anumber,aradius,acolor,alabel] = ainfo(input)
%  
%  %
%  % usage: 
%  %
%  
%  input; 
%  
%  switch input
%       case {1,'1','H','h'}          ; values=[01,0.32,1.000,1.000,1.000]; alabel ='H';   
%       case {2,'2','He','he'}        ; values=[02,0.93,0.851,1.000,1.000]; alabel ='He';  
%       case {3,'3','Li','li'}        ; values=[03,1.23,0.800,0.502,1.000]; alabel ='Li';  
%       case {4,'4','Be','be'}        ; values=[04,0.90,0.761,1.000,0.000]; alabel ='Be';  
%       case {5,'5','B','b'}          ; values=[05,0.82,1.000,0.710,0.710]; alabel ='B';   
%       case {6,'6','C','c'}          ; values=[06,0.77,0.200,0.200,0.900]; alabel ='C';     
%       case {7,'7','N','n'}          ; values=[07,0.75,0.188,0.314,0.973]; alabel ='N';   
%       case {8,'8','O','o'}          ; values=[08,0.73,1.000,0.051,0.051]; alabel ='O';   
%       case {9,'9','F','f'}          ; values=[09,0.72,0.565,0.878,0.314]; alabel ='F';   
%       case {10,'10','Ne','ne'}      ; values=[10,0.71,0.702,0.890,0.961]; alabel ='Ne';  
%       case {11,'11','Na','na'}      ; values=[11,1.54,0.671,0.361,0.949]; alabel ='Na';  
%       case {12,'12','Mg','mg'}      ; values=[12,1.36,0.541,1.000,0.000]; alabel ='Mg';  
%       case {13,'13','Al','al'}      ; values=[13,1.18,0.749,0.651,0.651]; alabel ='Al';  
%       case {14,'14','Si','si'}      ; values=[14,1.11,0.941,0.784,0.627]; alabel ='Si';  
%       case {15,'15','P','p'}        ; values=[15,1.06,1.000,0.502,0.000]; alabel ='P';   
%       case {16,'16','S','s'}        ; values=[16,1.02,1.000,1.000,0.188]; alabel ='S';   
%       case {17,'17','Cl','cl'}      ; values=[17,0.99,0.122,0.941,0.122]; alabel ='Cl';  
%       case {18,'18','Ar','ar'}      ; values=[18,0.98,0.502,0.820,0.890]; alabel ='Ar';  
%       case {19,'19','K','k'}        ; values=[19,2.03,0.561,0.251,0.831]; alabel ='K';   
%       case {20,'20','Ca','ca'}      ; values=[20,1.74,0.239,1.000,0.000]; alabel ='Ca';  
%       case {21,'21','Sc','sc'}      ; values=[21,1.44,0.902,0.902,0.902]; alabel ='Sc';  
%       case {22,'22','Ti','ti'}      ; values=[22,1.32,0.749,0.761,0.780]; alabel ='Ti';  
%       case {23,'23','V','v'}        ; values=[23,1.22,0.651,0.651,0.671]; alabel ='V';   
%       case {24,'24','Cr','cr'}      ; values=[24,1.18,0.541,0.600,0.780]; alabel ='Cr';  
%       case {25,'25','Mn','mn'}      ; values=[25,1.17,0.612,0.478,0.780]; alabel ='Mn';  
%       case {26,'26','Fe','fe'}      ; values=[26,1.17,0.878,0.400,0.200]; alabel ='Fe';  
%       case {27,'27','Co','co'}      ; values=[27,1.16,0.941,0.565,0.627]; alabel ='Co';  
%       case {28,'28','Ni','ni'}      ; values=[28,1.15,0.314,0.816,0.314]; alabel ='Ni';  
%       case {29,'29','Cu','cu'}      ; values=[29,1.17,0.784,0.502,0.200]; alabel ='Cu';  
%       case {30,'30','Zn','zn'}      ; values=[30,1.25,0.490,0.502,0.690]; alabel ='Zn';  
%       case {31,'31','Ga','ga'}      ; values=[31,1.26,0.761,0.561,0.561]; alabel ='Ga';  
%       case {32,'32','Ge','ge'}      ; values=[32,1.22,0.400,0.561,0.561]; alabel ='Ge';  
%       case {33,'33','As','as'}      ; values=[33,1.20,0.741,0.502,0.890]; alabel ='As';  
%       case {34,'34','Se','se'}      ; values=[34,1.16,1.000,0.631,0.000]; alabel ='Se';  
%       case {35,'35','Br','br'}      ; values=[35,1.14,0.651,0.161,0.161]; alabel ='Br';  
%       case {36,'36','Kr','kr'}      ; values=[36,1.89,0.361,0.722,0.820]; alabel ='Kr';  
%       case {37,'37','Rb','rb'}      ; values=[37,2.16,0.439,0.180,0.690]; alabel ='Rb';  
%       case {38,'38','Sr','sr'}      ; values=[38,1.91,0.000,1.000,0.000]; alabel ='Sr';  
%       case {39,'39','Y','y'}        ; values=[39,1.62,0.580,1.000,1.000]; alabel ='Y';   
%       case {40,'40','Zr','zr'}      ; values=[40,1.45,0.580,0.878,0.878]; alabel ='Zr';  
%       case {41,'41','Nb','nb'}      ; values=[41,1.34,0.451,0.761,0.788]; alabel ='Nb';  
%       case {42,'42','Mo','mo'}      ; values=[42,1.30,0.329,0.710,0.710]; alabel ='Mo';  
%       case {43,'43','Tc','tc'}      ; values=[43,1.27,0.231,0.620,0.620]; alabel ='Tc';  
%       case {44,'44','Ru','ru'}      ; values=[44,1.25,0.141,0.561,0.561]; alabel ='Ru';  
%       case {45,'45','Rh','rh'}      ; values=[45,1.25,0.039,0.490,0.549]; alabel ='Rh';  
%       case {46,'46','Pd','pd'}      ; values=[46,1.28,0.000,0.412,0.522]; alabel ='Pd';  
%       case {47,'47','Ag','ag'}      ; values=[47,1.34,0.753,0.753,0.753]; alabel ='Ag';  
%       case {48,'48','Cd','cd'}      ; values=[48,1.41,1.000,0.851,0.561]; alabel ='Cd';  
%       case {49,'49','In','in'}      ; values=[49,1.44,0.651,0.459,0.451]; alabel ='In';  
%       case {50,'50','Sn','sn'}      ; values=[50,1.41,0.400,0.502,0.502]; alabel ='Sn';  
%       case {51,'51','Sb','sb'}      ; values=[51,1.40,0.620,0.388,0.710]; alabel ='Sb';  
%       case {52,'52','Te','te'}      ; values=[52,1.36,0.831,0.478,0.000]; alabel ='Te';  
%       case {53,'53','I','i'}        ; values=[53,1.33,0.580,0.000,0.580]; alabel ='I';   
%       case {54,'54','Xe','xe'}      ; values=[54,1.31,0.259,0.620,0.690]; alabel ='Xe';  
%       case {55,'55','Cs','cs'}      ; values=[55,2.35,0.341,0.090,0.561]; alabel ='Cs';  
%       case {56,'56','Ba','ba'}      ; values=[56,1.98,0.000,0.788,0.000]; alabel ='Ba';  
%       case {57,'57','La','la'}      ; values=[57,1.25,0.439,0.831,1.000]; alabel ='La';  
%       case {58,'58','Ce','ce'}      ; values=[58,1.65,1.000,1.000,0.780]; alabel ='Ce';  
%       case {59,'59','Pr','pr'}      ; values=[59,1.65,0.851,1.000,0.780]; alabel ='Pr';  
%       case {60,'60','Nd','nd'}      ; values=[60,1.64,0.780,1.000,0.780]; alabel ='Nd';  
%       case {61,'61','Pm','pm'}      ; values=[61,1.63,0.639,1.000,0.780]; alabel ='Pm';  
%       case {62,'62','Sm','sm'}      ; values=[62,1.62,0.561,1.000,0.780]; alabel ='Sm';  
%       case {63,'63','Eu','eu'}      ; values=[63,1.85,0.380,1.000,0.780]; alabel ='Eu';  
%       case {64,'64','Gd','gd'}      ; values=[64,1.61,0.271,1.000,0.780]; alabel ='Gd';  
%       case {65,'65','Tb','tb'}      ; values=[65,1.59,0.188,1.000,0.780]; alabel ='Tb';  
%       case {66,'66','Dy','dy'}      ; values=[66,1.59,0.122,1.000,0.780]; alabel ='Dy';  
%       case {67,'67','Ho','ho'}      ; values=[67,1.58,0.000,1.000,0.612]; alabel ='Ho';  
%       case {68,'68','Er','er'}      ; values=[68,1.57,0.000,0.902,0.459]; alabel ='Er';  
%       case {69,'69','Tm','tm'}      ; values=[69,1.56,0.000,0.831,0.322]; alabel ='Tm';  
%       case {70,'70','Yb','yb'}      ; values=[70,1.70,0.000,0.749,0.220]; alabel ='Yb';  
%       case {71,'71','Lu','lu'}      ; values=[71,1.56,0.000,0.671,0.141]; alabel ='Lu';  
%       case {72,'72','Hf','hf'}      ; values=[72,1.44,0.302,0.761,1.000]; alabel ='Hf';  
%       case {73,'73','Ta','ta'}      ; values=[73,1.34,0.302,0.651,1.000]; alabel ='Ta';  
%       case {74,'74','W','w'}        ; values=[74,1.30,0.129,0.580,0.839]; alabel ='W' ;   
%       case {75,'75','Re','re'}      ; values=[75,1.28,0.149,0.490,0.671]; alabel ='Re';  
%       case {76,'76','Os','os'}      ; values=[76,1.26,0.149,0.400,0.588]; alabel ='Os';  
%       case {77,'77','Ir','ir'}      ; values=[77,1.27,0.090,0.329,0.529]; alabel ='Ir';  
%       case {78,'78','Pt','pt'}      ; values=[78,1.30,0.816,0.816,0.878]; alabel ='Pt';  
%       case {79,'79','Au','au'}      ; values=[79,1.34,1.000,0.820,0.137]; alabel ='Au';  
%       case {80,'80','Hg','hg'}      ; values=[80,1.49,0.722,0.722,0.816]; alabel ='Hg';  
%       case {81,'81','Tl','tl'}      ; values=[81,1.48,0.651,0.329,0.302]; alabel ='Tl';  
%       case {82,'82','Pb','pb'}      ; values=[82,1.47,0.341,0.349,0.380]; alabel ='Pb';  
%       case {83,'83','Bi','bi'}      ; values=[83,1.46,0.620,0.310,0.710]; alabel ='Bi';  
%       case {84,'84','Po','po'}      ; values=[84,1.53,0.671,0.361,0.000]; alabel ='Po';  
%       case {85,'85','At','at'}      ; values=[85,1.47,0.459,0.310,0.271]; alabel ='At';  
%       otherwise                     ; values=[100,2,0.5,0.5,0.5];         alabel ='H'; ;  
%  end
%  
%  anumber = values(1) ;
%  aradius = values(2) ;
%  
%  acolor  = [ values(3) values(4) values(5) ];
%  
%  end