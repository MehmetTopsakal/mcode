format compact;
format short g;
more on;

FontSize = 12;    %12
LineWidth = 1.5;  %1

set(0, 'DefaultTextFontSize', FontSize);
set(0, 'DefaultAxesFontSize', FontSize);
set(0, 'DefaultAxesFontName', 'Arial');
set(0, 'DefaultAxesLineWidth', LineWidth);
set(0, 'DefaultAxesTickLength', [0.014 0.014]);
set(0, 'DefaultAxesBox', 'on');
set(0, 'DefaultLineLineWidth', LineWidth);
set(0, 'DefaultLineMarkerSize', 5);
set(0, 'DefaultPatchLineWidth', LineWidth);
set(0, 'DefaultFigureColor', [1 1 1]);
% set(0, 'DefaultAxesColor', 'none');
set(0, 'DefaultFigurePaperPosition',[2.65 4.3 3.2 2.4]);
set(0, 'DefaultFigurePosition', [800 500 360 270])
% 360x260 pixels on screen keeps same aspect ratio as 3.2x2.4 printed
set(0, 'DefaultFigurePosition', [800 500 426 320])
set(0, 'DefaultFigureDockControls', 'off')

% try to remember last working directory
if ispref('StartupDirectory','LastWorkingDirectory')
    lwd = getpref('StartupDirectory','LastWorkingDirectory');
    try
        cd(lwd)
    catch
        disp('Sorry, but I could not go to your last working directory:')
        disp(lwd)
    end;
end;
