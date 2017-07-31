open(my $fh, '<', "collected.csv");
open(my $wh, '>', "debug.txt");
my $i = 0;
#the following code is written as such for demonstrative clarity, not for efficiency.
#split(/,/,$line) would be more efficient, but does not as clearly show the structure
#of one line of collected.csv. This test visually shows that each line consists of 
#exactly 8 comma-separated values followed by a newline.
while (my $line = <$fh>){
	$line=~/(.+),(.+),(.+),(.+),(.+),(.+),(.+),(.+)\n/;
	print $wh "$i\n$1\n$2\n$3\n$4\n$5\n$6\n$7\n$8\n\n";
	$i++;
}
close $fh;
close $wh;
