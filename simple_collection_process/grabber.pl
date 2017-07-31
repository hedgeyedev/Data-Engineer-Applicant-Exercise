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
	my $dlDir = 'image_'.join('_', split(/\W/, $headline)).'/';
	mkpath ([$dlDir],1,0711);
	my @author;
	if(hasAuthor($page)==1){
		#print "has author\n";
		@author = getAuthor($page);
	}
	else{
		push(@author,"n/a,n/a,n/a");
	}
	my $contentBodyHtml = getContent($page);
	getImage($page, $dlDir);
	open(my $wh, '>>', "collected.csv");
	#below I have included optional code to organize the csv files into separate files and folders,
	#rather than have all the information in one large csv
	###################
	#open(my $wh, '>', "$dlDir/collected.csv");
	###################
	#comment out line 42, uncomment line 45, and remove the " 'image_'. " from line 30 to implement
	print $wh "$headline,";
	foreach(@dateTime){
		print $wh "$_,";
	}
	foreach(@author){
		print $wh "$_,";
	}
	#to remove commas and newlines from contentBodyHtml:
	$contentBodyHtml=~s/,/ /g;
	$contentBodyHtml=~s/\n//g;
	#uncomment the following lines to remove the majority of html tags from contentBodyHtml.
	#Warning: the regex is not perfect yet, may remove some body content in addition to the html tags.
	###################
	#$contentBodyHtml=~s/<[\/apbh3iem]{1,3}>//g;
	#$contentBodyHtml=~s/<\/*span( style=['"].+['"])*>//g;
	#$contentBodyHtml=~s/<\/*div( class=['"].+['"])*>//g;
	#$contentBodyHtml=~s/<\/*a href=['"].+['"]( (target=['"].*['"])|(rel=['"].*['"])|(data-slimstat=['"].*['"]))*>//g;
	#$contentBodyHtml=~s/<\/*img alt=['"].*['"]( (class=['"].*['"])|(sizes=['"].*['"])|(src=['"].*['"])(srcset=['"].*['"]))* *\/*>//g;
	#$contentBodyHtml=~s/<\/*strong>//g;
	###################
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
	}else{push(@authorInfo, "n/a");}
	if($page=~ /<div class=\'full-name\'>(.+)</) {
		push(@authorInfo, $1);
	}else{push(@authorInfo, "n/a");}
	if($page=~ m/\<div class=\'twitter-handle\'\>/){
		if($page=~ /\<a href=\"http\:\/\/twitter.com\/(\@.+)\"\s/){
			push (@authorInfo, $1);
		}
	}else{push(@authorInfo, "n/a");}
	return @authorInfo;
}

#this subroutine gathers date and time data
sub getDateTime {
	my ($page) = @_;
	my @dateTime;
	if($page=~ /<time datetime=\'(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2})(.\d{2}:\d{2})\'/){
		push(@dateTime, ($1, $2, $3));
	}else{push(@dateTime, "n/a");}
	return @dateTime;
}

#this subroutine finds the Headline
sub getHeadline {
	my ($page) = @_;
	my $headline;
	if($page=~ /headline_droid\'\sitemprop=\'name\'>\n(.+)\n/){
		$headline = $1;
		$headline=~ s/[^[:ascii:]]+//g;
	}else{$headline= "n/a";}
	return $headline;
}

#this soubroutine gathers the content of the articleBody
sub getContent {
	my ($page) = @_;
	my $content;
	if($page=~/<div\sitemprop=\'articleBody\'\sstyle=\'clear\:both\'>\n(.+)\n<\/div>\n<\/div>\n<\/article>/s){
		$content = $1;
		$content=~ s/[^[:ascii:]]+//g;
	}else{$content="n/a";}
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
open(my $wh, '>', "collected.csv");
print $wh "Headline,Date,Time,Timezone,Author Headshot Href,Name,Twitter Handle,Content Body HTML\n";
close $wh;
foreach(@links){
	collectFrom($_);
}

#this creates the run instructions file
open(my $ri, '>', "run_instructions.txt");
print ($ri "Created by William Stoddard\nWritten in Perl, on a Windows desktop running Strawberry Perl 5.26.0.1 64bit\nCPAN Modules needed:\n\tLWP::Simple\n\tFile::Path\nTo run, execute the grabber.pl script\n");
