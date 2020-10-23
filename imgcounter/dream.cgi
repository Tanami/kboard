#!/usr/bin/perl

#---------------------------------------#
#  DREAM COUNTER v2.31 (2001/03/04)	#
#  Copyright(C) Kent Web 2001		#
#  webmaster@kent-web.com		#
#  http://www.kent-web.com/		#
#---------------------------------------#

#--- [注意事項] ------------------------------------------------#
# 1. このスクリプトはフリーソフトです。このスクリプトを使用した	#
#    いかなる損害に対して作者は一切の責任を負いません。		#
# 2. 設置に関する質問はサポート掲示板にお願いいたします。	#
#    直接メールによる質問は一切お受けいたしておりません。	#
#---------------------------------------------------------------#

# [タグの書き方の例] (*** はログファイル名)
#
#  ・カウンタ <img src="count/dream.cgi?id=***">
#  ・時刻表示 <img src="count/dream.cgi?mode=time">
#  ・カレンダ <img src="count/dream.cgi?mode=date">
#  ・ファイルの更新時間
#             <img src="count/dream.cgi?file=/home/～/index.html">
#             [注意] --> /home/～/index.htmlの部分はフルパスを指定
#
#  * 応用例(id名を kent と仮定)＊
#    1.画像を変更するとき：(以下はgif2ディレクトリの画像指定例)
#      <img src="パス/dream.cgi?id=kent&gif=2">
#    2.数字をランダムに表示するとき：
#      <img src="パス/dream.cgi?mode=rand">
#    3.カウンタ桁数を７桁にするとき：
#      <img src="パス/dream.cgi?id=kent&fig=7">
#
#  * チェックモード ( mode=check という引数をつけて呼び出す）
#    http://～～/dream.cgi?mode=check
#
# [ディレクトリ構成例 (かっこ内はパーミッション)]
#
#    public_html / index.html(ここにカウンタ等を表示)
#          |
#          +-- count [777] / dream.cgi  [755]
#                |           gifcat.pl  [644]
#                |           index.dat  [666] .. ログファイル1
#                |           index2.dat [666] .. ログファイル2
#                |              :                    :
#                |           xxxxx.dat  [666] .. ログファイルx
#                |
#                +-- gif1 / 0.gif .. 9.gif, a.gif, p.gif, c.gif, d.gif
#                |
#                +-- gif2 / 0.gif .. 9.gif, a.gif, p.gif, c.gif, d.gif
#                     :

#============#
#  設定項目  #
#============#

# 画像連結ライブラリ取込み
require './gifcat.pl';

# IPアドレスのチェック (0=no 1=yes) 
#   → yesの場合連続したIPアドレスはカウントアップしない
$ip_chk = 1;

# ログの自動生成 (0=no 1=yes)
$id_creat = 0;

# ログを置くサーバディレクトリ
#   → 現行ディレクトリであればこのままでよい
#   → 最後は必ず / で閉じる
#   → フルパスなら / から始める（http://からではない）
$LogDir = './';

# ファイルロック形式 (0=no 1=symlink関数 2=open関数)
$lockkey = 0;

# ロックファイルのサーバディレクトリ
#   → 現行ディレクトリであればこのままでよい
#   → 最後は必ず / で閉じる
#   → フルパスなら / から始める（http://からではない）
$LockDir = './';

# 画像のあるサーバディレクトリの指定
#   → フルパスなら / から始める（http://からではない）
sub gif_path {
	$gifdir  = "./gif$gif"; # gif画像のあるディレクトリのパス
	$defodir = "./gif1";	# デフォルト（初期値）のディレクトリ
}

# 他サイトからアクセスを排除する場合
#   → dream.cgiを設置するURLを http://から記述
$base_url = "";

#============#
#  設定完了  #
#============#

# 他サイトからのアクセスを排除
if ($base_url) {
	$ref_url = $ENV{'HTTP_REFERER'};
	$ref_url =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	if ($ref_url !~ /$base_url/i) { &error; }
}

# デコード処理
$buffer = $ENV{'QUERY_STRING'};
if ($buffer) {
	@pairs = split(/&/, $buffer);
	foreach (@pairs) {
		($name, $value) = split(/=/);
		$value =~ tr/+/ /;
		$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

		$value =~ s/\r//g;
		$value =~ s/\n//g;
		$value =~ s/\t//g;

		$in{$name} = $value;
	}
	$mode = $in{'mode'};
	$gif  = $in{'gif'};
	$fig  = $in{'fig'};
	$id   = $in{'id'};
	$id   =~ s/\W//g;
}
# 引数がなければランダムモード
else {
	$mode = 'rand';
}

# GIFディレクトリを定義
&gif_path;

# デフォルトディレクトリを定義
if ($gif eq "") { $gifdir = $defodir; }

## 時間処理
if ($mode eq "time") {
	# 時間を取得
	&get_time;

	# 24時間制の場合
	if ($in{'type'} == 24) {
		($t1,$t2) = split(//, $hour);
		($t3,$t4) = split(//, $min);

		@caras = ("$t1","$t2","c","$t3","$t4");
	}
	# 12時間制の場合
	else {
		if ($hour >= 12) {
			$hour = sprintf("%02d",$hour -12);
			$head = 'p';
		}
		else { $head = 'a'; }

		($t1,$t2) = split(//, $hour);
		($t3,$t4) = split(//, $min);

		@caras = ("$head","$t1","$t2","c","$t3","$t4");
	}
}
## カレンダ処理
elsif ($mode eq "date") {
	# 時間を取得
	&get_time;

	($dmy1,$dmy2,$d1,$d2) = split(//, $year);

	($d3,$d4) = split(//, $mon);
	($d5,$d6) = split(//, $mday);

	if ($in{'year'} eq '4') {
		@caras = ("$dmy1","$dmy2","$d1","$d2","d","$d3","$d4","d","$d5","$d6");
	} else {
		@caras = ("$d1","$d2","d","$d3","$d4","d","$d5","$d6");
	}
}

## 更新時間表示処理
elsif ($in{'file'}) {
	# ファイルがなければエラー
	unless (-e $in{'file'}) { &error; }

	# 更新日数を取得
	($mtime) = (stat("$in{'file'}"))[9];

	# 更新時間を文字分割
	&get_time($mtime);
	($y1,$y2,$y3,$y4) = split(//, $year);
	($mon1,$mon2) = split(//, $mon);
	($day1,$day2) = split(//, $mday);
	($hr1,$hr2)   = split(//, $hour);
	($min1,$min2) = split(//, $min);

	# スラッシュ "/" がなければダッシュ "-" で代用
	if (-e "$gifdir\/s.gif") { $s = 's'; }
	else { $s = 'd'; }

	# 配列化
	@caras = ("$y1","$y2","$y3","$y4","$s","$mon1","$mon2","$s",
			"$day1","$day2","d","$hr1","$hr2","c","$min1","$min2");
}

## ファイルサイズ数表示処理
elsif ($in{'size'}) {
	# ファイルがなければエラー
	unless (-e $in{'size'}) { &error; }

	# サイズ数を取得 (bytes)
	($size) = (stat("$in{'size'}"))[7];

	# 単位変換（四捨五入）
	if ($in{'p'} eq 'k') { $size = int ($size / 1024 +0.5); }
	elsif ($in{'p'} eq 'm') { $size = int ($size / 1048576 +0.5); }

	# サイズ数を配列化
	@caras=();
	foreach (0 .. length($size)-1) {
		$n = substr($size,$_,1);
		push(@caras,$n);
	}
}
## チェックモード
elsif ($mode eq "check") {
	&check;
}

## カウンタ処理
if ($id ne "" && $mode ne "rand") {
	# ログを定義
	$logfile = "$LogDir$id\.dat";

	# ログの存在をチェック
	unless(-e $logfile) {
		# ログ生成 [なし] ならプログラムを終了
		if ($id_creat == 0) { &error; }

		# ログ生成 [あり] ならログを生成
		else {
			open(OUT,">$logfile") || &error;
			print OUT "0";
			close(OUT);

			# パーミッションを 666 へ
			chmod (0666,"$logfile");
		}
	}

 	# ロックファイル名を定義
	$lockfile = "$LockDir$id\.lock";

	# デフォルト桁数を定義
	if ($fig eq "") { $fig = 5; }

	# IPアドレスを取得
	$addr = $ENV{'REMOTE_ADDR'};

	# ロック開始
	if ($lockkey == 1) { &lock1; }
	elsif ($lockkey == 2) { &lock2; }

	# 記録ファイルから読み込み
	open(IN,"$logfile") || &error;
	$data = <IN>;
	close(IN);

	# 前バージョン変換処理
	if ($data =~ /<>/) { ($daykey,$data) = split(/<>/, $data); }

	# 記録ファイルを分解
	($count,$ip) = split(/:/, $data);

	# IPチェック
	$flag=0;
	if ($ip_chk && $addr eq "$ip") { $flag=1; }

	# ログ更新
	if (!$flag) {
		# カウントアップ
		$count++;

		# ファイルをフォーマット
		if ($ip_chk) { $data = "$count\:$addr"; }
		else { $data = "$count"; }

		# 記録ファイルを更新する
		open(OUT,">$logfile") || &error;
		print OUT $data;
		close(OUT);
	}

	# ロック解除
	if (-e $lockfile) { unlink($lockfile); }
}

## 乱数発生
if ($mode eq "rand") {
	srand;
	$count = rand;
	$count = int($count * 10000);

	# デフォルト桁数を定義
	if ($fig eq "") { $fig = 5; }
}

## GIF画像を出力
&count_view;
exit;

#---------------#
#  GIF出力処理  #
#---------------#
sub count_view {
	# 時間表示およびカレンダ表示処理
	if ($mode eq "time" || $mode eq "date" || $in{'file'} || $in{'size'}) {
		@GIF = ();
		foreach (0 .. $#caras) { push(@GIF, "$gifdir/$caras[$_].gif"); }
	}

	# カウンタ表示処理
	else {
		while (length($count) < $fig) { $count = '0' . $count; }
		$length = length($count);
		@GIF=();
		foreach (0 .. $length-1) {
			$n = substr($count,$_,1);
			push(@GIF,"$gifdir/$n\.gif");
		}
	}

	print "Content-type: image/gif\n\n";
	binmode(STDOUT);
	print &gifcat'gifcat(@GIF);
}

#-----------------------------------#
#  ロックファイル処理：symlink関数  #
#-----------------------------------#
sub lock1 {
	local($retry) = 5;
	while (!symlink(".", $lockfile)) {
		if (--$retry <= 0) { &error; }
		sleep(1);
	}
}

#--------------------------------#
#  ロックファイル処理：open関数  #
#--------------------------------#
sub lock2 {
	local($retry) = 0;
	foreach (1 .. 5) {
		if (-e $lockfile) { sleep(1); }
		else {
			open(LOCK,">$lockfile") || &error;
			close(LOCK);
			$retry = 1;
			last;
		}
	}
	if (!$retry) { &error; }
}

#--------------#
#  時間を取得  #
#--------------#
sub get_time {
	$ENV{'TZ'} = "JST-9";
	$times = time;

	if ($_[0]) { $times = $_[0]; }

	($sec,$min,$hour,$mday,$mon,$year) = localtime($times);
	$year += 1900;
	$mon++;
	if ($hour < 10) { $hour = "0$hour"; }
	if ($min  < 10) { $min  = "0$min";  }
	if ($mon  < 10) { $mon  = "0$mon";  }
	if ($mday < 10) { $mday = "0$mday"; }
}

#--------------#
#  エラー処理  #
#--------------#
sub error {
	if (-e $lockfile) { unlink($lockfile); }

	@err_gif = ('47','49','46','38','39','61','2d','00','0f','00','80','00','00','00','00','00','ff','ff','ff','2c', '00','00','00','00','2d','00','0f','00','00','02','49','8c','8f','a9','cb','ed','0f','a3','9c','34', '81','7b','03','ce','7a','23','7c','6c','00','c4','19','5c','76','8e','dd','ca','96','8c','9b','b6', '63','89','aa','ee','22','ca','3a','3d','db','6a','03','f3','74','40','ac','55','ee','11','dc','f9', '42','bd','22','f0','a7','34','2d','63','4e','9c','87','c7','93','fe','b2','95','ae','f7','0b','0e', '8b','c7','de','02','00','3b');

	print "Content-type: image/gif\n\n";
	foreach (@err_gif) {
		$data = pack('C*',hex($_));
		print $data;
	}
	exit;
}

#------------------#
#  チェックモード  #
#------------------#
sub check {
	print "Content-type: text/html\n\n";
	print "<html><head><title>DREAM COUNTER</title></head>\n";
	print "<body>\n<h2>Check Mode</h2>\n<UL>\n";

	# ログファイル検索
	opendir(DIR,"$LogDir")
		|| print "<LI>ディレクトリを認識できません: $LogDir\n";
#	@dir = readdir(DIR);
	@dir = grep { /\.dat$/ && -f "$LogDir$_" } readdir(DIR);
	closedir(DIR);

	$flag=0;
	foreach (@dir) {
		$target = "$LogDir$_";
#		if (-d "$LogDir$_") { next; }
#		if ($_ !~ /(.+)\.dat$/) { next; }

		if (-r $target && -w $target) { print "<LI>$_ : パーミッションOK \n"; }
		elsif (!-r $target) { print "<LI>$_ : 読込みパーミッションNG \n"; }
		elsif (!-w $target) { print "<LI>$_ : 書込みパーミッションNG \n"; }
		$flag=1;
	}
	if (!$flag) { print "<LI>ログファイルが存在しません\n"; }

	if ($gif ne "") { $target_dir = $gifdir; }
	else { $target_dir = $defodir; }

	# 画像ディレクトリのパス確認
	if (-d $target_dir) { print "<LI>$target_dir : 画像ディレクトリのパス : OK! \n"; }
	else { print "<LI>$target_dir : 画像ディレクトリがありません\n"; }

	# 画像チェック
	@GifFile = ("0".."9", "a", "p", "c", "d");
	foreach (@GifFile) {
		$target = "$target_dir\/$_\.gif";
		if (-e "$target") { print "<LI>$target : 画像OK \n"; }
		else { print "<LI>$target : 画像がありません\n"; }
	}

	# 著作権表示：削除改変を禁止します
	print "</UL>\n<P><small><!-- $ver -->\n";
	print "Copyright(C) <a href='http://www.kent-web.com/' target='_top'>Kent Web</a> 2001\n";
	print "</small>\n</body></html>\n";
	exit;
}
