
MISC=../data/output/misc
ENSEMBLE=100

echo "Procssing run : $1"
echo "Time split : < $3, [$3 $4], > $4"

perl networksummarize.pl $1 $2

perl authorgraphgenrelax.pl $1 $2
perl authorgraphgenrelaxtab.pl $1 $2 >> ../data/output/transcollabcounts.txt

perl zP.pl $1
perl edgeswithnoderoles.pl $1
perl snetrandomize.pl $1 $ENSEMBLE
perl guimeraconprofile.pl $1 $2 $ENSEMBLE

matlab -nojvm -r "guimeranormalizeprofile('$1')"

cat ../data/output/guimeraprofile/$1.txt | awk '{print $3}' > ../data/output/guimeravecs/$1.txt

perl clustersize.pl $1 $2
perl yearinfo.pl $1 $2 $3 $4

perl genericjoin.pl $MISC/$1.authcount.txt $MISC/$1.pubs.txt $MISC/$1.hubcount.txt > ../data/output/clustercat/$1.marked.txt
perl genericjoin.pl $MISC/$1.authcount.txt $MISC/$1.pubs.txt $MISC/$1.yearly.txt > ../data/output/clustercat/$1.lim.txt
