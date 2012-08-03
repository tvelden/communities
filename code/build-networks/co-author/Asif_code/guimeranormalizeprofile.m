function guimeranormalizeprofile(dirname)

l= load(sprintf('../data/output/misc/guimeraprofile.%s.txt', dirname), '-ascii');

s= l(:, 1);
t= l(:, 2:end);

size(t)

m= zeros(length(s), 1);
ss= zeros(length(s), 1);
z= zeros(length(s), 1);

lbl= {};

k= 1;
for i=1:7
    for j=i:7
        m(k)= mean(t(k, :));
        if s(k) == m(k)
            ss(k)= 0;
            z(k)= 0;
        else
            ss(k)= std(t(k, :), 1);
            z(k)= (s(k) - m(k))/ss(k);
        end
        
        lbl= [lbl; sprintf('R%d-R%d', i, j)];
        
        k= k+1;
    end
end

ord= [1 2 8 3 9 14 4 10 15 19 5 11 16 20 6 12 17 21 7 13 18 22 23 24 26 25 27 28];

fid= fopen(sprintf('../data/output/guimeraprofile/%s.txt', dirname), 'wt');
for k=1:28
    fprintf(fid, '%s %d %.4f %.2f %.2f\n', char(lbl(ord(k))), s(ord(k)), z(ord(k)), m(ord(k)), ss(ord(k)));
end
fclose(fid);
