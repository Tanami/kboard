#!/usr/bin/perl

# Dream Editor v2.3 (2001/02/17)
# Copyright(C) Kent Web 2001
# webmaster@kent-web.com
# http://www.kent-web.com/

#============#
#  設定項目  #
#============#

# パスワード (英数字で指定)
$pass = '0123';

# スクリプト名
$script = './edit.cgi';

# method形式 (POST or GET)
$method = 'POST';

# ログを置くサーバディレクトリ
#   → 現行ディレクトリであればこのままでよい
#   → 最後は必ず / で閉じる
#   → フルパスなら / から始める（http://からではない）
$LogDir = './';

#============#
#  設定完了  #
#============#

&decode;
if ($in{'pass'} ne "$pass") { &enter; }
if ($mode eq "mente") { &mente; }
elsif ($mode eq "make") { &make; }
elsif ($mode eq "del") { &id_del; }
&admin;


#------------#
#  管理画面  #
#------------#
sub admin {
	&header;
	print <<"EOM";
<table width="100%"><tr><th bgcolor="#0000A0">
<font color="#FFFFFF">管理画面</font>
</th></tr></table>
<blockquote>
<P>
<OL>
<B><LI>カウンタ値の変更メンテナンス</B>
<P>
  <DL>
  <DT>ID名を入力し、送信キーを押して下さい。
  </DL>
<P>
<form action="$script" method="$method">
<input type=hidden name=mode value="mente">
<input type=hidden name=pass value="$in{'pass'}">
ID名 <input type=text name=id size=12>
<input type=submit value="送信する">
</form>
<hr>
<P>
<B><LI>ログファイルの削除</B>
<P>
  <DL>
  <DT>ID名を入力し、削除キーを押して下さい。
  </DL>
<P>
<form action="$script" method="$method">
<input type=hidden name=mode value="del">
<input type=hidden name=pass value="$in{'pass'}">
ID名 <input type=text name=id size=12>
<input type=submit value="削除する">
</form>
<hr>
<P>
<B><LI>ログファイルの生成</B>
<P>
  <DL>
  <DT>ID名を入力し、生成キーを押して下さい。
  </DL>
<P>
<form action="$script" method="$method">
<input type=hidden name=mode value="make">
<input type=hidden name=pass value="$in{'pass'}">
作成ID名 <input type=text name=id size=12> (必ず半角英数字で)<br>
開始カウント数 <input type=text name=count size=12 value="0">
<P>
<input type=submit value="生成する">
</form>
</OL>
</blockquote>
</body></html>
EOM
	exit;
}

#------------------#
#  パスワード画面  #
#------------------#
sub enter {
	&header;
	print <<"EOM";
<center>
<h4>- パスワードを入力してください -</h4>
<form action="$script" method="$method">
<input type=password name=pass size=8><input type=submit value=" 認証 ">
</form></center>
</body></html>
EOM
	exit;
}

#------------------#
#  メンテ処理画面  #
#------------------#
sub mente {
	# ログファイルを定義
	$logfile = "$LogDir$id\.dat";
	if ($id =~ /\W/) { &error("ID名は半角の英数字で指定して下さい"); }

	# ログの存在をチェック
	unless (-e $logfile) {
		&error("指定のIDログファイル <B>$id</B> が見つかりません");
	}

	# ログを読み込み
	open(IN,"$logfile") || &error("Can't open $logfile");
	$line = <IN>;
	close(IN);

	# ログを分解
	($count,$ip) = split(/:/,$line);

	# メンテ実行
	if ($flag) {
		$line = "$in{'count'}\:$ip";

		# ログを更新
		open(OUT,">$logfile") || &error("Can't write $logfile");
		print OUT $line;
		close(OUT);

		# 完了通知
		&header;
		print "<center><h3>メンテ処理は正常に完了しました</h3>\n";
		print "<hr width='400'>\n";
		print "<table><tr><td>ID名：<b>$id</b>\n";
		print "<P>カウント数：<b>$in{'count'}</b></td></tr></table>\n";
		print "<hr width='400'>\n";
		print "<form action=\"$script\" method=$method>\n";
		print "<input type=hidden name=mode value=admin>\n";
		print "<input type=hidden name=pass value=\"$in{'pass'}\">\n";
		print "<input type=submit value=\"管理画面にもどる\"></form>\n";
		print "</center>\n";
		print "</body></html>\n";
	}

	# ログを表示
	else {
		&header;
		print <<"EOM";
<center>
■<b>$id</b>のカウントを修正します。
<P>
<form action="$script" method="$method">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=mode value="mente">
<input type=hidden name=id value="$id">
<input type=hidden name=flag value="1">
カウント数 <input type=text name=count size=12 value="$count">
<input type=submit value="修正する">
</form>
</center>
</body></html>
EOM
	}
	exit;
}

#------------------#
#  IDファイル削除  #
#------------------#
sub id_del {
	# ログファイルを定義
	$logfile = "$LogDir$id\.dat";
	if ($id =~ /\W/) { &error("ID名は半角の英数字で指定して下さい"); }

	# ログの存在をチェック
	unless (-e $logfile) {
		&error("指定のIDログファイル <B>$id</B> が見つかりません");
	}

	# 削除実行
	if ($flag) {
		unlink($logfile);

		# 完了通知
		&header;
		print <<"EOM";
<center>
<hr width='400'>
IDファイル <B>$id</B> は削除されました
<hr width='400'>
<form action="$script" method=$method>
<input type=hidden name=mode value=admin>
<input type=hidden name=pass value="$in{'pass'}">
<input type=submit value=管理画面にもどる></form>
</center>
</body></html>
EOM
	}

	# 再確認画面
	else {
		&header;
		print <<"EOM";
<center><hr width="400">
IDファイル <font color=#DD0000><B>$id</B></font> を本当に削除しますか？
<hr width="400">
<P><form action="$script" method="$method">
<input type=hidden name=id value="$id">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=mode value="del">
<input type=hidden name=flag value="1">
<input type=submit value="削除する"></form>
</center>
</body></html>
EOM
	}
	exit;
}

#----------------------#
#  IDファイル生成処理  #
#----------------------#
sub make {
	if ($id =~ /\W/) { &error("ID名は半角の英数字で指定して下さい"); }

	# ログファイルを定義
	$logfile = "$LogDir$id\.dat";

	# ログの存在をチェック
	if (-e $logfile) {
		&error("指定のID <B>$id</B> は既に使用されています。<br>
			別のID名を指定して下さい");
	}

	# ログをフォーマット
	$new_file = $in{'count'};

	# ログを作成
	open(OUT,">$logfile") || &error("Can't write $logfile");
	print OUT $new_file;
	close(OUT);

	# パーミッションを 666 へ
	chmod (0666,$logfile);

	# 完了通知
	&header;
	print "<center><h3>ID作成処理は正常に完了しました</h3>\n";
	print "<hr width='60%'>\n";
	print "<table><tr><td>作成ID名：<b>$id</b><P>\n";
	print "カウント数：<b>$in{'count'}</b></td></tr></table>\n";
	print "<hr width='60%'>\n";
	print "<form action=\"$script\" method=$method>\n";
	print "<input type=hidden name=mode value=admin>\n";
	print "<input type=hidden name=pass value=\"$in{'pass'}\">\n";
	print "<input type=submit value=\"管理画面にもどる\"></form>\n";
	print "</center>\n";
	print "</body></html>\n";
	exit;
}

#----------------#
#  デコード処理  #
#----------------#
sub decode {
	if ($ENV{'REQUEST_METHOD'} eq "POST") {
		read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
	} else { $buffer = $ENV{'QUERY_STRING'}; }

	@pairs = split(/&/,$buffer);
	foreach $pair (@pairs) {
		($name, $value) = split(/=/, $pair);
		$value =~ tr/+/ /;
		$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

		$in{$name} = $value;
	}
	$id   = $in{'id'};
	$mode = $in{'mode'};
	$flag = $in{'flag'};

	# 日時の取得
	$ENV{'TZ'} = "JST-9";
	($sec,$min,$hour,$mday,$mon,$year,$dmy,$dmy) = localtime(time);
}

#----------------#
#  HTMLヘッダー  #
#----------------#
sub header {
	print "Content-type: text/html\n\n";
	print <<"EOM";
<html>
<head>
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=Shift_JIS">
<title>DREAM EDITOR</title></head>
<body bgcolor="#FFFFFF" text="#000000">
EOM
}

#--------------#
#  エラー処理  #
#--------------#
sub error {
	&header;
	print "<center><h3>ERROR !</h3>\n";
	print "<font color='#DD0000'>$_[0]</font>\n";
	print "</center>\n";
	print "</body></html>\n";
	exit;
}
