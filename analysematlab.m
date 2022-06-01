clear variables;
close all;
clc;

% Lecture du fichier
[y1,Fs1] = audioread('./music/music1.wav');  
[y2,Fs2] = audioread('./music/music2.wav');
[y3,Fs3] = audioread('./music/music3.wav');

% Stéréo --> Mono
y1 = y1(:);   
y2 = y2(:);
y3 = y3(:);

% Spectrogramme
s = spectrogram(y1);
spectrogram(y1,'yaxis')

%%
sound(y,Fs); 
test = input ('Press 1 to stop the music: ');

while test~=1 
fprintf ('You didn''t enter 1 ');
fprintf ('\n');
end
    clear sound;