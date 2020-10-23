#!/usr/bin/perl

# アイコンアップロード用掲示板(^^)
# 改造・再配布可
# Copyright 1999,2000 Qz...?
#--------------------------------------------------------
# Modified by SHIRO 2001/06/08
# e-mail      s-o-yama@fa2.so-net.ne.jp
# homepage    www.kyoshin-sj.co.jp/oyama/
# KBOARD SHIRO'S VERSION 用に改変
# "専用" は実質機能していません。
#--------------------------------------------------------
$| = 1;
$VER = '1.60';

#--１ページの表示件数
$PageCount = 5;

#--改ページマークの設定
#  画像の指定も可能です。
$PrevPageMark = '<small>←前のページ</small>';
$NextPageMark = '<small>次のページ→</small>';

#--URLマークの設定
#  画像の指定も可能です。
$HomeMark = '[HOME]';

#--管理者用登録のための設定
$AdminName = '管理人';               #あなたのおなまえ
$AdminMail = 'xx@xx.xx.xx';              #あなたのメールアドレス
$AdminComment = '管理人登録です';    #登録メッセージ

###################################
###　必須項目の設定　　　　　　####
###################################

$JcodeLib = './jcode.pl';	#--漢字ライブラリ jcode.pl のファイル名
$CharCode = 'sjis';		#--漢字コード（'sjis' 'euc' 'jis'）
$addminpass = "0123";	#--管理者パスワード(必ず変更してください)
$ReturnBBS = "./kboard.cgi";	#--戻り先掲示板ＵＲＬ
$icon_url = "gif/icon";         #Pathで指定してください。
$IconPath = "gif/icon";

###################################
###　必須項目の設定の終了　　　####
###################################

###################################
###　画像保存の動作設定　　    ####
###################################

#--保存ＯＫの容量(単位KB, 0:無制限)
$MaxPicSize = 20;

#--保存ＯＫの縦サイズ(0:無制限)
$MaxPicHeight = 60;

#--保存ＯＫの横サイズ(0:無制限)
$MaxPicWidth = 60;

#--保存件数(0:無制限)
$MaxSaveCount = 0;

#--記事削除時の画像ファイル削除(1:削除 0:削除しない)
$PicDeiMode = 1;

###################################
###　タイトル・画面色の設定　　####
###################################

#--Titleタグの名前｡  タグ入りでの設定は、しないで下さい｡
$HeadTitle = "専用アイコン登録";

#--掲示板タイトル
$TopTitle = <<'_____E_';
<Center>
<Font Color=#DD0000 Size=+2>
アイコン登録コーナー
</Font>
</Center>
_____E_
#↑ _____E_ は削除しないでください。

#--各種色設定
$BackColor  = "#ADDEFC";			# 背景色を指定
$TextColor  = "#000000";			# 文字色を指定
$LinkColor  = "#0000FF";			# リンク色を指定（未リンク）
$VLinkColor = "#0000FF";			# リンク色を指定（既リンク）
$ALinkColor = "#FF0000";			# リンク色を指定（リンク中）

$IN_TBL_Color = "C0C0C0";			# 入力画面のテーブル背景色
$IN_IMG_Color = "FF8040";			# 入力画面のイメージ欄の色

#--背景画像(未指定なら、表示しません)
$BackGround = "";

###############################################
###　応用設定（必要に応じて変更して下さい　####
###############################################

#--このＣＧＩの名称またはＵＲＬ｡  未指定なら、自動取得
$ThisCGI = "pup.cgi";

#--保存ログファイル名
$SaveFile = "iconfile.log";

#--保存セキュリティーモード
#  0-誰でも登録可能
#  1-パスワードによる制限
#  2-基本的に誰でも登録可能だけど、登録するリモートホストに制限をかける
$SaveMode = 0;

#--登録用パスワード(保存セキュリティーモードが１のときに必要)
$UserPass = "userpass";

#--登録不可リモートホスト名(保存セキュリティーモードが２のときに必要)
$NGRemortHost =<<'_____E_';
a
aa
aaa
_____E_
#↑ _____E_ は削除しないでください。

#--プロキシを通しての登録不可(0-OK 1-不可)
#  これって、うまく動作するか、謎:-)
$ProxyNG = 0;

#--クッキーに登録用パスワードを保存する(0:しない 1:する)
$CookieUserPassSave = 1;

#--クッキーに保存する日数
$CookieDay = 30;

#--クッキー識別名
$CookieID = "pup";

#--ロック(0:しない 1:する)
$LockMode = 0;

#--ロックファイル名
$LockFile = "pup_lock";

###########################
###　応用設定　終了  　####
###########################

#;___以上で設定は終わりです____________________________;

#;_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
#;処理
#;_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
#_簡易設定チェック
&PrintErrHtml("$JcodeLibが見つかりません。") unless(-e $JcodeLib);
&PrintErrHtml("$SaveFileが見つかりません。") unless(-e $SaveFile);
&PrintErrHtml("$IconPathが見つかりません。") unless(-e $IconPath);
require $JcodeLib;
#未指定なら、自動取得
unless($THIS_CGI){
	($THIS_CGI) = ($ENV{SCRIPT_NAME} || $0 ) =~ m|/([^/]+)$|;
}

#;メイン処理______________________________________________________________;
&FormDecord;
if($FORM{'ACTION'} eq "REGIST"){
	&ExecSave;
}elsif($FORM{'ACTION'} eq "DELETE"){
	&ExecDelete;
}else{
	&PrintLogHtml;
}
exit(0);


#;最上部表示______________________________________________________________;
sub PrintTopHtml
{
local($BG) = "BackGround=\"$BackGround\"" unless($BackGround eq "");
&GetJapanCode;
print "Content-type: text/html\n\n";
print <<"_____E_";
<HTML>
<HEAD>
<Meta Http-Equiv="Content-type" Content="text/html; charset=$CharSet">
<TITLE>$HeadTitle</TITLE>
</HEAD>
<Body $BG BGColor=$BackColor Text=$TextColor Link=$LinkColor VLink=$VLinkColor ALink=$ALinkColor>
<A Href="$ReturnBBS">▲ 掲示板に戻る</A>
$TopTitle
_____E_
}

#;使用方法表示____________________________________________________________;
sub PrintGuidHtml
{
print <<"_____E_";
<Center>
<HR Width="80%">
<Table Width="80%">
<TR><TD>■ アイコン(画像ファイル)をゲストの方のパ\ソ\コ\ン\から直接、掲示板のサーバに登録出来ます。</TD></TR>
<TR><TD>■ 登録できる画像は、Jpeg画像、GIF画像、PNG画像のみとなっております。</TD></TR>
<TR><TD>■ 画像は、ファイルサイズ：$MaxPicSize Kbyte、横：$MaxPicWidth Ｘ縦：$MaxPicHeight 以内のものが登録できます。</TD></TR>
<TR><TD>■ 著作権などを考慮して、問題のない画像を登録してください。</TD></TR>
<TR><TD>■ NetScape Navigater 3以上、Internet Explorler 4以上の方しか、ご利用できません。</TD></TR>
<TR><TD>■ Internet Explorler 3.0 をお使いの方は、以下のＵＲＬからプラグインが入手できます。</TD></TR>
<TR><TD Align=Center><a href="http://www.microsoft.com/ie_intl/ja/download/ie3add.htm">http://www.microsoft.com/ie_intl/ja/download/ie3add.htm</A></TD></TR>
</Table>
<HR Width="80%">
</Center>
_____E_
}

#;登録できないよ～メッセージ部表示__________________________________________;
sub PrintNoRegist
{ #メッセージはかなりいい加減？
print <<"_____E_";
<center>
<p><em>
アイコン登録件数が、$MaxSaveCount件に、到達したので、
現在、アイコンの登録は、できません。
</em><p>
</center>
_____E_
}

#;最下部表示（著作権表示、削除不可！）______________________________________;
sub PrintBottomHtml
{
print <<"_____E_";
<Center>
<HR Width="80%">
<Font Color=$TextColor><Small>
<A Href="mailto:qz\@ca.sakura.ne.jp">- Pup Ver $VER by Qz - </A><P> 
<A Href="http://homepage.nifty.com/mystaff/" target="_top">Modified By Season</A>
</Small></Font>
</Center>
</Body>
</Html>
_____E_
}

#;エラー表示______________________________________________________________;
sub PrintErrHtml
{
	&FileUnLock if($LOCK_SW);
	&PrintTopHtml;
	print "<Table Width=\"100%\" Height=\"80%\"><TR><TD Align=Center Valign=Center>\n";
	print "<Table Width=400 Border=1>\n";
	print "<TR><TD Align=Center><B>エラー</B></TD></TR>\n";
	print "<TR><TD Height=200 VAlign=Center Align=Center>\n";
	print $_[0];
	print "\n</TD></TR>\n";
	print "<TR><TD Align=Center>ブラウザの戻るボタンでお戻りください。\n";
	print "\n</TD></TR></Table>\n";
	print "\n</TD></TR></Table>\n";
	&PrintBottomHtml;
	exit(0);
}

#;ログ表示処理____________________________________________________________;
sub PrintLogHtml
{
	#;クッキー取得
	&GetCookie;

	#;ログ読込
	open(IN,"$SaveFile") || &PrintErrHtml("保存ファイルの読み込みに失敗しました。<BR>原因:$!");

	#ログの件数を数える
	local($lcnt)= 0;
	$lcnt++ while(<IN>);
	
	&PrintTopHtml;

	if(($MaxSaveCount > 0) && ($MaxSaveCount <= $lcnt)){
		#保存件数が最大保存件数より大きいので、
		#登録できないようにする
		
		#登録できない文の表示
		&PrintNoRegist;
		
	}else{

		#;投稿フォーム表示
		&PrintRegistForm;
	
		#;説明文の表示
		&PrintGuidHtml;
	}

	#ログを巻き戻す
	seek(IN, 0, 0);

	#;記事一覧表示
	print "<Form Action=\"$ThisCGI\" Method=\"POST\">\n";
	print "<Input Type=\"Hidden\" Name=\"ACTION\" Value=\"DELETE\">\n";
	print "<Center>\n";

	local($cnt) = 0;
	local($start_cnt) = $PageCount * $FORM{'PAGE'}; #開始位置
	local($end_cnt)   = $start_cnt + $PageCount;    #終了位置

	while(<IN>){
		next if($start_cnt > $cnt++);
		last if($end_cnt   < $cnt);
		
		($pfn, $ptitle, $ptime, $ppwd, $pno, $pdate, $pname, $pmail, $pmsg,
			$phost, $pw, $ph, $ptype, $plen, $progname, $purl, $only
		)= split(/\,/, $_);
		$LinkNmae = "<A Href=\"mailto:$pmail\">$pname</A>";
		if ($purl) { $LinkURL  = "<A Href=\"http://$purl\">$HomeMark</A>"; 
		}else 	   { $LinkURL  = ""; }
		if ($only) { $only = "（$pname専用）"; 
		}else	   { $only = "（共用アイコン）"; }
		$property = "(w$pw x h$ph, $plen byte, $ptype ,$progname)";
print <<"_____E_";
<!--
[$pno Infomation]
name:$pname
mail:$pmail
url:$purl
host:$phost
progname:$progname
-->
<Table Border=1 Width="80%"><TR><TD>
<Table Border=0 Bgcolor=$IN_TBL_Color Width="100%">
<TR>
<TD Width="50%"><B>[$pno] $ptitle</B> $only</TD>
<TD Align=Right><Small>$property <Input Type="CheckBox" Name="ID" Value="$ptime"></Small></TD>
</TR></Table>
<Table Border=0 Width="100%">
<TR><TD RowSpan=10 Width="10%"><Img Src="$icon_url/$pfn" Alt="$pfn" Width=$pw Height=$ph></TD></TR>
<TR><TD ColSpan=2> 登録者：$LinkNmae<Small> 登録日：$pdate $LinkURL</Small></TD></TR>
<TR><TD ColSpan=2>コメント＞$pmsg</TD></TR>
</Table></TR></TD></Table><BR>
<!-- _____________________________________________________ -->
_____E_
	} #-- end of loop

	close(IN); #ここで、ファイルを閉じる

	#ページボタン
	#   レイアウト的にここでいいのかな・・・
	#  ちなみに、qq は、" の代わりに使用できるものです。
	#  "でかこまれた中に、" がある場合、\ をつけずにすむので便利
	#  q がいっこのときは、' の代わりにつかえる
	#  qq() や、qq!! q// などのように使用します。
	#  qq の次の文字で、なかの文字を囲めます。
	#
	if($FORM{'PAGE'} > 0){
		$prev_page = $FORM{'PAGE'} - 1;
		print qq| <a href="$THIS_CGI?PAGE=$prev_page">$PrevPageMark</a> |;
	}
	if($end_cnt < $lcnt){
		$next_page = $FORM{'PAGE'} + 1;
		print qq| <a href="$THIS_CGI?PAGE=$next_page">$NextPageMark</a> |;
	}

	print "<Table Width=\"80%\"><TR><TD Align=Right>";
	print "<Small>登録キー：</Small>\n";
	print "<Input Type=\"PassWord\" Size=10 Name=\"DELKEY\" Value=\"$COOKIE{'MYPWD'}\">\n";
	print "<Input Type=\"Submit\" Value=\"削除\">\n";
	print "</TD></TR></Table></Form></Center>\n";

	&PrintBottomHtml;
}

#;投稿フォーム表示________________________________________________________;
#下記のフォームから1行削除
#<Input Type="Hidden" Name="ADMIN" Value="MATOME">
#if("ADMIN"=="MATOME"){$FORM{'ADMIN'} = 'MATOME'} 追加する場所？

sub PrintRegistForm
{
print <<"_____E_";
<Form Action="$ThisCGI" Method="POST" Enctype="multipart/form-data">
<Input Type="Hidden" Name="ACTION" Value="REGIST">
<Center>
<Table Border=0>
_____E_

if($SaveMode == 1){
print <<"_____E_";
<TR>
<TD Bgcolor=$IN_IMG_Color>登録用パスワード</TD>
<TD Bgcolor=$IN_IMG_Color><Input Type="Password" Name="WRITEPASS" Size=20" Value="$COOKIE{'WRITEPASS'}"></TD>
</TR>
_____E_
} #-- end of if

print <<"_____E_";
<TR>
<TD Bgcolor=$IN_IMG_Color>画像タイトル</TD>
<TD Bgcolor=$IN_IMG_Color><Input Type="Text" Name="TITLE" Size=30 Maxlength=50">←気休めですが、自分専用にしたい時は後ろに(専用)と付けて下さい｡</TD>
</TR>
<TR>
<TD Bgcolor=$IN_IMG_Color>画像選択</TD>
<TD Bgcolor=$IN_IMG_Color><Input Type="FILE" Name="IMG" Size=50></TD>
</TR>
_____E_

if($FORM{'ADMIN'} ne 'MATOME'){
print <<"_____E_";
<TR>
<TD Bgcolor=$IN_TBL_Color>おなまえ</TD>
<TD Bgcolor=$IN_TBL_Color><Input Type="Text" Name="NAME" Size=25 Maxlength=50 Value="$COOKIE{'NAME'}">
</TD>
</TR>
<TR>
<TD Bgcolor=$IN_TBL_Color>Ｅ－ｍａｉｌ</TD>
<TD Bgcolor=$IN_TBL_Color><Input Type="Text" Name="EMAIL" Size=40 Maxlength=40 Value="$COOKIE{'EMAIL'}"></TD>
</TR>
<TR>
<TD Bgcolor=$IN_TBL_Color>ＨｏｍｅＰａｇｅ</TD>
<TD Bgcolor=$IN_TBL_Color><Input Type="Text" Name="HPURL" Size=60 Maxlength=60 Value="http://$COOKIE{'HPURL'}"></TD>
</TR>
<TR>
<TD Bgcolor=$IN_TBL_Color>コメント</TD>
<TD Bgcolor=$IN_TBL_Color><Input Type="Text" Name="MESSAGE" Size=80 Maxlength=100></TD>
</TR>
_____E_
} #-- end of if

print <<"_____E_";
<TR>
<TD Bgcolor=$IN_TBL_Color>登録キー</TD>
<TD Bgcolor=$IN_TBL_Color><Input Type="Password" Name="MYPWD" Size=10 Maxlength=10 Value="$COOKIE{'MYPWD'}">
<Input Type="Checkbox" Name="COOKIE" $CookieChecked>この情報を次回も利用する。
</TD>
</TR>
</Table>
<BR>
<Input Type="Submit" Value="--登録実行--">
<Input Type="Reset" Value="クリア">
</Form>
</Center>
_____E_
}

#;登録処理________________________________________________________________;
sub ExecSave
{
	if($FORM{'ADMIN'} eq 'MATOME'){
		if($FORM{'MYPWD'} ne $addminpass){
			&PrintErrHtml('パスワードが違います。');
		}else{
			$FORM{'NAME'} = $AdminName;
			$FORM{'MESSAGE'} = $AdminComment;
			$FORM{'EMAIL'} =$AdminMail;
		}
	}

	#;簡易セキュリティチェック
	&SeculityCheck;

	#;未入力チェック

	&PrintErrHtml("画像タイトルが未入力です。") unless($FORM{'TITLE'});

	if($FORM{'ADMIN'} ne 'MATOME'){
		&PrintErrHtml("おなまえが未入力です。") unless($FORM{'NAME'});
		&PrintErrHtml("メールアドレスが未入力です。") unless($FORM{'EMAIL'});
		&PrintErrHtml("不正なメールアドレスです。") if(!($FORM{'EMAIL'} =~ /[-A-Za-z0-9.]+@[-a-z0-9.]+/));
		&PrintErrHtml("コメントが未入力です。") unless($FORM{'MESSAGE'});
	}
	&PrintErrHtml("登録パスワードが未入力です。") unless($FORM{'MYPWD'});

	#;日時取得
	$ENV{'TZ'} = "JST-9";
	$GTime = time();
	($sec, $min, $hour, $day, $mon, $year, $wday) = localtime($GTime);
	$WeekName = ("(Sun)","(Mon)","(Tue)","(Wed)","(Tur)","(Fri)","(Sut)")[$wday];
	$year += 1900; $mon++;
	$mon  = "0$mon"  if($mon < 10);  $day  = "0$day"  if($day < 10);
	$hour = "0$hour" if($hour < 10); $min  = "0$min"  if($min < 10);
	$sec  = "0$sec"  if($sec < 10);
	$DateFileName = "$year$mon$day$hour$min$sec";
	$DateFormat = "$year/$mon/$day $WeekName $hour:$min";

	#;ロック開始
	&OpenFileLock;

	#;ログ読込
	open(IN,"$SaveFile") || &PrintErrHtml("保存ファイルの読み込みに失敗しました。<BR>原因:$!");
	@LINES = <IN>;
	close(IN);

	#;２重登録チェック
	foreach(@LINES){
		($pfn, $ptitle) = split(/\,/, $_);
		&PrintErrHtml("その画像名称はすでに登録されています。") if($ptitle eq $FORM{'TITLE'});
	}

	#;画像保存
	&SaveBinFile;

	#;最後の記事の番号を取得し１加算
	($pfn, $ptitle, $ptime, $ppwd, $pno) = split(/\,/, $LINES[0]);
	$No = $pno + 1;

	#;パスワード暗号化
	$EncodePass = &EnCodeKey($FORM{'MYPWD'});
	
	#;画像ファイルネーム簡素化  ### Add by Season
	$PicFile = $FILE_NAME{'IMG'};
	$PicFile =~ /([^\\\/]+$)/;
	$PicFile = $1;
	
	#;ＵＲＬフォーマット  ### Add by Season
	$HPURL  = $FORM{'HPURL'};
	$HPURL  =~ s/^http\:\/\///;
	$HPURL  =~ s/\r//g;
	$HPURL  =~ s/\n//g;

	#カンマ( , )入力対策(うぎゃ～ by Q)
	$FORM{'TITLE'}   =~ s/\,/、/g;
	$FORM{'NAME'}    =~ s/\,/、/g;
	$FORM{'EMAIL'}   =~ s/\,/、/g;
	$FORM{'MESSAGE'} =~ s/\,/、/g;
	$HPURL           =~ s/\,/、/g;
	#たぶん、入力フォームは以上だとおもう・・・けど(^^;;
	#にしても、なんで、データの区切りに、カンマをつかったんだろう？
	#魔がさしたとしかおもえない・・・

	#;データフォーマット化
	$NewLine = join("\,", $PicName, $FORM{'TITLE'}, $GTime, $EncodePass, $No, 
				$DateFormat, $FORM{'NAME'}, $FORM{'EMAIL'}, $FORM{'MESSAGE'},
				$Host, $PicWidth, $PicHeight, $PicType, $PicLen, $PicFile, 
				$HPURL, $FORM{'Only'}, 
				"\n"
			);

	#;日本コード変換&タグの除去
	&jcode'convert(*NewLine, $CharCode);
	$NewLine =~ s/</&lt;/g;
	$NewLine =~ s/>/&gt;/g;

	#;保存件数制御
	@LINES = ($NewLine, @LINES);
	if(($MaxSaveCount > 0) && ($MaxSaveCount < @LINES)){
		@DEL_ITEM = splice(@LINES, $MaxSaveCount);
		&DelIcon if($PicDeiMode);
	}

	#;ログ書込
	open(OUT,">$SaveFile") || &PrintErrHtml("保存ファイルの書き込みに失敗しました。<BR>原因:$!");
	print OUT @LINES;
	close(OUT);

	#;ロック解除
	&FileUnLock;

	#;クッキー発行
	&SetCookie;

	&PrintLogHtml;
}

#;画像保存処理____________________________________________________________;
sub SaveBinFile
{
	local($filename, $F);
	local($Len) = length($FILE_DATA{'IMG'});

	#;各種チェック
	if($Len <= 0){
		&PrintErrHtml("画像が選択されていません。");
	}

	#マックバイナリなら、マックバイナリを除去
	if($FILE_TYPE{'IMG'} eq 'application/x-macbinary'){
		$FILE_DATA{'IMG'} = &DelMacBin($FILE_DATA{'IMG'});
	}

	local($rtn, $w, $h) = &GetPicInf($FILE_DATA{'IMG'});

	if(($Len > $MaxPicSize * 1024) && ($MaxPicSize)){
		&PrintErrHtml("画像ファイルが、$MaxPicSize KByteを越えています。");
	}

	if(!$rtn){
		&PrintErrHtml("画像ファイル(GIF,JPEG)ではない可\能\性があります。<BR>御確認ください。");
	}

	if(($w > $MaxPicWidth) && ($MaxPicWidth)){
		&PrintErrHtml("画像ファイルの画面サイズが大きすぎます。<BR>横$MaxPicWidth × 縦$MaxPicHeight以下の画像しか受けつけておりません<BR>御確認ください。");
	}

	if(($h > $MaxPicHeight) && ($MaxPicHeight)){
		&PrintErrHtml("画像ファイルの画面サイズが大きすぎます。<BR>横$MaxPicWidth × 縦$MaxPicHeight以下の画像しか受けつけておりません<BR>御確認ください。");
	}

	#;保存処理
	$PicWidth = $w;
	$PicHeight = $h;
	$PicType = $rtn;
	$PicLen = $Len;

	$rtn =~ tr/A-Z/a-z/;

	$filename =  $DateFileName . "\.$rtn";

	$F = $IconPath . "\/" . $filename;
	if(-e $F){
		#;念のため同名ファイル名がないかチェック
		&PrintErrHtml("同名の画像ファイルが既に登録されています。");
	}

	open(OUT, "> $F") || &PrintErrHtml("画像登録に失敗しました。<BR>原因:$!");
	binmode(OUT);
	print OUT $FILE_DATA{'IMG'};
	close(OUT);

	$PicName = $filename;
}

#;ログ削除実行____________________________________________________________;
sub ExecDelete
{
	if(scalar(keys %DELETE_ID)==0){
		#削除
		#if($LocationMode){
		#	print "Location: $ThisCGI\n\n";
		#}else{
		#	&PrintLogHtml;
		#}
		&PrintLogHtml;
		return;
	}

	#;ロック開始
	&OpenFileLock;

	#;ログ読込
	open(IN,"$SaveFile") || &PrintErrHtml("保存ファイルの読み込みに失敗しました。<BR>原因:$!");
	@LINES = <IN>;
	close(IN);

	foreach $Rec(@LINES){
		($pfn, $ptitle, $ptime, $ppwd) = split(/\,/, $Rec);
		 unless($DELETE_ID{$ptime}){
		 	push(@NEW_LINES, $Rec);
		 	next;
		 }
		if($FORM{'DELKEY'} ne $addminpass){
			$match = &DeCodeKey($FORM{'DELKEY'}, $ppwd);
			if ($match ne 'yes') { 
				&PrintErrHtml("削除キーまたは管理者パスワードが違います。");
			}
		}
		$F = $IconPath . "\/" . $pfn;
		unlink($F) if($PicDeiMode && (-e $F));
	}

	#;ログ書込
	open(OUT,">$SaveFile") || &PrintErrHtml("保存ファイルの書き込みに失敗しました。<BR>原因:$!");
	print OUT @NEW_LINES;
	close(OUT);

	#;ロック解除
	&FileUnLock;

	&PrintLogHtml;
}

#;画像ファイル削除処理____________________________________________________;
sub DelIcon
{
	foreach(@DEL_ITEM){
		($pfn, $ptitle) = split(/\,/, $_);
		$F = $IconPath . "\/" . $pfn;
		unlink($F) if(-e $F);
	}
}

#;リモートホスト名取得____________________________________________________;
sub GetHost
{
	local($addr) = $ENV{'REMOTE_ADDR'};
	local($host) = $ENV{'REMOTE_HOST'};
	if(($host eq "") || ($host eq $addr)){

		#;お使いのサーバーが、gethostbyaddrの使用を禁止している場合、
		#;この行を削除してください。
		#;コメントにするだけでは、ダメなサーバーもあるようです。
		$host = gethostbyaddr(pack("C4", split(/\./, $addr)), 2);
		#;_______________________________________________________

		$host = $addr if($host eq "");
	}
	$Host  = $host;
}

#;簡易セキュリティチェック________________________________________________;
sub SeculityCheck
{
	&GetHost;
	
	if($SaveMode == 1){      #;1-パスワードによる制限
		return if($FORM{'WRITEPASS'} eq $UserPass);
		return if($FORM{'WRITEPASS'} eq $addminpass);
		&PrintErrHtml("登録用パスワードが違います。<BR>管理人にパスワードを教えてもらってください。");
	}elsif($SaveMode == 2){  #;2-リモートホストによる制限
		@HOSTS = split(/\n/, $NGRemortHost);
		foreach(@HOSTS){
			if($Host =~ /$_/i){
				&PrintErrHtml("登録できないリモートホストです。");
			}
		}
	}
	if($ProxyNG){
		if($Host =~ /proxy/i){
			&PrintErrHtml("プロキシサーバーからの登録はできません。");
		}
	}
}

#;フォーム情報デコード____________________________________________________;
sub FormDecord
{
	if($ENV{'CONTENT_TYPE'} =~ /multipart\/form-data; boundary=[^\0]*$/i){
		&InitFormMultiPart;
	}else{
		&InitFormNorm;
	}
}

#;削除用フォーム情報デコード______________________________________________;
#  改ページでも使用するので、GET対応
sub InitFormNorm
{
	if ($ENV{'REQUEST_METHOD'} eq "POST") {
		read(STDIN, $Que, $ENV{'CONTENT_LENGTH'});
	}else{
		$Que = $ENV{'QUERY_STRING'};
	}

	@Arr = split(/[&;]/, $Que);
	foreach(@Arr){
		($n, $v) = split(/=/, $_);
		$v =~ tr/+/ /;
		$v =~ s/%([A-Fa-f0-9][A-Fa-f0-9])/pack("C", hex($1))/eg;
		if($n eq "ID"){
			$DELETE_ID{$v} = 1;
		}else{
			$FORM{$n} = $v;
		}
	}
}

#;投稿用フォーム情報デコード______________________________________________;
sub InitFormMultiPart
{
	local($que, $remain, $tmp, $bound, @arr);
	$que = "\r\n";
	$remain = $ENV{'CONTENT_LENGTH'};
	binmode(STDIN);
	while($remain){
		$remain -= sysread(STDIN, $tmp, $remain);
		$que .= $tmp;
	}

	$ENV{'CONTENT_TYPE'} =~ /multipart\/form-data; boundary=([^\0]*)$/i;
	$bound = $1;

	@arr = split(/\r\n-*$bound-*\r\n/, $que);
	shift(@arr);
	foreach(@arr){
		$tmp = $_;
		if(/^Content-Disposition: ([^;]*); name="([^;]*)"; filename="([^;]*)"/i){
			$tmp =~ s/^Content-Disposition: ([^;]*); name="([^;]*)"; filename="([^;]*)"\r\nContent-Type: ([^;]*)\r\n\r\n//;
			$FILE_NAME{$2} = $3;
			$FILE_TYPE{$2} = $4;
			$FILE_DATA{$2} = $tmp;
		}elsif(/^Content-Disposition: ([^;]*); name="([^;]*)"/i){
			$tmp =~ s/^Content-Disposition: ([^;]*); name="([^;]*)"\r\n\r\n//;
			$FORM{$2} = $tmp;
		}
	}
	$que = undef; #一応クリア･･･
}
#;画像情報取得処理________________________________________________________;
sub GetPicInf
{
	local($rtn, $w, $h);
	local($buf) = $_[0];

	($rtn, $w, $h) = &GetGifSize($buf);
	if($rtn){
		return "GIF", $w, $h;
	}
	
	($rtn, $w, $h) = &GetJpegSize($buf);
	if($rtn){
		return "JPG", $w, $h;
	}

	($rtn, $w, $h) = &get_png_size($buf);
	if($rtn){
		return "PNG", $w, $h;
	}

	return 0, "", "";
}

#;GIF のサイズを取得______________________________________________________;
#    USAGE:($sts,$width,$height) = &GetGifSize(data);
#    引数)
#        data: GIFデータ
#    返値)
#        $sts   : true:GIF, false:GIFファイルではない。
#        $width : 横の長さ
#        $height: 縦の長さ
sub GetGifSize
{
	local($buf) = $_[0];
	if (substr($buf, 0, 3) eq "GIF"){
		local($GIFWidth) = ord(substr($buf,6,1)) + ord(substr($buf,7,1)) * 256;
		local($GIFHeight) = ord(substr($buf,8,1)) + ord(substr($buf,9,1)) * 256;
		return 1,$GIFWidth, $GIFHeight;
	}else{
		return 0,"","";
	}
}

#;JPEG のサイズを取得_____________________________________________________;
#    USAGE:($sts,$width,$height) = &GetJpegSize(data);
#    引数)
#        data: Jpegデータ
#    返値)
#        $sts   : true:Jpeg, false:Jpegファイルではない。
#        $width : 横の長さ
#        $height: 縦の長さ
sub GetJpegSize
{
	local($buffer) = $_[0];

	#SOI APP0検索
	local($FFD8Idx) = index($buffer, "\xFF\xD8\xFF\xE0");
	if($FFD8Idx == -1){
		return 0, "", "";
	}

	#JFIF識別文字列検索
	local($JFIFIdx) = index($buffer, "JFIF", $FFD8Idx + 4);
	if($JFIFIdx == -1){
		return 0, "", "";
	}

	#Get Jpeg Size
	local($SOFnIdx) = 2;
	local(%SOFn) = ("\xC0", 1, "\xC1", 1, "\xC2", 1, "\xC3", 1, "\xC5", 1, 
					"\xC6", 1, "\xC7", 1, "\xC8", 1, "\xC9", 1, "\xCA", 1, 
					"\xCB", 1, "\xCD", 1, "\xCE", 1, "\xCF", 1);

	#SOFn検索
	local($BufLen) = length($buffer);
	while($SOFnIdx < $BufLen){
		$c = substr($buffer, $SOFnIdx, 1); $SOFnIdx++;
		if($c eq "\xFF"){
			$c = substr($buffer, $SOFnIdx, 1); $SOFnIdx++;
			if($SOFn{$c}){
				@SIZE = unpack("CCCC", substr($buffer, $SOFnIdx + 3, 4));
				return 1, $SIZE[2] * 256 + $SIZE[3], $SIZE[0] * 256 + $SIZE[1];
	    	}elsif(($c eq "\xD9") || ($c eq "\xDA")){
				return 0, "", "";
			}else{
				$c = substr($buffer, $SOFnIdx, 2);
				@JMP = unpack("CC", $c);
				$SOFnIdx += $JMP[0] * 256 + $JMP[1];
			}
		}
	}
	return 0, "", "";
}
#;PNG のサイズを取得_____________________________________________________;
#    USAGE:($sts,$width,$height) = &get_png_size(data);
#    引数)
#        data: PNGデータ
#    返値)
#        $sts   : 1:PNG, 0:PNGファイルではない。
#        $width : 横の長さ
#        $height: 縦の長さ
sub get_png_size
{
	local($buffer) = $_[0];
	#著名(8byte) 89 50 4E 47 0D 0A 1A 0A 検索
	unless(substr($buffer, 0, 8) eq "\x89\x50\x4E\x47\x0D\x0A\x1A\x0A"){
		return 0, "", "";
	}

	#IHDR検索
	#  チャンク構造 
	#  1-4 チャンクの長さ
	#  5-9 チャンクタイプ
	local($pos, $chunk_len, $chunk_type, @w, @h, $width, $height);
	$chunk_len = 8;
	while($chunk_type ne "IHDR"){
		$pos = $chunk_len;
		$chunk_len = substr($buffer, $pos, 4);
		$pos += 4;
		$chunk_type = substr($buffer, $pos, 4);
	}
	if($chunk_type eq "IHDR"){
		@w = unpack("CCCC", substr($buffer, $pos + 4, 4));
		@h = unpack("CCCC", substr($buffer, $pos + 8, 4));
		$width = 0;
		$height = 0;
		$k = 3;
		foreach(0..3){
			$width += $w[$_] * (256 ** $k);
			$height += $h[$_] * (256 ** $k);
			$k--;
		}
		return 1, $width, $height;
	}else{
		return 0, "", "";
	}
}
#;マックバイナリの除去____________________________________________________;
sub DelMacBin
{
	local($bindata) = $_[0];
	local(@len, $size, $k);

	#マックバイナリヘッダから、データ長さを取得
	@len = unpack("CCCC", substr($bindata, 83, 4));
	$size = 0;
	$k = 3;
	foreach(0..3){
		$size += $len[$_] * (256 ** $k);
		$k--;
	}
	
	return substr($bindata, 128, $size);
}
#;日本語コード設定________________________________________________________;
sub GetJapanCode
{
	$Bit_1 = ord(substr("漢", 0, 1));
	if($Bit_1 == 0xb4){
		$CharSet = "x-euc-jp";
	}elsif($Bit_1 == 0x1b) {
		$CharSet = "iso-2022-jp";
	}else{
		$CharSet = "x-sjis";
	}
}

#;クッキー発行____________________________________________________________;
sub SetCookie
{
	return unless($FORM{'COOKIE'});

	local($ExpiresValue, $Cook);
	local($Sec, $Min, $Hour, $Day, $Month, $Year, $Week) = gmtime(time + $CookieDay * 24 * 60 * 60);

	$Year += 1900;

	$Sec  = "0$Sec"  if($Sec  < 10);
	$Min  = "0$$Min" if($Min  < 10);
	$Hour = "0$Hour" if($Hour < 10);
	$Day  = "0$Day"  if($Day  < 10);

	$Month = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')[$Month];
	$Week = ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')[$Week];

	$ExpiresValue = "$Week, $Day\-$Month\-$Year $Hour:$Min:$Sec GMT";

	push(@COOKS, "NAME\:$FORM{'NAME'}");
	push(@COOKS, "EMAIL\:$FORM{'EMAIL'}");
	push(@COOKS, "HPURL\:$HPURL");
	push(@COOKS, "MYPWD\:$FORM{'MYPWD'}");
	push(@COOKS, "WRITEPASS\:$FORM{'WRITEPASS'}") if($CookieUserPassSave);

	$Cook = join("\,", @COOKS);

	print "Set-Cookie: $CookieID=$Cook; expires=$ExpiresValue\n";
}

#;クッキー取得____________________________________________________________;
sub GetCookie
{
	@pairs = split(/;/,$ENV{'HTTP_COOKIE'});
	foreach $pair (@pairs) {
		local($name, $value) = split(/=/, $pair);
		$name =~ s/ //g;
		$DUMMY{$name} = $value;
	}
	@pairs = split(/,/,$DUMMY{$CookieID});
	$CookieChecked = "Checked" if(@pairs>0);
	foreach $pair (@pairs) {
		local($name, $value) = split(/:/, $pair);
		$COOKIE{$name} = $value;
	}
}

#;OpenFileロック__________________________________________________________;
sub OpenFileLock
{
	return unless($LockMode);
	local($Retry) = 5;
	foreach(1..$Retry){
		if(-e "$LockFile"){
			local($mtime) = (stat($LockFile))[9];
			if ($mtime < $GTime - 600){
				#;生成されてから、１０分以上経過されていたら削除
				unlink($LockFile);
			}else{
				sleep(1);
			}
		}else{
			open(LOCK, ">$LockFile") || &PrintErrHtml("ロックファイル生成失敗<BR>原因:$!");
			close(LOCK);
			$LOCK_SW = 1;
			return;
		}
	}
	&PrintErrHtml("現在、他の人が登録を行なっています。<BR>再度、登録を実行してください。");
}

#;ロック解除______________________________________________________________;
sub FileUnLock
{
	unlink($LockFile) if(-e "$LockFile");
	$LOCK_SW = 0;
}

#;暗号化__________________________________________________________________;
sub EnCodeKey
{
	local($inpw) = $_[0];
	local(@SALT, $salt, $encrypt);

	@SALT = ('a'..'z', 'A'..'Z', '0'..'9', '.', '/');
	srand;
	$salt = $SALT[int(rand(@SALT))] . $SALT[int(rand(@SALT))];
	$encrypt = crypt($inpw, $salt) || crypt ($inpw, '$1$' . $salt);
	return $encrypt;
}

#;暗号照号________________________________________________________________;
sub DeCodeKey
{
	local($inpw, $logpw) = @_;
	local($salt, $key, $check);

	$salt = $logpw =~ /^\$1\$(.*)\$/ && $1 || substr($logpw, 0, 2);
	$check = "no";
	if (crypt($inpw, $salt) eq "$logpw" || crypt($inpw, '$1$' . $salt) eq "$logpw")
		{ $check = "yes"; }
	return $check;
}
__END__
#;_____________________End_of_Script______________________________________;



