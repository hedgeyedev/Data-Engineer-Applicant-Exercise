open(my $fh, '<', "collected.csv");
open(my $wh, '>', "debug.txt");
my $i = 0;
while (my $line = <$fh>){
	$line=~/(.+),(.+),(.+),(.+),(.+),(.+),(.+),(.+)\n/;
	print $wh "$i\n$1\n$2\n$3\n$4\n$5\n$6\n$7\n$8\n\n";
	$i++;
}
close $fh;
close $wh;