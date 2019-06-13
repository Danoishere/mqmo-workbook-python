tEnd = 100000;
erloesProKunde = 15;
kostenProSitzplatzPro8h = 20;


kostenProSitzplatzProMin = kostenProSitzplatzPro8h/8/60;
N = 1:20;
lN = length(N);
nVK = zeros(lN, 1);

gewinn = zeros(lN, 1);

for k = 1:lN
    n = N(k);
    sim('Aufgabe2');
    nVK(k) = nVerpflegteKunden(end);
    gewinn(k) = nVK(k)*erloesProKunde - n*kostenProSitzplatzProMin*tEnd;
end

figure, plot(N, gewinn, 'o')

