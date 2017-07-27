use LWP::Simple qw(getstore);
use File::Path;
use utf8;
use strict;

#This section will find the hrefs to the first 6 articles on the main page, and return an array of links
sub getHrefs {
	my $mainpage=LWP::Simple::get("https://app.hedgeye.com/insights/all?type=insight");
	my @popHrefs = ($mainpage =~ /\<a class=\'popular-this-week__heading--link\' href=\'(.+)\'\>/g);
	my @latestHrefs = ($mainpage =~ /\<a class=\'latest-insights__heading--link\' href=\'(.+)\'\>/g);
	my @hrefs = @popHrefs[0..4];
	push (@hrefs, @latestHrefs[0]);
	foreach(@hrefs){
		$_="https://app.hedgeye.com$_";
	}
	return @hrefs;
}

my @links = getHrefs();
#foreach(@links)
#	print "$_\n"
#

#this subroutine calls all the collection subroutines on the given url, and writes the directories and files
sub collectFrom {
	my $url = $_[0];
	my $page=LWP::Simple::get($url);
	my @dateTime = getDateTime($page);
	my $headline = getHeadline($page);
	my $dlDir = join('_', split(/\W/, $headline)).'/';
	mkpath ([$dlDir],1,0711);
	my @author;
	if(hasAuthor($page)==1){
		#print "has author\n";
		@author = getAuthor($page);
	}
	else{
		push(@author,"Author not specified");
	}
	my $contentBodyHtml = getContent($page);
	getImage($page, $dlDir);
	open(my $wh, '>', "$dlDir/collected.csv");
	print $wh "datetime and timezone:\n";
	foreach(@dateTime){
		print $wh "$_,";
	}
	print $wh "\nHeadline:\n";
	print $wh $headline;
	print $wh "\nAuthor:\n";
	foreach(@author){
		print $wh "$_,";
	}
	print $wh "\nContent Body HTML:\n";
	print $wh $contentBodyHtml;
	print $wh "\n";
	#below I provide alternate code to write the ContentBodyHTML to a txt
	#I am providing this because in the body of these articles are commas
	#when those commas are read as part of a CSV, strange and likely unwanted formatting can occur
	###################
	#open(my $body, '>', "$dlDir/contentBodyHtml.txt");
	#print $body "\nContent Body HTML:\n";
	#print $body $contentBodyHtml;
	#print $body "\n";
	#close $body;
	###################
	close $wh;
}
#this subroutine determines if the article has an author
sub hasAuthor {
	my ($page) = @_;
	if($page=~m/\<div class=\'full-name\'\>/){
		return 1;
	}
	else{
		return 0;
	}
}

#this subroutine gathers author data
sub getAuthor {
	my ($page) = @_;
	my @authorInfo;
	if($page=~ /<div class=\'headshot\'>(.+)src=\"(.+)\"/){
		push(@authorInfo, $2);
	}
	if($page=~ /<div class=\'full-name\'>(.+)</) {
		push(@authorInfo, $1);
	}
	if($page=~ m/\<div class=\'twitter-handle\'\>/){
		if($page=~ /\<a href=\"http\:\/\/twitter.com\/(\@.+)\"\s/){
			push (@authorInfo, $1);
		}
	}
	return @authorInfo;
}

#this subroutine gathers date and time data
sub getDateTime {
	my ($page) = @_;
	my @dateTime;
	if($page=~ /<time datetime=\'(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2})(.\d{2}:\d{2})\'/){
		push(@dateTime, ($1, $2, $3));
	}
	return @dateTime;
}

#this subroutine finds the Headline
sub getHeadline {
	my ($page) = @_;
	my $headline;
	if($page=~ /headline_droid\'\sitemprop=\'name\'>\n(.+)\n/){
		$headline = $1;
		$headline=~ s/[^[:ascii:]]+//g;
	}
	return $headline;
}

#this soubroutine gathers the content of the articleBody
sub getContent {
	my ($page) = @_;
	my $content;
	if($page=~/<div\sitemprop=\'articleBody\'\sstyle=\'clear\:both\'>\n(.+)\n<\/div>\n<div\sclass=\'author-tag\'>/s){
		$content = $1;
		$content=~ s/[^[:ascii:]]+//g;
	}
	return $content;
}

#this subroutine downloads the first image in the article body, and saves it to the hard drive
sub getImage {
	my $page = $_[0];
	my $dir = $_[1];
	my $imgUrl;
	my $type;
	if($page=~/<div\sitemprop=\'articleBody\'\sstyle=\'clear\:both\'>\n.+<a href="(https:\/\/.+\.(png|jpg))"\srel="popover">/s){
		$imgUrl = $1;
		$type = $2;
	}
	my $save = "$dir/first_image.$type";
	getstore($imgUrl,$save);
}

#this loop runs collectFrom on the first six articles
foreach(@links){
	collectFrom($_);
}

#this creates the run instructions file
open(my $wh, '>', "run_instructions.txt");
print ($wh 
		"Created by William Stoddard\nWritten in Perl, on a Windows desktop running Strawberry Perl 5.26.0.1 64bit\nto run, simply execute the grabber.pl script\n");
