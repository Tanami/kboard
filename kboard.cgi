#!/usr/bin/env perl
##↑Perlへのパス

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃マスターキーの設定                                      ┃
#┃半角英数で8文字以下で指定してください。                 ┃
#┃"コロンに挟まれた[0123]を変更します。                   ┃
#┃["][;]を消さないように注意してください。                ┃

$masterkey  = "0123";

#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃外部ファイルの呼び出し                                  ┃
#┃jcode.plが複数ある場合は、まとめましょう                ┃

   require './jcode.pl';
   require './kboard.ini';
                                                             
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃以下変更すべきところは特にありません。                  ┃
#┃Perlに自信がある人だけ、改造など変更してください。      ┃
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃KBOARD v12.30 (03/10/04)                                ┃
#┃(C) 2000-2003 KAISM                                     ┃
#┃E-MAIL: kai@kaism.com                                   ┃
#┃   WWW: http://www.kaism.com                            ┃
$ver = 'kboard v12.30';                  # バージョン情報  ┃
#┃---[注意事項]-------------------------------------------┃
#┃このスクリプトはフリーソフトです。このスクリプトを使用  ┃
#┃したいかなる損害に対して作者は一切の責任を負いません。  ┃
#┃改造・再配布に関する制限はありませんが、著作権を放棄し  ┃
#┃たわけではありません。                                  ┃
#┃--------------------------------------------------------┃
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃処理手順                                                ┃
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫

&decode;
&access_deny;

if ($mode eq "res_pass"){&res_pass;}
if ($mode eq "town"){&ktown_win;}
if ($mode eq "write"){&write;}
if ($mode eq "frame"){&frame;}
if ($mode eq "menu"){&menu;}

if ($mode eq "clear" && &make_mpass($pass) ne "$masterkey"){&clear;}
if ($mode eq "clear" && &make_mpass($pass) eq "$masterkey"){&admin_res_form;}
if ($mode eq "admin_clear"){&clear;}
if ($mode eq "admin_res_write"){&admin_res_write;}

if ($mode eq "admin_in"){&admin_in;}
if ($mode eq "admin_pass" && &make_mpass($pass) eq "$masterkey"){&admin_form;}
if ($mode eq "admin_pass" && &make_mpass($pass) ne "$masterkey"){&admin_in("キーが違います");}
if ($mode eq "admin_write"){&admin_write;}

if ($mode eq "res_html"){&res_html;}
if ($mode eq "res_write"){&res_write;}
if ($mode eq "res_clear_form"){&res_clear_form;}
if ($mode eq "res_clear"){&res_clear;}

if ($mode eq "make_mpass"){&make_mpass_mode;}

&html;

#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃サブルーチン全リスト                                    ┃
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
#┃sub html                 メイン表示処理                 ┃
#┃sub write                ログ書き込み処理               ┃
#┃sub clear                ログ削除処理                   ┃
#┃sub decode               デコード処理                   ┃
#┃sub make_pass            削除キー暗号化処理             ┃
#┃sub match_pass           削除キー暗号符合処理           ┃
#┃sub uemess               注意メッセージ表示処理         ┃
#┃sub error                エラーメッセージ表示処理       ┃
#┃sub auto_link            自動リンク処理                 ┃
#┃sub get_time             時間取得処理                   ┃
#┃sub get_host             ホスト・IPアドレス取得処理     ┃
#┃sub lock                 ロック処理                     ┃
#┃sub unlock               ロック解除処理                 ┃
#┃sub set_cookie           クッキー生成処理               ┃
#┃sub get_cookie           クッキー取得処理               ┃
#┃sub mail_to              メール送信処理                 ┃
#┃sub new_time             新着表示処理                   ┃
#┃sub how_to               使い方表示処理                 ┃
#┃sub page                 ページリンク表示処理           ┃
#┃sub ktown                town表示処理                   ┃
#┃sub ktown_win            town別窓表示処理               ┃
#┃sub ktown_time           town日時フォーマット処理       ┃
#┃sub ktown_up             townカウント更新処理           ┃
#┃sub fudousan             売却メッセージ表示処理         ┃
#┃sub pastwrite            過去ログファイル更新処理       ┃
#┃sub new_pfile            過去ログファイル作成処理       ┃
#┃sub frame                過去ログフレーム生成処理       ┃
#┃sub menu                 過去ログメニュー生成処理       ┃
#┃sub admin_in             管理用認証フォーム出力処理     ┃
#┃sub admin_form           townデータ修正フォーム出力処理 ┃
#┃sub admin_write          townデータ修正処理             ┃
#┃sub admin_res_form       管理者レス入力フォーム         ┃
#┃sub admin_res_write      管理者レス書きこみ処理         ┃
#┃sub res_html             私書箱表示処理                 ┃
#┃sub res_write            私書箱データの書きこみ処理     ┃
#┃sub res_clear_form       私書箱データ削除フォーム表示   ┃
#┃sub res_clear            私書箱データ削除処理           ┃
#┃sub res_pass             置き手紙パスワード照合処理     ┃
#┃sub access_deny          アクセス拒否処理               ┃
#┃sub head_html            ヘッダー表示処理               ┃
#┃sub house_page_count     家表示ページ処理               ┃
#┃sub mail_flag            置手紙未読チェック             ┃
#┃sub url_encode           urlエンコード処理              ┃
#┃sub ie_size              家サイズ決定処理               ┃
#┃sub make_mpass           マスターキー照合処理           ┃
#┃sub make_mpass_mode      マスターキー暗号化処理         ┃
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛


#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃メイン表示処理                                          ┃
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
sub html{  

##クッキーの情報を取得する処理に 
	
	#$cookie{'cname'}   名前             
	#$cookie{'cemail'}  メールアドレス   
	#$cookie{'curl'}    HPアドレス       
	#$cookie{'cpass'}   削除キー         
	&get_cookie;

##投稿記事を取得する処理
	
	#ログファイルを開きます
	open (IN,"$logfile") || &error("投稿記事ファイル$logfileが読みこめませんでした");
	
	#各行（記事）を配列に代入
	@lines = <IN>;
	
	#ファイルを閉じる
	close(IN);

	#ヘッダー表示処理へ
	#ページタイトルをもっていく
	&head_html("$title");

	#ヒアドキュメント
	print <<"EOM";
<center>
<table border=0>
<tr>
<!---left-cell---->
<td width=400 nowrap valign=top bgcolor="$mess_color">

<!---form-table-->
	<table width=400 border=0>
		<form name=MainForm onSubmit="return hissu_check()" action="$script" method="$method">
		<input type=hidden name=mode value="write">
		<tr><td align=center class="title"><b>$title</b></td></tr>
		<tr><td><hr size=1></td></tr>
		<tr><td nowrap align=right><b>name:</b><input type=text name=name size=30 value="$cookie{'cname'}"></td></tr>
		<tr><td nowrap align=right><b>email:</b><input  type=text name=email size=30 value="$cookie{'cemail'}"></td></tr>
		<tr><td nowrap align=right><b>url:</b><input  type=text name=url size=30 value="http://$cookie{'curl'}"></td></tr>
		<tr><td nowrap align=right><b>title:</b><input type=text name=sub size=30></td></tr>
		<tr><td align=right><textarea cols=50 rows=5 name=comment wrap="$wrap"></textarea></td></tr>
		<tr><td align=right valign=bottom><b>key:</b><input type=password name=pass size=8 maxlength=8 value="$cookie{'cpass'}"><input type=image src="$submit_gif" width=$submit_w height=$submit_h border=0 on></td></tr>
<script language="JavaScript">
<!--
function hissu_check(){
	NameCheck  = document.MainForm.name.value
	TitleCheck = document.MainForm.sub.value
	EmailCheck = document.MainForm.email.value
	KeyCheck   = document.MainForm.pass.value
EOM
	if($name_check){
		print "if(NameCheck == \"\"){alert(\"$mess_name\");return false}\n";
	}
	if($email_check){
		print "if(EmailCheck == \"\"){alert(\"$mess_email\");return false}\n";
	}
	if($sub_check){
		print "if(TitleCheck == \"\"){alert(\"$mess_sub\");return false}\n";
	}
	if($pass_check){
		print "if(KeyCheck == \"\"){alert(\"$mess_key_nashi\");return false}\n";
	}
	print <<"EOM";
	return true
}
//-->
</script>
EOM
	if($name_pass_check){
		print "<tr><td align=center><font color=\"$npc_color\">$npc_mess</font></td></tr>\n";
	}
	print <<"EOM";
		<tr><td align=center><font color="$uemess_color">$uemess</font></td></tr>
		</form>
	</table>
<!--form-table-end---->

<hr size=1>
EOM

##ページ処理
	
	#表示する記事の行番号を取得してくる
	&page;

##記事データの分析＆フォーマット処理

	#各記事データを解析する。以下、データに対する
	#処理の繰り返し。
	# $page_start 表示する記事の最初の行数(-1)
	# $page_end   表示する記事の最後の行数(-1)
	foreach ($page_start .. $page_end){

		#$num		記事番号
		#$name		名前
		#$email		メールアドレス
		#$url		HPアドレス
		#$sub		タイトル
		#$comment	記事
		#$date		日付
		#$second	日付（秒）
		#$host		ホスト
		#$pass		削除キー（暗号化）
		($num,$name,$email,$url,$sub,$comment,$res,$date,$second,$host,$pass) = split (/<>/,$lines[$_]);
		
		#メールアドレスがあれば、リンクをはる。
		if ($email ne ""){
			
			#メール画像があれば、それにリンクをはる。
			if ($emailgif){
				$email = "<a href=mailto:$email><img src=\"$emailgif\" border=0 width=$emailgif_w height=$emailgif_h></a> ";
			
			#なければ、名前にリンクをはる。
			}else{
			
				$name = "<a href=mailto:$email>$name</a>";
			}
		}
		
		#HPアドレスがあれば、リンクをはる
		if ($url ne ""){
		
			#家アイコンがあれば、それにリンクをはる。
			if ($urlgif){
				$url = "<a href=\"http://$url\" target=\"$target\"><img src=\"$urlgif\" border=0 width=$url_w height=$url_h></a>";

			#家アイコンがなければ、[url]の文字にリンクをはる。
			}else{
				$url = "[<a href=\"http://$url\" target=\"$target\">url</a>]";
			}
		}
		
		#新着強調表示をするかを判断し、新着かどうか評価
		if ($new_time_check){&new_time;}

		#ヒアドキュメント（記事表示）
		print <<"EOM";
<!---[$num]-message-table--->
	<table border=0>
		<form action="$script" method="$method">
		<input type=hidden name=mode value=clear>
		<input type=hidden name=num value="$num">
		<tr><td width=400>
		<p align=left>
		<b>[$num]$sub</b><br>
		$date
		</p>
		<ul>
		$comment
		</ul>
		</td>
		</tr>
		<tr>
		<td align=right>$name</td>
		</tr>
		<tr>
		<td align=right>$email $url<input type=image src="$gomi_gif" width=$gomi_w height=$gomi_h border=0><input type=password name=pass size=8 maxlength=8></td>
		</tr>
		</form>
EOM

		#管理者のレスの表示
		if ($res){
			print <<"EOM";
		<tr>
			<td>
			<ul><ul>
			<br>
			<font color="$master_color">$res</font>
			</ul></ul>
			<p align=right>$master_name</p>
			</td>
		</tr>
EOM
		}
		
		print <<"EOM";
	</table>
<!---[$num]-messgae-table-end--->

<hr size=1>

EOM
	}
	
	
##使い方表示を取得

	#使い方を表示するなら、
	if ($mode eq "howtogo"){
		
		#表示処理へ
		&how_to;
		
	#表示しないなら
	}else{
	
		#リンクを表示
		$howto = "<center><a href=\"$script?mode=howtogo\">使い方をみる</a></center>";
	}

##html表示処理
	
	#ヒアドキュメント
	print <<"EOM";

<!---page/copyright-table--->
	<table width=100% border=0><tr><td align=left nowrap>$page_back</td><td align=left nowrap>$page_next</td><td align=right>$ver <a href="http://www.kaism.com" target="_blank">kaism</a></td></tr></table>
<!---page/copyright-table-end--->

</td>
<!--left-cell-end--->

<!--right-cell--->
<td align=center nowrap valign=top width=250>

<!--info-table--->
	<table cellspacing=0 cellpadding=3 border=0 bgcolor="$info_bgcolor">
		<tr><td><br></td></tr>
		<tr><td nowrap width=200 align=center>$message</td></tr>
		<tr><td nowrap width=200 align=left><hr size=1 width=100%>$howto<hr size=1 width=100%></td></tr>
		<tr><td nowrap width=200 align=center><a href="$home" target="$h_target">もどる</a> | <a href="$script?mode=admin_in">管理用 </a>

EOM

##過去ログリンクに関して

	#過去ログを使うかどうか
	if($past_check){
	
		#$pcnt_fileの一行目にある、過去ログファイルNOを取り出す。
		open (IN ,"$pcnt_file") || &error("$pcnt_fileが開けませんでした") ;
		$pcnt = <IN>;
		close (IN);
	
		#行末の改行文字を切り落とす
		$pcnt =~ s/\n//g;
	
		#過去ログファイルNOが0でないなら、過去ログファイルへのリンクを表示
		unless($pcnt == 0){
			print "| <a href=\"$script?mode=frame\">過去ログ</a>\n";
		}
	}
	
	#ヒアドキュメント
	print <<"EOM";
		</td></tr>
		<tr><td><br></td></tr>
	</table>
<!--info-table-end--->

<br>

<!--town-table--->
EOM


	#town表示処理選択
	#一緒に表示するなら、表示処理に。
	if($ktown){&ktown;}
	
	#別窓表示ならtown画像にリンクをはる
	else{
		print <<"EOM";
<table>
<tr>
	<td align=center width=200 nowrap align=center><b>$town_title</b><br><a href="$script?mode=town" target=_blank><img src="$iedir/town.gif" border=0></a></td>
</tr>
</table>
EOM
	}

	#ヒアドキュメント
	print <<"EOM";
<!---town-table-end--->

</td>
<!---right-cell-end--->

</tr>
</table>

</center>

</body>
</html>
EOM

	#処理を終了。
	exit;

}                                                          
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
 
#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃ログファイルに書きこみする処理                          ┃
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
sub write{                                                 



##必須項目制限の処理

	#投稿記事に名前$nameが記入されてなかった時の処理
	#名前が必須項目なら
	if ($name_check){
	
		#名前が必須なら、その旨のメッセージを表示して、処理を中断
		if ($name eq ""){
			&uemess("$mess_name");
		}
	
	#必須でないなら
	}else{
		if($name eq ""){
		
			#名前に$tokumeiで指定した名前を入れる
			$name = "$tokumei";
		}
	}
	
	#メールアドレスが記入されなかったときの処理
	#メールアドレスが必須項目なら
	if ($email_check){
		if ($email eq ""){
		
			#その旨のメッセージを表示して、処理を中断
			&uemess("$mess_email");
		}
	}

	#投稿記事に題名$subが記入されてなかった時の処理
	#題名が必須項目なら
	if ($sub_check){
		if ($sub eq ""){
		
			#その旨のメッセージを表示して、処理を中断
			&uemess("$mess_sub");
		}
		
	#必須項目でなければ、
	}else{
		if ($sub eq ""){
		
			#タイトルに$mudaiで指定したものを入れる
			$sub ="$mudai";
		}
	}

	#投稿記事に削除キーが記入されてなかった時の処理
	#キーが必須項目なら
	if ($pass_check){
		if ($pass eq ""){
			
			#その旨のメッセージを表示して、処理を中断
			&uemess("$mess_key_nashi");
		}
	}
	
	#投稿者名チェック機能を利用する場合
	if ($name_pass_check){
		open(IN,"$rankfile") || &error("$rankfileが開けませんでした。");
		@npc_datas = <IN>;
		close(IN);
		
		$npc_flag = "ok";
		
		foreach(@npc_datas){
			($npc_name,$xx,$xx,$xx,$xx,$npc_pass,$xx) = split(/<>/,$_);
			if($name eq "$npc_name"){
				$npc_flag = &match_pass("$pass","$npc_pass");
				last;
			}
		}
		
		unless ($npc_flag eq "ok"){
			&uemess("その名前はすでに使われているか、キーが違います。<br>キーを忘れてしまったら、残念ながら他の名前を使ってください。");
		}
	}
	
##二重処理回避処理

	#二重処理を回避するために、ロック処理をする。
	if($lock_check){&lock;}
	
##ログファイルデータを取得する処理

	#ログファイルを開く
	open (IN,"$logfile") || &error("投稿記事保存ファイル$logfileが開けませんでした。");

	#各行を配列に代入
	@lines = <IN>;
	
	#ファイルを閉じる
	close(IN);

	#以下、sub decodeから受け取った変数の値を使う

##二重投稿回避処理

	#二重投稿があったかどうかの印の指定
	$niju_flag = 0;
	
	#ログにある全記事の一つ一つに対して
	foreach (@lines) {
	
		#各要素に分割して、配列に代入
		@datas_niju = split(/<>/,$_);
		
		#もしも、投稿者と、内容が一致するものが今までのログにあったら、
		if ($name eq "$datas_niju[1]" && $comment eq "$datas_niju[5]"){
		
			#二重投稿の印に１を代入
			$niju_flag = 1;
			
			#その記事のNo.を取得
			$niju_no = $datas_niju[0];
			
			#ループから抜け出す。
			last;
		}
	}
	
	#もしも、二重投稿の印に１が入っていたら（０でなければ）
	if ($niju_flag){
		
		#sub uemessに$mess_onajiというメッセージを持っていって、
		#二重投稿の旨をつげ、投稿を拒否する。
		&uemess("$mess_onaji","[$niju_no]");
	}

##白紙コメント回避
	#コメントが書かれていなかったときは、
	#白紙投稿を禁止する旨のメッセージをもって、sub uemessへいって、
	#ログに書きこみする処理をやめる。
	if ($comment eq ""){&uemess("$mess_nashi");}

##連続投稿に関して

	#直前の投稿データだけを取り出す。
	@bline = split(/<>/,$lines[0]);
	
	#制限をかけるなら
	if ($renzoku_check){
		
		#直前の名前と同じかチェック
		if ($name eq "$bline[1]"){
			
			#直前の投稿からの経過時間（秒）
			$keika_time = time - $bline[8];
			
			#連続投稿を許す時間を指定（秒）
			$renzoku_ok = 60 * $renzoku_time;
			
			#連続投稿を許可するまでの残り時間を指定（秒）
			$nokori_time = $renzoku_ok - $keika_time;
			
			#連続投稿を許可するか
			#早過ぎるなら
			unless ($nokori_time < 0 ){
			
				#あと何秒後で書きこめるかのメッセージを表示
				&uemess("$nokori_time$renzoku_mess");
			}
		}
	}
	

##投稿記事に関する情報を取得する。

	#$date に日付を代入
	&get_time;

	#$hostにホスト情報を代入
	&get_host;

	#passがあれば、それを暗号化するため、
	#sub make_passへいって、返ってきた値を$PWに代入する。
	if ($pass){ $PW = &make_pass($pass);}

	#直前のデータの記事番号にプラス１して、今回の記事番号にする。
	$num = $bline[0]+1;


##新着記事をログファイルに保存する処理

	#新投稿記事を保存形式に整理して、$newの値とする。
	$new = "$num<>$name<>$email<>$url<>$sub<>$comment<>$res<>$date<>$second<>$host<>$PW\n";

	#新投稿記事をログ配列の先頭に追加
	unshift (@lines,$new);

##保存記事数の処理
	#総記事数を取得
	$kiji = @lines;

	#最大記事保存数・総記事数を０から始まる行数にするため、マイナス１する
	$dmax = $max -1;
	$dkiji= $kiji -1;

	#logfileに書き出す記事を入れる配列を指定
	@news  =();

	#保存する行数分だけ、配列@newsに代入
	foreach (0 .. $dmax){
		push(@news,$lines[$_]);
	}

	#最大記事保存数を超えたときに、過去ログとして保存するかどうか
	if ($past_check){
	
		#最後の行数が、最大保存する行数よりも大きければ、
		if ($dkiji > $dmax){

			#過去ログに書きこむデータを入れる配列を指定
			@pasts =();
			
			#溢れた記事の行数分だけ、配列@pastsに代入
			foreach ($max .. $dkiji){
				push(@pasts,$lines[$_]);
			}
			
			#過去ログに書き込みをする処理へ
			&pastwrite;

		}
	}
	
	
	#表示される記事をあらためて、$logfileに書きこむ。
	open (OUT,">$logfile") || &error("$logfileがひらけませんでした。");
	print OUT @news;
	close(OUT);


	
##townデータを更新する処理

	#カウントを増やすので、upという値を持っていく。（削除の場合と区別するため）
	&ktown_up("up");

##クッキーの処理

	#書きこみされた内容をクッキーとして焼く
	&set_cookie;

##メール通知処理

	#書きこまれた内容を管理者にメール通知するかどうかチェックして、
	#もし通知するのなら、その処理を行なう
	if ($mail_send) {&mail_to;}

##次の処理を許可する

	#ログの更新処理が終了したので、ロックを解除する
	if($lock_check){&unlock;}

}
                                                           
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛


#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃記事を削除する処理                                      ┃
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
sub clear{

##二重処理を回避

	#ログを更新するため、ロック処理する。
	if($lock_check){&lock;}

##記事情報を取得する処理

	#ログファイルを開く
	open (IN,"$logfile") || &error("$logfileが開けませんでした。");
	
	#各行を配列に代入
	@lines = <IN>;
	
	#ログファイルを閉じる
	close(IN);

##削除する記事を見つける処理
##sub decodeからきた変数を使う
##$num	削除する記事番号
##$pass	削除キー

	#削除しない記事を代入する配列の指定
	@news=();
	
	#記事情報を、ひとつづつ処理する。
	foreach $line (@lines){

		#xxの部分はいらないので、ダミーの変数。
		#最後のc はclearのc
		#$namec,$urlcは&ktown_upで使用する。
		($numc,$namec,$xx,$urlc,$xx,$xx,$xx,$xx,$xx,$xx,$psc) = split(/<>/,$line);

		#$pscは行の最後にあるので、改行を削除する。
		$psc =~ s/\n//g;

		#sub decodeから送られてきた、削除する記事番号$numをもとに
		#削除する記事かどうかを判断。
		if ($numc == $num){
		
			#設定されていた削除キーを$PWに代入
			#削除する記事の投稿者名を取得（変数を変えるのは、&ktown_upでの処理のため)
			#削除する記事がみつかったか、どうか$delで判断する
			$PW = $psc;
			$name = $namec;
			$del = 1;

		#削除する記事でなければ、配列@newsに入れる
		}else{
			push(@news,$line);
		}
	}

##削除するかどうかの処理

	#入力された削除キーがマスターキーじゃなかったら
	unless ( $pass eq "$masterkey"){

		#その記事が投稿されたときに、削除キーが設定されていなければ、
		#sub uemessにその旨のメッセージをもっていき、削除を中止。
		if ($PW eq ""){&uemess("$mess_key_ng1");}

		#sub decodeから送られてきた、削除キー$passと、記事に設定されていた削除キー$PWが一致するかどうかを
		#sub match_passで処理して、その結果を$resultに代入する。
		$result = &match_pass("$pass","$PW");

		#sub match_passから受け取った結果$resultが、okでなければ、
		#sub uemessにその旨のメッセージを持っていき、削除を中止
		unless ($result eq 'ok'){ &uemess("$mess_key_ng2");}
	}

##ログファイルの更新処理

	#削除する記事があって、($del = 1なら)
	#以上の削除キーに対する評価を乗り越えて、削除が認められたら、
	if($del){
	
		#ログファイルを開く
		open (OUT,">$logfile") || &error("$logfileがひらけませんでした。");
	
		#あたらしいデータに更新
		print OUT @news;
	
		#ログファイルを閉じる
		close (OUT);
	
		#townデータファイルの更新処理
		#カウントを減らすので、downという値をもっていく（書き込みと区別するため）
		&ktown_up("down");
	}
	
	#以上、ログの更新作業が終了したので、ロックを解除する。
	if($lock_check){&unlock;}
	
	#パスワードを初期化
	$FORM{'pass'} = "";
	
}                                                          

#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃デコード処理                                            ┃
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
sub decode {                                               

##送られたデータを読み取る処理

	#情報の送信方法Post or Getで処理を区別
	#postで送信されていれば、
	if ($ENV{'REQUEST_METHOD'} eq "POST") {

		#そのデータを$bufferに代入
		read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
	
	#getなら
	#そのデータを$bufferに代入
	} else { $buffer = $ENV{'QUERY_STRING'}; }

##受け取ったデータを分析する処理

	#受け取った情報$bufferを＆で分割する。
	@pairs = split(/&/, $buffer);

	#@pairsを１つづつ処理する
	foreach $pair (@pairs) {

		#$pairを連想配列のキー$nameと、値$valueに分割
		($name,$value) = split(/=/, $pair);

		#$valueのなかの+を半角スペースに。
		$value =~ tr/+/ /;
		
		#受け取った$valueの中身は、%と16進数で表記されているので、
		#それを処理する。
		$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
		
		#最初に指定した、jcode.plを用いて、文字コードを変換Shift-JISコードに変換処理する。

		&jcode'convert(*value,'sjis');



		
		#タグを許可するなら
		if ($tag_check) {

			#タグを許可
			#コメント・危険なSSIの書きこみを排除する
			$value =~ s/<!--(.|\n)*-->//g;
			
			#記事ログの各要素を分けている<>は変換する。
			$value =~ s/<>/&lt;&gt;/g;

		#タグを許可しなければ
		}else{

			#<,>,"をそれぞれ変換する
			$value =~ s/</&lt;/g;
			$value =~ s/>/&gt;/g;
			$value =~ s/\"/&quot;/g;
		}

		#改行を<br>に変換する。
		#改行コードが違う場合を想定して、順に変換する。
		$value =~ s/\r\n/<br>/g;
		$value =~ s/\r/<br>/g;
		$value =~ s/\n/<br>/g;
		
		#連想配列%FORMにキー$nameと値$valueとして指定する。
		$FORM{$name} = $value;
	}
	
##データのフォーマット

	#HPアドレスの最初のhttp://の部分を削除する。
	$FORM{'url'} =~ s/^http:\/\///g;

	#連想配列では使いづらいので、変数に代入しなおす。
	$mode    = $FORM{'mode'};
	$name    = $FORM{'name'};
	$email   = $FORM{'email'};	
	$sub     = $FORM{'sub'};
	$url     = $FORM{'url'};
	$comment = $FORM{'comment'};
	$pass    = $FORM{'pass'};
	$num     = $FORM{'num'};
	$cnt     = $FORM{'cnt'};
	$del     = $FORM{'del'};
	$bname   = $FORM{'bname'};
	$res     = $FORM{'res'};
	$color   = $FORM{'color'};
	$ie      = $FORM{'ie'};
	$owner   = $FORM{'owner'};
	$count   = $FORM{'count'};
	$sec     = $FORM{'sec'};
	$pass_t  = $FORM{'pass_t'};

	
	
	#記事内にアドレスなどがあったら、自動でリンクをはる処理を行なうため
	&auto_link($comment);
	&auto_link($res);
}                                                          
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃削除キーを暗号化する処理                                ┃
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
sub make_pass{

	#受け取った削除キーを変数に代入しなおす
	$password = $_[0];

	#現在時刻（秒）を取得する。
	$time2 = time;

	#現在時刻（秒）の下二桁を暗号化する塩として取り出す。
	$salt = substr($time2,-2,2);
	
	#crypt関数によって、暗号化し、その値をこのサブルーチンがよばれた場所に返す
	return crypt($password,$salt);
}                                                          
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃削除キーの照合処理                                      ┃
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
sub match_pass{                                            
                                                           
	#受け取った配列を、設定されていた削除キー$log_passと入力された削除キー$form_passに代入しなおす。
	($form_pass,$log_pass)= @_;

	#塩の場所を調べる
	if ($log_pass =~ /^\$1\$/) { $key=3;}
	else{ $key = 0; }

	#設定されていた削除キーと入力された削除キーが一致するかを判断
	if (crypt($form_pass,substr($log_pass,$key,2)) eq "$log_pass"){
	
		#一致したら、このサブルーチンを呼んだところに、値"ok"を返す
		return 'ok';
	}else{
	
	#一致しなかったら、このサブルーチンを呼んだところに、値"ng"を返す
		return 'ng';
	}
}                                                          
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃フォームの下に注意メッセージを表示する処理              ┃
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
sub uemess {                                               

	#ログの更新処理などの途中であった場合を想定して、ロックを解除する。
	if($lock_check){&unlock;}

	#メッセージ内容を、tempデータに入れる。
	$uemess = "$_[1] $_[0]";
	
	#メイン表示サブルーチンsub htmlへ
	&html;
}                                                          
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
 
#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃エラーメッセージの表示処理                              ┃
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
sub error {                                                

	#ログの更新処理などの途中であった場合を想定して、ロックを解除する。
	if($lock_check){&unlock;}
	
 &head_html("error message");

print <<"EOM";
<center>
<table border=0 bgcolor="#777777" width=400 cellpadding=5>
	<tr>
		<td align=center>
			<table width=370>
				<tr>
					<td align=center bgcolor="#eeeeee"><font color="#333333">---Message---</font></td>
				</tr>
				<tr>
					<td align=center><hr size=1><br>$_[0]</td>
				</tr>
				<tr>
					<td align=right><hr size=1><br>$ver <a href="http://www.kaism.com">kaism</a></td>
				</tr>
			</table>
		</td>
	</tr>
</table>
</center>
</body>
</html>
EOM
	exit;
}                                                          
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃リンク処理                                              ┃
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
sub auto_link {                                            

	#受け取った値$_[0]をリンクを張った状態に変換する。
	$_[0] =~ s/([^=^\"]|^)(http\:[\w\.\~\-\/\?\&\+\=\:\@\%\;\#]+)/$1<a href=\"$2\" target='$target'>$2<\/a>/g;
}
                                                           
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃現在日時の取得・フォーマット処理                        ┃
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
sub get_time {                                             

	#日本時間を指定
	$ENV{'TZ'} = "JST-9";

	#timeで取得した秒をそれぞれの要素に分ける。
	#各要素は(秒・分・時・日・月・年・曜日・夏時間調整・？）
	($sec,$min,$hour,$mday,$mon,$year,$wday,$d,$d) = localtime(time);

	#年$yearは1900年からの年数なので、1900を足す
	$year += 1900;

	#月$monは0から11なので、１足す。
	$mon++;

	#各値で、一桁のときは、最初に０を足す。（見た目のため）
	if ($mon  < 10) { $mon  = "0$mon";  }
	if ($mday < 10) { $mday = "0$mday"; }
	if ($hour < 10) { $hour = "0$hour"; }
	if ($min  < 10) { $min  = "0$min";  }
	if ($sec  < 10) { $sec  = "0$sec";  }

	#曜日$weekは0から6なので、それを文字に変換する。
	$week = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat') [$wday];

	#日時をフォーマットする。
	$date = "$year\/$mon\/$mday\($week\) $hour\:$min\:$sec";

	#時間の秒を取得しておく。
	$second = time;
}                                                          
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛


#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃ホスト名を取得する処理                                  ┃
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
sub get_host {                                             

	#環境変数から、ホスト名・IPアドレスを取得する。
	$host = $ENV{'REMOTE_HOST'};
	$addr = $ENV{'REMOTE_ADDR'};

	#ホスト名が取得できなかったか、IPアドレスのみのときは、
	#IPアドレスから、ホスト名に変換する。
	if ($host eq "" || $host eq "$addr") {
			$host = gethostbyaddr(pack("C4", split(/\./, $addr)), 2);
	}

	#変換できなければ、しょうがないので、IPアドレスを$hostに入れる。
	if ($host eq "") { $host = $addr; }
}                                                          
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃ロック処理                                              ┃
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
sub lock{                                                  
	#ロックを判断するファイルの指定
	$lockfile = "board.lock";

	#処理を判断する旗を立てる
	local($flag) = 0;

	#リトライ回数を指定（デフォルトは５回）
	foreach (1..5) {

		#ロックファイルが存在すれば、1秒待つ
		if (-e $lockfile){
			 sleep(1);
		}else{

			#ロックファイルがなければ、容量ゼロのロックファイル$lockfileを作成する。
			open(LOCK,">$lockfile");
			close(LOCK);

			#処理をしたことを示す旗に印をつける。
			$flag = 1;

			#リトライ・ループから抜け出す。
			last;
		}
	}

	#旗に印がなければ、ロックファイルがあり、誰かが書きこみ処理をしていることだから、
	#しばらく待ってもらう旨のメッセージを表示させる。
	if ($flag == 0) {
		&uemess("しばらく待ってから再度投稿してください。")
	}
}
                                                           
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛


#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃ロック解除処理                                          ┃
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
sub unlock{                                                

	#処理が終了した印である、ロックファイルを削除して、
	#他の人が書きこみなど出来るようにしてあげる。
	if (-e,$lockfile){unlink($lockfile);}
}                                                          
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃クッキーを発行する処理                                  ┃
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
sub set_cookie{                                            

	#クッキーの保存期間は60日に指定
	($secg,$ming,$hourg,$mdayg,$mong,$yearg,$wdayg,$dmy,$dmy) = gmtime(time + 60*24*60*60);

	#以下、日付のフォーマット
	$yearg += 1900;
	if ($secg  < 10) { $secg  = "0$secg";  }
	if ($ming  < 10) { $ming  = "0$ming";  }
	if ($hourg < 10) { $hourg = "0$hourg"; }
	if ($mdayg < 10) { $mdayg = "0$mdayg"; }

	$month = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')[$mong];
	$youbi = ('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday')[$wdayg];

	$date_gmt = "$youbi, $mdayg\-$month\-$yearg $hourg:$ming:$secg GMT";

	#クッキーの内容を指定
	$cook="cname\:$name\,cemail\:$email\,curl\:$url\,cpass\:$pass";

	#クッキーを焼く
	print "Set-Cookie: kboard=$cook; expires=$date_gmt\n";
}                                                          
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃クッキーを取得する処理                                  ┃
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
sub get_cookie {                                           
	
	#クッキー情報を取得
	@pairs = split(/\;/, $ENV{'HTTP_COOKIE'});
	
	#読み取ったクッキーを1つづつ調べる
	foreach $pair (@pairs) {
		local($name, $value) = split(/\=/, $pair);
		$name =~ s/ //g;
		$DUMMY{$name} = $value;
	}

	#kboardのクッキーを取り出す
	@pairs = split(/\,/, $DUMMY{'kboard'});
	
	#クッキー情報を分析
	foreach $pair (@pairs) {
		local($name, $value) = split(/\:/, $pair);

		#フォームに取得したクッキーを表示させるために、%cookie配列に代入する。
		$cookie{$name} = $value;
	}

	#書きこみをした直後であれば、最新の情報に取り替える
	if ($FORM{'name'})  { $cookie{'cname'}  = $FORM{'name'}; }
	if ($FORM{'email'}) { $cookie{'cemail'} = $FORM{'email'}; }
	if ($FORM{'url'})   { $cookie{'curl'}   = $FORM{'url'}; }
	if ($FORM{'pass'})  { $cookie{'cpass'}  = $FORM{'pass'}; }
}
                                                           
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛


#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃メール送信処理 ┃
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
sub mail_to { 

	#記事内容の、改行等を変換する。
	$comment =~ s/<br>/\n/g;
	$comment =~ s/&lt;/</g;
	$comment =~ s/&gt;/>/g;

	#mailのタイトル指定
	if ($mailtitle_chek){
		$mail_title = "[$num] $sub";
	}else{
		$mail_title = "$mail_sub";
	}

	##mailの本文の作成##
	$mailbody = <<"EOM";
--------------------------------------------------------
投稿日時： $date
ホスト： $host
名前： $name
MAIL： $email
URL： http://$url
タイトル： $sub

$comment
--------------------------------------------------------
EOM

	##データのフォーマット処理
	#文字コードをjisに変換する。
	&jcode'convert(*mail_title,'jis');
	&jcode'convert(*mailbody,'jis');

	##sendmailへの出力処理

	#sendmailを開く
	#開ければ
	if (open(MAIL,"| $sendmail $mailto")) {

		#受信者のアドレスを指定
		print MAIL "To: $mailto\n";

		#投稿者のメールアドレスがなければ、ダミーのアドレスを代入
		if ($email eq "") { $email = "nomail\@xxx.xxx"; }

		#メールの内容を出力
		print MAIL "From: $email\n";
		print MAIL "Subject: $mail_title\n";
		print MAIL "MIME-Version: 1.0\n";
		print MAIL "Content-type: text/plain; charset=ISO-2022-JP\n";
		print MAIL "Content-Transfer-Encoding: 7bit\n";
		print MAIL "X-Mailer: kaism kboard\n\n";
		print MAIL "$mailbody\n"; 
		#sendmailを閉じる
		close(MAIL);
	}

} 
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃新着表示処理                                            ┃
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
sub new_time{                                              

	#何時間前を新着とするかを指定。
	$newd = time - 60*60*$new_time;

	#指定した時刻（秒）よりも、投稿時刻（秒）が新しければ
	if ($newd <= $second){
	
		#新着マーク画像があれば、それを表示
		if ($newgif){
			$date = "<img src=\"$newgif\" width=$newgif_w height=$newgif_h> $date";
		
		#なければ、日付に色をつける。
		}else{
			$date = "<font color=\"$newcolor\">$date</font>";
		}
	}
}                                                          
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃HOW TO 表示処理                                         ┃
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
sub how_to{                                                

##how toコメントの指定
	
	#タグを許可するなら
	if ($tag_check){
		$howto_tag = "<li><b>タグ</b>は使えます。閉じ忘れに注意。<br>";
	
	#許可しないのなら
	}else{
		$howto_tag = "<li><b>タグ</b>は使えません。<br>";
	}
	
	#必須項目のチェック
	$howto_hissu = "<li>";
	
	#名前が必須項目なら
	if ($name_check){
	
		#変数に追加。
		$howto_hissu .= "<b>name</b> ";
		
		#必須項目があることをチェック
		$flag=1;
	}
	
	#メールアドレスが必須項目なら
	if ($email_check){
	
		#変数に追加。
		$howto_hissu .= "<b>email</b> ";
		
		#必須項目があることをチェック
		$flag=1;
	}
	
	#タイトルが必須項目なら
	if ($sub_check){
	
		#変数に追加
		$howto_hissu .= "<b>title</b> ";
		
		#必須項目があることをチェック
		$flag=1;
	}
	
	#キーが必須項目なら
	if ($pass_check){
	
		#変数に追加
		$howto_hissu .= "<b>key</b> ";
		
		if($name_pass_check){
			$howto_hissu .= "(変更不可)";
		}
		
		#必須項目があることをチェック
		$flag=1;
	}
	
	#必須項目があるのなら
	if ($flag){
	
		#変数に追加
		$howto_hissu .= "の欄は必須です。";
	
	#必須項目がなければ、
	}else{
	
		#変数をクリアーする
		$howto_hissu = "";
	}

	#新着マーク処理をするなら
	if ($new_time_check) {
	
		#マーク画像を使うなら
		if ($newgif){
			
			#マーク画像がつくことを変数に代入
			$howto_newmark = "<li><b>$new_time</b>時間以内の投稿には<img src=\"$newgif\" width=$newgif_w height=$newgif_h>がつきます。";
		
		#日付の色付けなら
		}else{
		
			#日付に色がつくことを変数に代入
			$howto_newmark = "<li><b>$new_time</b>時間以内の投稿は、日時に<font color=\"$newcolor\">色</font>がつきます。";
		}
	}
	
	#削除キーに関する説明
	$howto_key     = "<li><b>key</b>(英数半角8文字以下)を設定しておくと、自分の投稿を後で削除することができます。<li>自分の記事を削除したい時は、その記事の右下のフォームに<b>key</b>を入力し<img src=\"$gomi_gif\">をクリックしてください。";
	
	# change #1
	#town表示に関する説明
	$howto_town    = "<li><b>$town_title</b>では、規定の投稿数を超えるとそのたびに持ち家が変化していきます。";
	
	# change #2
	#別窓表示の時の説明
	if (!$ktown){
		$howto_town .= "<li><b>town画像</b>をクリックすると、町並みがみれます。";
	}
	
	
	# change #3
	#私書箱機能の説明
	if ($shishobako_check){
		$howto_shisho = "<li>各家に<b>置き手紙</b>を残すことができます。ポストをクリックしてください。<li>ポストに<b>手紙</b>がある時は、<b>未読</b>の置き手紙があることを示しています。<li>各家ごとに最大<b>$resmax件</b>の置き手紙が保存されます。";
	}
	
	if ($oki_pass_check){
		$howto_shisho .= "<li>掲示板で投稿するときに<b>key</b>を設定しておくと、<b>ポストに鍵</b>をかけることができ、他の人に置き手紙を覗かれなくなります。";
	}
	
	# change #4
	#家成長機能に関して
	$howto_town   .= "<li><b>$old_limit</b>日間投稿がないと、廃墟に、<b>$baikyaku_limit</b>日間投稿がないと、売却されますのでご注意ください。売却されると買った人にカウント数が追加されます。売却と同時に書き込みした人だけ買うことができます。";
	
	#書き込みするときにクリックする画像の説明
	$howto_post    = "<li>書きこみしたあと、<img src=\"$submit_gif\" width=$submit_w height=$submit_h>をクリックして投稿します。";
	
	#なりすましチェックの説明
	if($name_pass_check){
		$howto_npcheck ="<li>2回目以降のカキコでは、<b>名前</b>と<b>key</b>が一致するかどうかをチェックしています。一致しない場合書き込みができなくなりますのでご注意ください。";
	}

##how to 表示のフォーマット

	#以上を、使い方の説明にまとめて代入
	$howto = "<ul type=circle>$howto_post\n$howto_tag\n$howto_hissu\n$howto_npcheck\n$howto_newmark\n$howto_key\n$howto_town\n$howto_shisho</ul><center><a href=\"$script?\">使い方をとじる</a></center>\n";
}
                                                           
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛


#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃ページ処理                                              ┃
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
sub page{                                                  

##ページ番号の指定処理
##行番号で指定する（最初の行は0行）

	#ページ指定がなければ、最初の行番号を指定
	if ($FORM{'page'} eq '') { $page_start = 0; } 

	#ページ指定があれば、その行番号を指定
	else { $page_start = $FORM{'page'}; }

	#ログファイルの最後の記事の行番号を指定
	#総行数-1とするのは、行番号は0から始まってるから
	$all_data = @lines - 1;

	#表示する最後の記事を行数で指定。
	$page_end = $page_start + $pagelog - 1;

	#ログファイルの最後の行番号よりも、指定した最後の行番号が大きければ
	#ログファイルの最後の行番号を、表示する最後の記事の行番号に指定しなおす。
	if ($page_end >= $all_data) { $page_end = $all_data; }

	#次のページの最初の記事の行番号を指定
	$next_page = $page_end + 1;
	
	#前のページの最初の記事の行番号を指定
	$back_page = $page_start - $pagelog;

##ページ変更ボタンの表示処理

	#もし、前のページがあるのならば、
	if ($back_page >= 0 ){

	#$page_back変数に代入する。
	$page_back = <<"EOM";
<form method="$method" action="$script">
<input type=hidden name=page value="$back_page">
<input type=image src="$back_gif" width=$back_w height=$back_h border=0>
</form>
EOM
	}

	#もし、次のページのがあるのなら、
	if ($page_end ne "$all_data") {

	#$page_next変数に代入する。
	$page_next =<<"EOM";
<form method="$method" action="$script">
<input class="input" type=hidden name=page value="$next_page\">
<input type=image src="$next_gif" width=$next_w height=$next_h border=0>
</form>
EOM
	}
}                                                          

#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛


#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃house page count処理                                    ┃
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
sub house_count{
	
	if($FORM{'hpc'} eq ''){
		$house_start = 0;
	}else{
		$house_start = $FORM{'hpc'};
	}
	
	$house_num = 20;
	$house_end = $house_start + $house_num - 1;
	
	if($house_end >= $#lines){
		$house_end = $#lines;
	}
	
	$house_next = $house_start + $house_num;
	
	$house_back = $house_start - $house_num;
}
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃town表示処理                                            ┃
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
sub ktown{                                                  

##townの表示処理
	
	#テーブルを作成
	print <<"EOM";
	<table cellspacing=0 cellpadding=0 border=0>
		<tr>
			<td nowrap align=center colspan=5><b>$town_title</b><br><img src="$iedir/town.gif"></td>
		</tr>
EOM

##townデータ取得処理

	#rankデータファイルを開く
	open (IN,"$rankfile") || &error("$rankfileが開けませんでした。");
	
	#データの各行を変数に代入
	@lines = <IN>;
	
	#データファイルを閉じる
	close (IN);

##データのフォーマット・表示処理
	
	#家の配置を制御する変数を指定
	$side = 0;

	#データをひとつづつ分析する
	
	#家表示ページ処理へ
	&house_page_count;

	print "<tr><td colspan=2 width=90 nowrap align=center>";

	if($ktown == 1){
		$ktown_win_select = none;
	}else{
		$ktown_win_select = town;
	}
	
	#前のページがあれば
	if ($house_back >= 0){
		print "<a href=\"$script?hpc=$house_back\&mode=$ktown_win_select\"><img src=\"$back_gif\" width=$back_w height=$back_h border=0 alt=\"前の通りへ\"></a>";
		
	#無いなら
	}else{
		print "<br>";
	}
	
	#道の部分の表示
	print <<"EOM";
</td>
			<td width=15 bgcolor="#cccccc" nowrap><img src="$gifdir/spacer.gif" width=15 height=40></td>
			<td width=90 colspan=2 nowrap align=center>
EOM
	
	#次のページがあれば
	if ($house_next <= $#lines){
		print "<a href=\"$script?hpc=$house_next\&mode=$ktown_win_select\"><img src=\"$next_gif\" width=$next_w height=$next_h border=0 alt=\"次の通りへ\"></a>";
	
	#無ければ
	}else{
		print "<br>";
	}
	

	print "</td></tr>";

	#表示分だけ・・・
	foreach ($house_start .. $house_end){
		($name,$count,$town,$url,$sec,$pass,$mflag) = split(/<>/,$lines[$_]);
		
		$mflag=~ s/\n//g;
		$sec  =~ s/\n//g;
		$pass =~ s/\n//g;
		
		$ie = &ie_size($count);
		
		#廃墟の期限かどうかを判断
		$old = time - 60*60*24*$old_limit;  #廃墟期限を指定
		
		#もしも廃墟期限になっていたら、家アイコンを廃墟画像に変更
		if ($old > $sec){$ie = "old";}

		#投稿日時のフォーマット
		&ktown_time;

		#総投稿数を取り出す
		$count = $count + $town * 100;
		
		#肩書きを入れる変数を指定
		$katagaki = "";

		# change #5
		#肩書き指定
		if($count >99) {$katagaki = "町長";}	#１００件以上なら
		if($count >199){$katagaki = "市長";}	#２００件以上なら
		if($count >299){$katagaki = "知事";}	#３００件以上なら
		if($count >399){$katagaki = "首相";}	#４００件以上なら
		if($count >499){$katagaki = "地球王";}	#５００件以上なら
		if($count >599){$katagaki = "宇宙王";}	#６００件以上なら


		#ポスト画像を指定
		$post = "$post1";

		#未読があるかどうかのチェック
		if($mflag){
			$post = "$post2";
		}
		
##私書箱機能を使うときの表示処理

		#私書箱機能を使うなら
		if ($shishobako_check){
			
			if ($oki_win_check){
				$oki_target = "oki_window";
			}else{
				$oki_target = "";
			}
			
			#v12.00#
			($en_name,$en_url) = &url_encode($name,$url);
			
			#道の左側に表示
			if ($side == 0){
			
				#次の家を右側に表示させるための印
				$side = 1;
			
				#表示
				print <<"EOM";
		<tr>
			<td valign=bottom align=right>$katagaki $name [$count]<br>$date<br>
EOM
				if ($url){
					print "<a href=\"http\://$url\" target=$target><img src=\"$iedir/$ie.gif\" border=0></a>\n";
				}else{
					print "<img src=\"$iedir/$ie.gif\" border=0>\n";
				}
				print <<"EOM";
			</td>
			<td valign=bottom align=right>
				<!--- #v12.00# ---><!--- #v12.20# --->
				<a href="$script?mode=res_html&owner=$en_name&url=$en_url&count=$count&ie=$ie" target="$oki_target">
					<img src="$post" width=$post_w height=$post_h border=0>
				</a>
			</td>
			<td width=15 bgcolor="#cccccc"><img src="$gifdir/spacer.gif" width=15 height=1></td>
			<td><br></td>
			<td><br></td>
		</tr>
EOM

			#道の右側に表示
			}else{
			
				#次の家は左側に表示させるための印
				$side = 0;
				print <<"EOM";
		<tr>
			<td><br></td>
			<td><br></td>
			<td width=15 bgcolor="#cccccc"><img src="$gifdir/spacer.gif" width=15 height=1></td>
			<td valign=bottom align=left>
				<!--- #v12.00# ---><!--- #v12.20# --->
				<a href="$script?mode=res_html&owner=$en_name&url=$en_url&count=$count&ie=$ie" target="$oki_target">
					<img src="$post" width=$post_w height=$post_h border=0>
				</a>
			</td>
			<td valign=bottom align=left>$katagaki $name [$count]<br>$date<br>
EOM
				if ($url){
					print "<a href=\"http\://$url\" target=$target><img src=\"$iedir/$ie.gif\" border=0></a>\n";
				}else{
					print "<img src=\"$iedir/$ie.gif\" border=0>\n";
				}
				print <<"EOM";
			
			</td>
		</tr>
EOM
			}

	#私書箱機能を使わないのなら
		}else{
			#道の左側に表示
			if ($side == 0){
		
				#次の家を右側に表示させるための印
				$side = 1;
		
				#表示
				print <<"EOM";
		<tr><td valign=bottom align=right>$katagaki $name [$count]<br>$date<br>
EOM

				#投稿者にHPがあれば家アイコンにリンクをはる
				if ($url ne ""){
					print "<a href=\"http://$url\" target=_blank><img src=\"$iedir/$ie.gif\" border=0></a>";
			
				#なければ、そのまま。
				}else{
					print "<img src=\"$iedir/$ie.gif\" border=0>";
				}
					print <<"EOM";
			</td>
			<td valign=bottom align=right><img src="$no_post" width=$no_post_w height=$no_post_h></td>
			<td width=15 bgcolor="#cccccc"><img src="$gifdir/spacer.gif" width=15 height=1></td>
			<td><br></td>
			<td><br></td>
		</tr>
EOM

		#道の右側に表示
			}else{
		
				#次の家は左側に表示させるための印
				$side = 0;
			
				print <<"EOM";
		<tr><td><br></td>
			<td><br></td>
			<td width=15 bgcolor="#cccccc"><img src="$gifdir/spacer.gif" width=15 height=1></td>
			<td valign=bottom align=left><img src="$no_post" width=$no_post_w height=$no_post_h></td>
			<td valign=bottom align=left>$katagaki $name [$count]<br>$date<br>
EOM
		
				#HPがあれば、家アイコンにリンクをはる。
				if ($url ne ""){
					print "<a href=\"http://$url\" target=_blank><img src=\"$iedir/$ie.gif\" border=0></a>";
		
				#なければそのまま
				}else{
					print "<img src=\"$iedir/$ie.gif\" border=0>";
				}
					print <<"EOM";
			</td>
		</tr>
EOM
			}
		}
	}
	
	
		print "<tr><td colspan=2 width=90 nowrap align=center>";
	
	if ($house_back >= 0){
		print "<a href=\"$script?hpc=$house_back\&mode=$ktown_win_select\"><img src=\"$back_gif\" width=$back_w height=$back_h border=0 alt=\"\前の通りへ\"></a>";
	}else{
		print "<br>";
	}
	
	print <<"EOM";
</td>
			<td width=15 bgcolor="#cccccc" nowrap><img src="$gifdir/spacer.gif" width=15 height=40></td>
			<td width=90 colspan=2 nowrap align=center>
EOM
	
	if ($house_next <= $#lines){
		print "<a href=\"$script?hpc=$house_next\&mode=$ktown_win_select\"><img src=\"$next_gif\" width=$next_w height=$next_h border=0 alt=\"次の通りへ\"></a>";
	}else{
		print "<br>";
	}
	
	print "</td></tr>";
	
	#テーブルを閉じる
	print "\t</table>\n";
}
                                                           
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃別窓でtownを表示する処理                                ┃
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
sub ktown_win{                                                 
	
 &head_html("$town_title");

	print "<center>\n";

	#town表示メイン処理
	&ktown;
	
	print "</center></body></html>";
	
	exit;
}
                                                           
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃townにつかう日時表示の処理                              ┃
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
sub ktown_time{                                             

	#日本時間を指定
	$ENV{'TZ'} = "JST-9";

	#各要素は(秒・分・時・日・月・年・曜日・夏時間調整・？）
	($sec,$min,$hour,$mday,$mon,$year,$wday,$d,$d) = localtime($sec);

	#年$yearは1900年からの年数なので、1900を足す
	$year += 1900;

	#月$monは0から11なので、１足す。
	$mon++;

	#各値で、一桁のときは、最初に０を足す。（見た目のため）
	if ($mon  < 10) { $mon  = "0$mon";  }
	if ($mday < 10) { $mday = "0$mday"; }
	if ($hour < 10) { $hour = "0$hour"; }
	if ($min  < 10) { $min  = "0$min";  }
	if ($sec  < 10) { $sec  = "0$sec";  }

	#日時をフォーマットする。秒数はカットした。
	$date = "$year\/$mon\/$mday";
	$rdate= "$mon\/$mday $hour:$min";


}                                                          
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃townのデータの更新処理                                  ┃
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
sub ktown_up{

	#投稿回数を増やすのか、減らすのかの判断（up or down）を取得
	local($flag) = "$_[0]";

##データ取得処理

	#データファイルを開く
	open (IN,"$rankfile")  || &error("$rankfileが開けませんでした");

	#データの各行を変数に代入
	@lines = <IN>;
	
	#ファイルを閉じる
	close(IN);
	
##更新するデータを見つけ、データをフォーマットする処理

	#更新されたデータをいれる配列の指定
	@ranks = ();
	
	#売却される家のデータを入れる配列の指定
	@saledata = ();

	#データを1つづつ分析する。
	foreach $line (@lines){
	
		#最後のtはtownのt
		($namet,$cnt,$town,$urlt,$sect,$passt,$mflagt) = split(/<>/,$line);
		
		$mflagt=~ s/\n//g;
		$sect =~ s/\n//g;
		$passt=~ s/\n//g;
		
		#更新するデータを名前で判断する。
		#$nameの値は、&write or &clearからのもの。
		if ($name eq "$namet"){

			#&writeからきた場合
			if ($flag eq "up"){
				
				#カウントをアップ
				++$cnt;

				#投稿回数が１００を超えた時の処理
				if ($cnt > 100){
				
				#100の位を制御する$townのカウントをアップ
				++$town;
				
				#カウントを1に戻す
				$cnt = 1;
				}

				#データをフォーマット
				#$url,$second,$PWは&writeからの値
				$rank = "$namet<>$cnt<>$town<>$url<>$second<>$PW<>$mflagt\n";

			#&clearからの場合
			}elsif($flag eq "down"){
				
				#カウントをダウン
				$cnt=$cnt-1;

				#減らした時に、投稿回数が０となった時
				if ($cnt <1){

					#総投稿回数が１００を越えてい場合
					if ($town >0){
					
						#カウントを100にする
						$cnt = 100;
						
						#100の位を制御する$townを１減らす
						$town = $town-1;
					
					#１００を越えていないときは、そのデータを削除する印をつける
					}else{$nodata = "yes";}
				}

				#データを更新する。
				$rank = "$namet<>$cnt<>$town<>$urlt<>$sect<>$passt<>$mflagt\n";
			}

		#更新するデータでない場合
		}else{
	
			#データのなかで、売却期限となっているかの判断
			$baikyaku = time - 60*60*24 * $baikyaku_limit;    #売却期限
		
			#売却対象とならないものだけ、保存する。
			if ($sect > $baikyaku){
				push(@ranks,$line);
			
			#売却対象の家があったとき
			}else{
				
				#売却配列に追加
				push(@saledata,$line);
				
				#売却対象があったことの印
				$saleflag = 1;
			}
		}
	}

##更新するデータが無い時
##初投稿 or townデータ修正で削除されていた場合

	#初めての投稿の場合
	#ダウンの場合を排除
	if ($flag eq "up" && $rank eq ""){
	
		#データのフォーマット
		#$name,$url,$second,$PWは&writeからの変数
		$rank = "$name<>1<>0<>$url<>$second<>$PW<>0\n";
	}

##売却処理

	#売却対象があった場合
	if ($saleflag){
		
		#総カウント数の変数を指定
		$cntup =0;
		
		#売却対象のすべての家データを分析
		foreach (@saledata){
		
			#分解して、配列に代入
			@data = split(/<>/,$_);
			
			#カウント数を取込む
			$cntup = $cntup + $data[1];
		}
	}

##新規データ配列に追加処理
##売却時のカウント処理

	#更新が削除でなければ、
	#削除処理の場合は、売却カウントアップ処理は
	#行なわない。つまり、そのまま売却（削除）されるだけ
	unless ($nodata eq "yes"){
		
		#売却する家があれば、
		if ($saleflag){
		
			#不動産売却機能を使う場合は
			if($fudousan_check){
		
				#改めて、今書き込みした人のデータを分析
				#先頭のsはsaleのs
				($sname,$scnt,$stown,$surl,$ssec,$spass,$smflag) = split(/<>/,$rank);
				
				$spass =~ s/\n//g;
				$smflag=~ s/\n//g;
				
				#カウントを追加
				$scnt = $scnt + $cntup;
				
				#追加した結果が、100以下になるまで、
				while ($scnt > 100){
				
					#100の位を制御する$stownのカウントをアップ
					++$stown;
					
					#$scntから100を引く
					$scnt = $scnt - 100;
				}
				
				#データのフォーマット
				$rank = "$sname<>$scnt<>$stown<>$surl<>$ssec<>$spass<>$smflag\n";
				
				#不動産報告メッセージの書きこみ処理へ
				&fudousan;

			}
		}
		
		
		#更新配列の一番上に追加
		unshift(@ranks,$rank);
	}

##データ更新処理

	#データファイルを開く
	open (OUT,">$rankfile");
	
	#新規データ配列を出力
	print OUT @ranks;
	
	#ファイルを閉じる
	close (OUT);
}
                                                           
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛


#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃不動産屋からの報告を書き込みする処理                    ┃
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
sub fudousan{
 
	#ログファイルを開く
	open (IN,"$logfile") || &error("投稿記事保存ファイル$logfileが開けませんでした。");

	#直前の行を配列に代入
	@lines = <IN>;
	
	#ファイルを閉じる
	close(IN);
	
	#直前のデータを取得する
	@bline = split(/<>/,$lines[0]);

	#直前の記事Noを取得
	$bnum = $bline[0];
	
	#記事Noを代入
	#fはfudousanのf
	$fnum  = $bnum + 1;
	
	#買主の名前をとりだす。
	$kainushi = "$sname";
	
	#不動産のリストを入れる配列を指定
	@ielist = ();

##売却リスト作成

	#売却対象配列を1つづつ分析
	foreach(@saledata){
	
		#売却対象データを分割する。
		@bukken = split(/<>/,$_);
		
		#持ち主の名前を取り出す
		$urinushi = "$bukken[0]";
		
		# change #6
		#投稿数から値段を決定する
		#なんとなく値段らしいものにするため
		#あえて半端な数をかける
		$nedan    =  $bukken[1] * 976;
		
		# change #7
		#物件データをフォーマット
		$list     = "<b>$urinushi</b> 様の土地建物 <b>$nedan</b> 万円 で売却。";
		
		#不動産リスト配列に追加
		push (@ielist,$list);
	}

##掲示板に書きこむデータを作成

	# change #8
	#名前
	$fname    = "$town_title不動産";
	
	# change #9
	#タイトル
	$fsub     = "売却報告";
	
	# change #10
	#コメント内容１（前置き）
	$fcomment = "このたび <b>$kainushi</b> 様との間で土地建物売却契約が成立しました。<br>";
	
	#コメント内容２（物件リスト）追加代入
	$fcomment .= join ('<br>',@ielist);
	
	#コメント内容３ （しめ）追加代入
	$fcomment .= "<br>以上により <b>$kainushi</b> 様の総カウント数は $cntup だけアップしました。";

	#データのフォーマット
	$line = "$fnum<>$fname<><><>$fsub<>$fcomment<>$fres<>$date<>$second<><>\n";

	#データ配列の先頭に追加
	unshift(@lines,$line);
	
	#データファイルを書きこみ用に開く
	open (OUT,">$logfile") || &error("$logfileが開けませんでした");
	
	#データ配列を書きこむ
	print OUT @lines;
	
	#ファイルを閉じる
	close(OUT);
}
                                                           
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃過去ログファイルを更新する処理                          ┃
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
sub pastwrite{                                             

##過去ログNOを取得する処理
	
	#過去ログNOファイルを開く
	open (IN ,"$pcnt_file") || &error("$pcnt_fileが開けませんでした") ;
	
	#一行目のNoだけをとりだす
	$pcnt = <IN>;
	
	#ファイルを閉じる
	close (IN);
	
	#行末の改行文字を削除する
	$pcnt =~ s/\n//g;
	
##過去ログディレクトリの設定がちゃんとなっているかのチェック処理（最初だけ）

	#過去ログファイルが生成されていないなら
	if ($pcnt == 0){
	
		#ダミーファイルを過去ログファイルを保存するディレクトリに指定する。
		$dmyfile = "$pastdir\/dmy.html";
		
		#ダミーファイル作成（作成できなければ、処理を中断）
		open (DMY,">$dmyfile") || &error("過去ログディレクトリの指定を再度確認してください。");
		
		#ダミーファイルを閉じる
		close (DMY);
		
		#ダミーファイルを削除する。
		unlink($dmyfile);
	}

##書きこむファイルを決定する処理

	#現在ある最新の過去ログファイルを指定
	$p_file = "$pastdir\/$pcnt\.html";

	#過去ログファイルがなければ、作成する処理に。
	#はじめて過去ログファイルを作る時が、これにあたる。
	#0.htmlファイルなんてある分けない
	unless(-e $p_file){&new_pfile;}
	
	
	#現在ある最新の過去ログファイルを開く
	open (IN,"$p_file") || &error("$p_fileが開けませんでした");
	
	#各行を配列に代入
	@plines = <IN>;
	
	#ファイルを閉じる
	close (IN);
	
	#過去ログファイルの最大行数の最後の行番号を指定
	#26は記事以外の行数（&new_pfileのベースhtmlを作成を参照してください。）
	$pline_max = 26 + $pline_max - 1;

	
	#今ある過去ログファイルの最終行の行番号が、最大行数の行番号とおなじなら
	#$#plinesは今ある過去ログファイルの最終行の行番号
	if ($#plines >= $pline_max){
	
		#新しい過去ログファイルを作成する処理に
		&new_pfile;
	}

##書き込み処理

	#書きこむ記事を入れる配列を指定
	@phtmls= ();

	#&writeからきた溢れ出した記事が入った配列1つづつを分析
	foreach (@pasts){
	
		#データを分解
		#投稿日時（秒）、ホスト情報、削除キーはいらないので、ダミーに代入
		($pnum,$pname,$pemail,$purl,$psub,$pcomment,$pres,$pdate,$xx,$xx,$xx) = split(/<>/,$_);
		
		#メールアドレスがあれば、名前にリンク
		if ($pemail){$pname = "<a href=\"mailto:$pemail\">$pname</a>";}
		
		#サイトがあれば、[url]の文字にリンク
		if ($purl){$purl = "| [<a href=\"http://$purl\" target=_blank>url</a>]";}
		
		if ($pres){$pres_data = "<ul><ul><font color=\"$master_color\">$pres</font><p align=right>$master_name</p></ul></ul>";}

		#記事を整理する。
		$phtml = "<p align=left><b>[$pnum]$psub</b><br>$pdate</p><ul>$pcomment</ul><p align=right>$pname $purl</p>$pres_data<hr size=1>\n";
		
		#書きこむ配列に代入
		push(@phtmls,$phtml);
	}

	#過去ログファイルを開く
	open (IN,"$p_file") || &error("$p_fileが開けませんでした");
	
	#各行を配列に代入
	@plines = <IN>;
	
	#ファイルを閉じる
	close(IN);
	
	#過去ログに改めて書きこむ、各行のデータを入れる配列の指定
	@pnews = ();
	
	#過去ログファイルに今まで書かれていたデータの各行に対して
	foreach $pline (@plines){
	
		#更新する配列に代入
		push(@pnews,$pline);
		
		#もしも、<!--start-->という行にきたら
		if($pline =~ /<!--start-->/i){
			
			#新しく書き込みする記事の配列を一気に代入
			push(@pnews,@phtmls);}
	}
	
	#過去ログファイルを開く
	open (OUT,">$p_file") || &error("$p_fileが開けませんでした");
	
	#更新データ配列を出力
	print OUT @pnews;
	
	#ファイルを閉じる
	close (OUT);

}
                                                           
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃過去ログファイルを作成する処理                          ┃
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
sub new_pfile{                                                  

##過去ログNoファイルを更新する処理

	#過去ログファイルのNOを1つ増やす
	++$pcnt;
	
	#過去ログNoファイルを開く
	open (CNT,">$pcnt_file") || &error("$pcnt_fileが開けませんでした");
	
	#Noを更新する
	print CNT "$pcnt";
	
	#ファイルを閉じる
	close (CNT);
	
##過去ログ数調整処理

	#過去ログ数調整を行なうか
	if ($pastlog_check){
		
		#現在の最新過去ログNo.最大過去ログ保存数よりおおきいなら
		#（削除すべき過去ログファイル候補があるということだから）
		if ($pcnt > $pastlog_max){
			
			#削除すべき過去ログファイルのなかで一番大きいNo.
			$pastlog_del = $pcnt - $pastlog_max;
			
			#削除すべき過去ログファイルを順に処理する
			foreach (1 .. $pastlog_del){
				
				#削除すべき過去ログファイルを指定
				$del_file = "$pastdir\/$_\.html";
				
				#その過去ログファイルが存在するなら
				if (-e $del_file){
					
					#そのファイルを削除
					unlink($del_file);
				}
			}
		}
	}
			
	
##過去ログファイルのベースを作成する処理

	#あらためて、過去ログファイルを指定
	$p_file = "$pastdir\/$pcnt\.html";

	#過去ログファイルを開く
	open (OUT,">$p_file") || &error("$p_fileが開けませんでした");
	
	#過去ログファイルのベースhtmlタグを書きこむ
	#この下のヒアドキュメント＋<body・・・の行数が、&pastwriteの過去ログの最大保存記事数の
	#26という行数にあたる。
	print OUT <<"EOM";
<html lang="ja">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>kboard過去ログ[$pcnt]</title>
<meta http-equiv="Content-Style-Type" content="text/css">
<style type="text/css">
<!--
a:link    {text-decoration:none;    color:$link; }
a:visited {text-decoration:none;    color:$vlink; }
a:active  {text-decoration:none;    color:$alink; }
a:hover   {text-decoration:underline;    color:$alink; }
table     {font-size:12px; }
.title    {font-size:18px; }
-->
</style>
</head>
EOM
	if ($bg_gif){
		print OUT "<body text=\"$text_color\" bgcolor=\"$bg_color\" background=\"$bg_gif\"link=\"$link\" alink=\"$alink\" vlink=\"$vlink\">\n";
	}else{
		print OUT "<body text=\"$text_color\" bgcolor=\"$bg_color\" link=\"$link\" alink=\"$alink\" vlink=\"$vlink\">\n";
	}
	print OUT <<"EOM";
<center>
<table border=0 width=400 bgcolor="$mess_color">
<tr><td>
<!--start-->
</td>
</tr>
</table>
</body>
</html>
EOM

	#ベース過去ログファイルを閉じる
	close (OUT);
	
	#過去ログファイルのパーミッションを指定
	chmod(0666,"$p_file");
}
                                                           
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃過去ログのフレームを生成する処理                        ┃
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
sub frame{                                                 

##過去ログファイルNOを取得する処理

	#過去ログNoファイルを開く
	open (IN,"$pcnt_file") || &error("$pcnt_fileが開けませんでした");
	
	#一行目のNoを代入
	$pcnt = <IN>;
	
	#ファイルを閉じる
	close (IN);

	#行末の改行文字を削除
	$pcnt =~ s/\n//g;


##フレームを生成する処理

	#html出力を宣言
	print "Content-type: text/html\n\n";
	
	#ヒアドキュメント
	print <<"EOM";
<html>
<frameset cols="*,200" border=0 >
	<frame src="$pastdir2/$pcnt.html" name="kiji">
	<frame src="$script?mode=menu" name="menu">
</frameset>
<noframes>
<body>
<center>
フレーム対応ブラウザでご覧ください
</center>
</body>
</noframes>
</html>
EOM

	#処理を終了する
	exit;

}                                                          
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛


#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃過去ログのメニュー（フレームの右側）表示の処理          ┃
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
sub menu{                                                  

##過去ログファイルNOを取得する処理

	#過去ログNoファイルを開く
	open (IN,"$pcnt_file") || &error("$pcnt_fileが開けませんでした");
	
	#一行目を読みこむ
	$pcnt = <IN>;
	
	#ファイルを閉じる
	close (IN);

	#行末の改行文字を削除する。
	$pcnt =~ s/\n//g;

 &head_html("過去ログメニュー");

	#ヒアドキュメント
	print <<"EOM";
<center>
	<table width=150 border=0 bgcolor="$info_bgcolor" cellspacing=5 cellpadding=0>
	<tr>
		<td align=center>過去ログ</td>
	</tr>
	<tr>
		<td align=center>｜<a href="$script" target=$b_target>掲示板に戻る</a>｜</td>
	</tr>
	<tr>
		<td align=center>
EOM

	#foreach処理の為に、Noをマイナス１する
	$pend = $pcnt - 1;

##過去ログ数調整処理
	#過去ログファイルの最大保存数を
	#0からはじまる数にする。
	$pastlog_max = $pastlog_max - 1;

	#過去ログファイル数を制限するなら、
	if ($pastlog_check){
	
		#最大過去ログファイル数以上であったら、
		if ($pend >= $pastlog_max){
			
			#リンクされる数を最大過去ログ数に変更
			$pend = $pastlog_max;
		}
	}
	

	#過去ログファイルの数だけ
	foreach (0..$pend){
		
		#リンクの順を逆にする為、全ファイル数から、引く
		$file_num = $pcnt - $_;
		
		#そのNo.の過去ログファイルがあるならば
		if (-e "$pastdir\/$file_num\.html"){
		
			#過去ログファイルへのリンクを表示
			print "[<a href=\"$pastdir2\/$file_num\.html\" target=\"kiji\">$file_num</a>]\n";
		}
	}
	
	#しめ
	print "</td></tr></table></center></body></html>\n";
	
	#処理を終了する
	exit;
	}                                                      
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛


#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃管理用マスター・キー認証処理                            ┃
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
sub admin_in{

	#注意メッセージの取得
	unless($_[0]=~ /value/){$mess2 = $_[0];}

 &head_html("管理者認証ページ");

	#ヒアドキュメント
	print <<"EOM";
<center>
<table border=0 bgcolor="$mess_color"><tr><td align=center valign=middle>
<table><tr><td nowrap bgcolor="#dddddd">
マスター・キーを入力してください</td></tr></table>
<font color="#ff0000">$mess2</font>
<form action="$script" method=$method>
<input type=hidden name=mode value=admin_pass>
<input type=password size=8 name=pass> <input type=submit value=" IN ">
</form>

｜<a href="$script">掲示板に戻る</a>｜
</td></tr></table>
</center>
</body>
</html>
EOM
	
	#処理を終了
	exit;
}
                                                           
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃townデータの修正フォーム出力処理                        ┃
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
sub admin_form{

	#不正処理後に戻ってきた時の場合を想定して
	#ロックを解除しておく
	if($lock_check){&unlock;}
	
##データを取得
	
	#townデータファイルを開く
	open (IN,"$rankfile");
	
	#データを配列に代入
	@lines = <IN>;
	
	#ファイルを閉じる
	close (IN);

 &head_html("街管理事務所");

	#ヒアドキュメント
	print <<"EOM";
<center>
<table border=0  bgcolor="$mess_color">
<tr><td align=center valign=middle>
<table border=0>
	<tr>
	<!---# change #11--->
		<td align=center colspan=5 bgcolor="#dddddd" nowrap>その家を<b>削除する</b>場合は、<b>チェックを入れて</b>編集をクリック。<br>データを<b>編集するだけ</b>なら、<b>チェックを入れずに</b>編集をクリック。<br><b>カウント</b>は<b>半角数字</b>で指定してください。<br>その家にある<b>置き手紙</b>を削除したければ<br>置き手紙の編集をクリックし、削除フォームへ。</td>
	</tr>
	<tr><td colspan=5 align=center><p><br>｜<a href="$script">掲示板に戻る</a>｜<br><br></td></tr>
	<tr><td colspan=5 align=center><p><font color="#ff0000">$mess</font></p></td></tr>
	<tr>
		<td nowrap align=center>削除</td>
		<td nowrap align=center>名前</td>
		<td nowrap align=center>カウント</td>
		<td nowrap align=center><br></td>
		<td nowrap align=center><br></td>
	</tr>

EOM

	#データの分析・出力
	foreach $line (@lines){
	
		($name,$juu,$hyaku,$xx,$xx,$xx,$xx) = split (/<>/,$line);
		
		#カウントのフォーマット
		$cnt= $hyaku * 100 + $juu;
		
		#ヒアドキュメント
		print <<"EOM";
<tr>
<form action="$script" method=$method>
<input type=hidden name=mode value="admin_write">
<input type=hidden name=bname value="$name">
<input type=hidden name=pass value="$masterkey">
<td align=center><input type=checkbox name="del" value="yes"></td>
<td align=center><input type=text size=20 name="name" value="$name"></td>
<td align=center><input type=text size=4 name="cnt" value="$cnt"></td>
<td align=center><input type=submit value="編集"></td>
</form>
<form action="$script" method=$method>
<input type=hidden name=mode value="res_clear_form">
<input type=hidden name=owner value="$name">
<td aling=center><input type=submit value="置き手紙の編集"></td>
</form>
</tr>
EOM
	}
	
	#ヒアドキュメント
	print <<"EOM";
</table>
</td></tr></table>
</center>
</body>
</html>
EOM

	#処理を終了
	exit;
}
                                                           
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃townデータ修正処理                                      ┃
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
sub admin_write{                                           

	if($pass ne "$masterkey"){
		&error("不正なアクセスです");
	}
	
	#二重処理を回避するために、ロック処理をする。
	if($lock_check){&lock;}

##データ取得処理

	#townデータファイルを開く
	open (IN,"$rankfile");
	
	#データを配列に代入
	@lines = <IN>;
	
	#ファイルを閉じる
	close(IN);

##カウントの指定文字のチェック

	#カウント編集時、全角数字が使われていたら
	if ($cnt =~ /\D/){
	
		#注意メッセージ取得
		$mess= "カウントは半角数字で指定してください";
		
		#処理を中断
		&admin_form;
	}
	
##位上げ処理

	#百以上の位の変数の指定
	$hyaku = 0;
	
	#カウント指定が100を越えていたら
	if ($cnt > 100){
	
		#100を越えている間
		while($cnt > 100){
		
			#100を引いて
			$cnt = $cnt - 100;
			
			#百以上の位を指定する変数をアップ
			#位上げ処理
			++$hyaku;
		}
	}

	#100以下の値を取得
	$juu = $cnt;
	

##データ更新処理
	
	#更新データを入れる配列の指定
	@news = ();
	
	#データ分析
	foreach $line (@lines){
		($pname,$pjuu,$phyaku,$purl,$psec,$ppass,$pmflag)=split(/<>/,$line);
		
		$pmflag=~ s/\n//g;
		$psec =~ s/\n//g;
		$ppass=~ s/\n//g;
		
		#修正するものなら（名前で判断）
		if ($pname eq $bname){
			
			#削除でなければ
			unless ($del eq "yes"){
				
				#名前の変更がある場合
				if ($bname ne "$name"){
				
					##二重指定を回避する処理
					
					#データを分析
					foreach (@lines){
						($pn,$x,$x,$x,$x,$x,$x) = split(/<>/,$_);
					
						#二重指定の場合
						if ($pn eq "$name"){
						
							#注意メッセージを取得
							$mess = "<b>$name</b>は既に使われています";
							
							#処理を中断
							&admin_form;
						}
					}
					
					#データのフォーマット
					$new = "$name<>$juu<>$hyaku<>$purl<>$psec<>$ppass<>$pmflag\n";
					
					#更新データを配列に追加
					push (@news,$new);
				
				#名前に変更が無い場合
				}else{
				
					#データのフォーマット
					$new = "$pname<>$juu<>$hyaku<>$purl<>$psec<>$ppass<>$pmflag\n";
				
					#更新データを配列に追加
					push (@news,$new);
				}
			}
		
		#修正しないものは
		}else{
		
		#データを配列に追加
		push(@news,$line);
		}
	
	}

	#更新用にデータファイルを開く
	open (OUT,">$rankfile") || &error("$rankfileが開けませんでした");
	
	#書きこみ
	print OUT @news;
	
	#ファイルを閉じる
	close (OUT);


	#以上、ログの更新作業が終了したので、ロックを解除する。
	if($lock_check){&unlock;}

	#管理用修正フォームに戻る
	&admin_form;
}
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛



#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃管理者レス入力フォーム                                  ┃
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
sub admin_res_form{

##記事データ取得処理
	
	#記事ログファイルを開く
	open (IN,"$logfile") || &error("$logfileが開けませんでした");
	
	#データを配列に代入する。
	@lines = <IN>;
	
	#ファイルを閉じる
	close (IN);
	
	#データを分析
	foreach $line (@lines){
		
		#データを各要素に分割
		@datas = split (/<>/,$line);
		
		#レスを付けるデータを見つける
		if ($num == $datas[0]){
		
			#レスを付けるデータを取り出す
			@ress = @datas;
			
			#分析処理を終了
			last;
		}
	}
	
	#もともとあったレス記事の改行タグを折り返しに変換
	$ress[6] =~ s/<br>/\r/g;
	
 &head_html("管理者記事管理");


	#ヒアドキュメント
	print <<"EOM";
<center>
	<table bgcolor="$mess_color">
		<tr>
			<td align=center>
				<table width=400 cellspacing=0 cellpadding=4>
					<tr>
						<td align=center bgcolor="#dddddd">管理者記事管理<br>選択した記事を削除するか、レスを付けるかを選択してください。</td>
					</tr>
					<form action="$script" method="$method">
					<input type="hidden" name="mode" value="admin_clear">
					<input type="hidden" name="num" value="$num">
					<input type="hidden" name="pass" value="$masterkey">
					<tr>
						<td align=center>｜<a href="$script?">掲示板に戻る</a>｜</td>
					</tr>
					<tr>
						<td align=center><input type=submit value="-----削除する-----"></td>
					</tr>
					</form>
					<tr>
						<td><hr size=1></td>
					</tr>
					<tr>
						<td valign=top>
							[$ress[0]] $ress[4] || $ress[1] $ress[7]<br>
							<ul>
								$ress[5]
							</ul>
						</td>
					</tr>
					<form action="$script" method="$method">
					<input type="hidden" name="mode" value="admin_res_write">
					<input type="hidden" name="num" value="$num">
					<input type="hidden" name="pass" value="$masterkey">
					<tr>
						<td align=center>
							<textarea name="res" wrap="$wrap" cols=40 rows=4>$ress[6]</textarea>
						</td>
					</tr>
					<tr>
						<td align=center>
							<input type=submit value="-----レスを付ける-----">
						</td>
					</tr>
				</table>
			</td>
		</tr>
	</table>
	</center>
</body>
</html>
EOM

	#処理を終了
	exit;
}
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃管理者レス書きこみ処理                                  ┃
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
sub admin_res_write{
	
	if($pass ne "$masterkey"){
		&error("不正なアクセスです");
	}
	
	#ログファイルを開く
	open (IN,"$logfile") || &error("$logfileが開けませんでした");
	
	#データを取得
	@lines = <IN>;
	
	#ファイルを閉じる
	close (IN);
	
	#更新するデータを入れる配列を指定
	@news = ();
	
	#データを分析
	foreach $line (@lines){
	
		#データを各要素に分解
		@datas = split(/<>/,$line);
		
		#レスを付けるデータを見つける
		if ($num == $datas[0]){
		
			#新しいレスを代入
			$datas[6] = $res;
			
			#新しいデータにフォーマット
			$line = join ("<>",@datas);
		}
		
		#データを更新するデータ配列に代入
		push (@news,$line);
	}
	
	#ログファイルを上書き用に開く
	open (OUT,">$logfile") || &error("$logfileが開けませんでした");
	
	#データを書きこみ
	print OUT @news;
	
	#ファイルを閉じる
	close (OUT);
	
	#パスワードを初期化
	$FORM{'pass'} = "";
	
	&html;
}
                                                          
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃私書箱表示処理                                          ┃
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
sub res_html{                                              
	
	#エラーメッセージを持っていたら、それを代入
	if($_[1] eq "res_html"){$mess = $_[0];}
	
	#ログの更新処理などの途中であった場合を想定して、ロックを解除する。
	if($lock_check){&unlock;}

	#クッキーを取得
	&get_cookie;
	
	#資産価値を計算
	#現実味を持たせるため、
	#カウントに976万をかける
	$nedan = $count * 976;
	
	&head_html("$ownerさんの私書箱");

	print <<"EOM";
<center>
<table width=370 bgcolor="#99ccff">
<tr><td align=center>
<br>
<table width=350 border=1 bgcolor="#ffcccc" bordercolor="#000000" cellpadding=2>
<tr>
	<td width=200 rowspan=3 align=center valign=middle><img src="$iedir\/$ie\.gif"></td>
	<!---# change #12--->
	<td width=150 align=left><b>$owner</b>さんのお宅</td>
</tr>
<tr>
EOM
	if($url){
		print "<td width=150 align=left>住所：<a href=\"http\:\/\/$url\" target=_blank>ここ</a></td>\n";
	}else{
		print "<td width=150 align=left>住所：不定</td>\n";
	}
	print <<"EOM";
</tr>
<tr><!---# change #13--->
	<td width=150 align=left>資産価値：$nedan万円</td>
</tr>
</table>
<br>
EOM
	if ($oki_win_check){
		print "| <a href=\"JavaScript:window.close()\">閉じる</a> |";
	}else{
		print "| <a href=\"$script?\">掲示板に戻る</a> |";
	}
	print <<"EOM";
<br>
<br>
<table width=350 border=0>
<form action="$script" method=$method>
<input type=hidden name=mode value=res_write>
<input type=hidden name=owner value="$owner">
<input type=hidden name=ie value="$ie">
<input type=hidden name=url value="$url">
<input type=hidden name=count value="$count">
<tr>
	<td width=350 align=center valign=bottom><b>$owner</b>さんに置き手紙を残すためのフォーム<br><br></td>
</tr>
<tr>
	<td width=350 align=center valign=bottom>
		<b>お名前：</b><input type=text name=name size=20 value="$cookie{'cname'}">
		<input type=submit value="---write---">
	</td>
</tr>
<tr>
	<td width=350 align=right valign=bottom><textarea cols=45 rows=3 name=res></textarea>
</tr>
<tr>
	<td width=350 align=center><input type=radio name=color value=000000 checked><font color="#000000">■</font>
EOM
		foreach (@res_colors){
			print "<input type=radio name=color value=$_><font color=\"\#$_\">■</font>\n";
		}
		print <<"EOM";
	</td>
</tr>
</form>
EOM
		if ($oki_pass_check){
		print <<"EOM";
<tr>
	<form action="$script" method=$method>
	<td width=350 align=center>
	<input type=hidden name=mode value=res_pass>
	<input type=hidden name=owner value="$owner">
	<input type=hidden name=ie value="$ie">
	<input type=hidden name=url value="$url">
	<input type=hidden name=count value="$count">
	<br><br>
	自分宛ての置き手紙を見るときは下のフォームにkeyを…<br>
	key：<input type=password name=pass size=8 maxlength=8 value="$cookie{'cpass'}"><input type=submit value="--look--">
	</td>
</tr>
EOM
		}
		print <<"EOM";
</form>
</table>

<br>
<font color="$uemess_color">$mess</font>
<br>
<hr size=1 width=350>

EOM
	if ($oki_pass_check == "0" || $oki_pass eq "ok"){
	
		&mail_flag("$owner","0");
		
		#私書箱データファイルを開く
		open (IN,"$res_file") || &error("$res_fileが開けませんでした");
	
		#データを配列に代入
		@lines = <IN>;
	
		#ファイルを閉じる
		close (IN);

		#rankデータファイルを開く
		open (IN,"$rankfile") || &error("$rankfileが開けませんでした。");
	
		#データの各行を変数に代入
		@datas = <IN>;
		
		#データファイルを閉じる
		close (IN);

		#置き手紙の数を数える変数
		$rescnt=0;
	
		#各データを分析
		foreach $line (@lines){
		
			#データを分解
			($ownerr,$guest,$res,$sec,$color) = split(/<>/,$line);
		
			#家の持ち主のデータのみ取り出す。
			if ($owner eq "$ownerr"){
			
				#置き手紙の数をカウント
				++$rescnt;
			
				#置き手紙の数が最大数をこえたら読みこみ終了
				if ($rescnt > $resmax){last;}
			
				#日時を拾得
				&ktown_time;
			
				#色の改行を削除
				$color =~ s/\n//g;
			
				#ヒアドキュメント
				print <<"EOM";
<table cellpadding=0 cellspacing=0 border=0>
	<tr>
		<td align=left valign=top width=10 height=10><img src="$hu"></td>
		<td bgcolor="#ffffff" width=320 height=10><img src="$spacer" width=300 height=1></td>
		<td align=right valign=top width=10 height=10><img src="$mu"></td>
	</tr>
	<tr>
		<td bgcolor="#ffffff" width=10><img src="$spacer" width=10 height=1></td>
		<td bgcolor="#ffffff" width=320>
		<font color="\#$color">$res</font>
		<p align=right>
EOM
				$resflag = 0;
				foreach(@datas){
					@resdatas = split(/<>/,$_);
					if($guest eq "$resdatas[0]"){
						$resflag = 1;
						last;
					}
				}
				
				if($resflag){
					$resdatas_ie = &ie_size($resdatas[1]);
					@en_resdatas = &url_encode(@resdatas);
					print "<a href=\"$script?mode=res_html&owner=$en_resdatas[0]&url=$en_resdatas[3]&count=$resdatas[1]&ie=$resdatas_ie\">$guest</a> ";
				}else{
					print "$guest ";
				}
				
				print <<"EOM";
|| $rdate</p></td>
		<td bgcolor="#ffffff" width=10><img src="$spacer" width=10 height=1></td>
	</tr>
	<tr>
		<td width=10 height=10 align=right valign=bottom><img src="$hs"></td>
		<td bgcolor="#ffffff" width=320 height=10><img src="$spacer" width=300 height=1></td>
		<td width=10 height=10 align=left valign=bottom><img src="$ms"></td>
	</tr> 
</table>
<br>
EOM
			}
		}
		if ($rescnt == 0){
			print "<font color=\"uemess_color\"</font>置き手紙は御預かりしておりません</font><br><br>";
		}
	}
	#ヒアドキュメント
	print <<"EOM";
</td>
</tr>
</table>
</center>
</body>
</html>
EOM
	
	#処理を終了
	exit;
}                                                          
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛


#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃私書箱データの書きこみ処理                              ┃
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
sub res_write{


##二重処理回避処理

	#二重処理を回避するために、ロック処理をする。
	if($lock_check){&lock;}
	
##ログファイルデータを取得する処理

	#ログファイルを開く
	open (IN,"$res_file") || &error("$res_fileが開けませんでした。");

	#各行を配列に代入
	@lines = <IN>;
	
	#ファイルを閉じる
	close(IN);

##二重投稿回避処理

	#直前の投稿データだけを取り出す。
	@bline = split(/<>/,$lines[0]);
	
	#以下、sub decodeから受け取った変数の値を使う
	
	#直前のデータのコメントと全く一緒だった時は、
	#二重投稿を禁止する旨のエラーメッセージを表示
	if ($res eq "$bline[2]"){&res_html("$mess_onaji","res_html");}

	#コメントが書かれていなかったときは、
	#白紙投稿を禁止する旨のメッセージを表示。
	if ($res eq ""){&res_html("$mess_nashi","res_html");}

	#名前がなければ、
	#その旨のメッセージを表示
	unless($name){&res_html("名前を記入してください","res_html");}


##投稿記事に関する情報を取得する。

	#$second に日付を代入
	&get_time;

##新着記事をログファイルに保存する処理

	#新投稿記事を保存形式に整理して、$newの値とする。
	$new = "$owner<>$name<>$res<>$second<>$color\n";

	#新投稿記事をログ配列の先頭に追加
	unshift (@lines,$new);

##保存記事数の処理
	#総記事数を取得
	$kiji = @lines;

	#最大記事保存数・総記事数を０から始まる行数にするため、マイナス１する
	$dmax = $reslog_max -1;
	$dkiji= $kiji -1;

	#logfileに書き出す記事を入れる配列を指定
	@news  =();

	#保存する行数分だけ、配列@newsに代入
	foreach (0 .. $dmax){
		push(@news,$lines[$_]);
	}

	#表示される記事をあらためて、$logfileに書きこむ。
	open (OUT,">$res_file") || &error("$res_fileがひらけませんでした。");
	print OUT @news;
	close(OUT);

##次の処理を許可する

	#ログの更新処理が終了したので、ロックを解除する
	if($lock_check){&unlock;}
	
	&mail_flag("$owner","1");

	$mess = "御手紙確かに受け取りました。";

	#私書箱表示処理へ
	&res_html;

}
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛


#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃私書箱記事を削除するフォーム表示処理                    ┃
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
sub res_clear_form{

	#不正処理後に戻ってきた時の場合を想定して
	#ロックを解除しておく
	if($lock_check){&unlock;}
	
##データを取得
	
	#townデータファイルを開く
	open (IN,"$res_file");
	
	#データを配列に代入
	@lines = <IN>;
	
	#ファイルを閉じる
	close (IN);
	
##html出力処理

 &head_html("私書箱削除フォーム");

	#ヒアドキュメント
	print <<"EOM";
<center>
<table border=0  bgcolor="$mess_color">
<tr><td align=center valign=middle>
<table border=0>
	<tr>
		<td align=center colspan=3 bgcolor="#dddddd" nowrap>削除する記事にチェックを入れ、削除をクリックしてください。</td>
	</tr>
	<tr><td colspan=3 align=center><p><br>｜<a href="$script">掲示板に戻る</a>｜<br><br></td></tr>
	<tr><td colspan=3 align=center><p><font color="#ff0000">$mess</font></p></td></tr>
	<tr><td colspan=3 align=center><p><b>$owner</b>への置き手紙を編集する</p></td></tr>

EOM

	$cnt = 0;
	
	#データの分析・出力
	foreach $line (@lines){
	
		($rowner,$rguest,$rres,$rsec,$xx) = split (/<>/,$line);
		
		if ($owner eq "$rowner"){
			
		#ヒアドキュメント
		print <<"EOM";
<form action="$script" method=$method>
<tr>
<input type=hidden name=mode value="res_clear">
<input type=hidden name=owner value="$rowner">
<input type=hidden name=sec value=$rsec>
<td align=center valign=middle><input type=checkbox name="del" value="yes"></td>
<td align=left bgcolor="#ffffff" width=300>$rres<br><p align=right>from $rguest</p></td>
<td align=center><input type=submit value="削除"></td>
</form>
</tr>
EOM
		}
	}
	
	#ヒアドキュメント
	print <<"EOM";
</table>
</td></tr></table>
</center>
</body>
</html>
EOM

	#処理を終了
	exit;
}
                                                           
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃私書箱データを削除する処理                              ┃
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
sub res_clear{                                             

	#ログを更新するため、ロック処理する。
	if($lock_check){&lock;}
	
	#私書箱データファイルを開く
	open (IN,"$res_file") || &error("$res_fileが開けませんでした");
	
	#データを読み込む
	@lines = <IN>;
	
	#ファイルを閉じる
	close (IN);
	
	#更新するデータを入れる配列を指定
	@news = ();
	
	#データを個別に分析
	foreach $line (@lines){
	
		#データを要素に分解
		@datas = split (/<>/,$line);
		
		#削除対象記事でなければ
		unless ("$del" eq "yes" && "$owner" eq "$datas[0]" && "$sec" eq "$datas[3]"){
			
			#更新データ配列の最後に追加
			push (@news,$line);
		}
	}
	
	#私書箱データファイルを上書き用に開く
	open (OUT,">$res_file") || &error("$res_fileが開けませんでした");
	
	#データを更新する
	print OUT @news;
	
	#ファイルを閉じる
	close (OUT);
	
	#以上、ログの更新作業が終了したので、ロックを解除する。
	if($lock_check){&unlock;}
	
	#私書箱削除フォーム表示処理へ
	&res_clear_form;
}                                                          
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃置き手紙パスワード照合処理                              ┃
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
sub res_pass{
	
	#ランクファイルを開く
	open (IN,"$rankfile") || &error("$rankfileが開けませんでした");
	
	#データを配列に代入
	@shishos = <IN>;
	
	#ファイルを閉じる
	close (IN);
	
	foreach(@shishos){
		@datas = split(/<>/,$_);
		if($owner eq $datas[0]){



			$pass_t = $datas[5];

			last;
		}
	}
	
	
	#sub decodeから送られてきた、$passと、ポストに設定されていたキー$pass_tが一致するかどうかを
	#sub match_passで処理して、その結果を$oki_passに代入する。
	$oki_pass = &match_pass("$pass","$pass_t");
	
	#もしも、$pass_tが設定されていなかったのなら（削除キーが設定されていなかったら）
	if ($pass_t eq ""){
	
		#だれでも見れるように、okをかえす。
		$oki_pass = "ok";
		
		#その旨のメッセージを表示
		$mess = "メイン掲示板でkeyを入力してね、他の人にもみられちゃうよ。";
	}
	
	#もしも、キーが違ったら
	if ($oki_pass ne "ok"){
	
		#覗き見しちゃだめという旨のメッセージを表示
		$mess = "のぞいちゃだめ！！";
	}
	
	#置き手紙表示処理へ
	&res_html;
}                                                          
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃アクセスチェック処理                                    ┃
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
sub access_deny{

	#排除ホスト候補があれば、
	if ($deny_list[0]) {
	
		# ホスト名を取得
		&get_host;
		
		#チェック印
		$flag_deny = 0;
		
		#排除リストを１つづつ
		foreach (@deny_list) {
		
			#空になったら、終わり
			if ($_ eq '') { 
				last;
			}
			
			#*の部分を正規表現に書きなおす
			$_ =~ s/\*/\.\*/g;
			
			#取得したホスト情報とリストが一致するか
			if ($host =~ /$_/) { 

				#印をつける
				$flag_deny = 1;
				
				#ループから脱出
				last;
			}
		}
		
		#印がついていたら
		if ($flag_deny) {
		
			# エラー表示
			&error("$access_deny_mess");
			exit;
		}
	}
}                                                          
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃ヘッダー表示処理                                        ┃
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
sub head_html{
	
	#ページタイトル取得
	local($t) = @_[0];

	#html出力宣言
	print "Content-type: text/html\n\n";
	
	#ヒアドキュメント
	print <<"EOM";
<html lang="ja">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>$t</title>
<meta http-equiv="Content-Style-Type" content="text/css">
<style type="text/css">
<!--
a:link    {text-decoration:none;    color:$link; }
a:visited {text-decoration:none;    color:$vlink; }
a:active  {text-decoration:none;    color:$alink; }
a:hover   {text-decoration:underline;    color:$alink; }
table     {font-size:12px; }
.title    {font-size:18px; }
-->
</style>
</head>
EOM

	#背景画像があれば、
	if ($bg_gif){
		print "<body bgcolor=\"$bg_color\" background=\"$bg_gif\" text=\"$text_color\" link=\"$link\" alink=\"$alink\" vlink=\"$vlink\">\n";
	#背景画像がなければ、
	}else{
		print "<body bgcolor=\"$bg_color\" link=\"$link\" alink=\"$alink\" vlink=\"$vlink\" text=\"$text_color\">\n";
	}
}
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃家表示ページ処理                                        ┃
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
sub house_page_count{
	
##表示する最初の家の行数
	#値を持っていなければ
	if($FORM{'hpc'} eq ''){
	
		#0行目、最初から
		$house_start = 0;
	
	#値を持っているなら
	}else{
	
		#その行目から、
		$house_start = $FORM{'hpc'};
	}
	
	#そのページの最後の家の行数
	$house_end = $house_start + $house_num - 1;
	
	#最後の家の行数が、データ上での最後の行数以上のときは、
	if($house_end >= $#lines){
	
		#データ上での最後の行数になる
		$house_end = $#lines;
	}
	
	#次のページの最初の家の行数
	$house_next = $house_start + $house_num;
	
	#前のページの最初の家の行数
	$house_back = $house_start - $house_num;
}
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃置手紙未読チェック                                      ┃
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
sub mail_flag{
	
	($mfname,$mf) = @_;
	
	if($lock_check){&lock;}
	
	open (IN,"$rankfile");
	@lines = <IN>;
	close(IN);
	
	foreach(@lines){
		($dname,$djuu,$dhyaku,$durl,$dpsec,$dpass,$dmflag) = split(/<>/,$_);
		$dpsec =~ s/\n//g;
		$dpass =~ s/\n//g;
		$dmflag=~ s/\n//g;
		if($mfname eq "$dname"){
			$_ = "$dname<>$djuu<>$dhyaku<>$durl<>$dpsec<>$dpass<>$mf\n";
			last;
		}
	}
	
	open (OUT,">$rankfile");
	print OUT @lines;
	close (OUT);
	
	if($lock_check){&unlock;}
	
}
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛


#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃urlエンコード処理                                       ┃
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
sub url_encode{
	local(@encode_datas) = @_;
	
	foreach (@encode_datas){
	s/(\W)/'%' . unpack('H2', $1)/eg;
	s/\s/+/g;
	}
	@encode_datas;
}
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃家サイズ決定処理                                        ┃
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
sub ie_size{
	$c = $_[0];
	$size = "";

	#家アイコンの指定
	if($c == 1 ){$size = "1";}		#最初の投稿
	elsif($c <= 2){$size = "2";}		#２回目の投稿
	elsif($c <= 3){$size = "3";}		#３回目の投稿
	elsif($c <= 4){$size = "4";}		#４回目の投稿
	elsif($c <= 6){$size = "5";}		#５〜６回目の投稿
	elsif($c <= 10){$size = "6";}		#７〜１０回目の投稿
	elsif($c <= 20){$size = "7";}		#１１〜２０回目の投稿
	elsif($c <= 30){$size = "8";}		#２１〜３０回目の投稿
	elsif($c <= 40){$size = "9";}		#３１〜４０回目の投稿
	elsif($c <= 50){$size = "10";}	#４１〜５０回目の投稿
	elsif($c <= 65){$size = "11";}	#５１〜６５回目の投稿
	elsif($c <= 80){$size = "12";}	#６６〜８０回目の投稿
	elsif($c <= 99){$size = "13";}	#８１〜９９回目の投稿
	elsif($c == 100){$size = "town";}	#１００回目の投稿
	$size;
}
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃マスターキー照合処理 v12.30                             ┃
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
sub make_mpass{
	my $pass = $_[0];
	if($make_mpass_mode){
		if ($masterkey =~ /^\$1\$/){ $key=3;}
		else{ $key = 0;}
		return crypt($pass,substr($masterkey,$key,2));
	}else{
		return $pass;
	}
}
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃マスターキー暗号化処理 v12.30                           ┃
#┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
sub make_mpass_mode{                                             
	my $message;
	if($pass){
		my $mpass = &make_pass($pass);
		$message = "暗号化されたマスターキーは<br><b>$mpass</b><br>です。<br>kboard.cgiで設定してください。";
	}
		
	&head_html("暗号化処理");

print <<"EOM";
<center>
<table border=0 bgcolor="#777777" width=400 cellpadding=5>
	<tr>
		<td align=center>
			<table width=370>
				<tr>
					<td align=center bgcolor="#eeeeee"><font color="#333333">---Message---</font></td>
				</tr>
				<tr>
					<td align=center><hr size=1>暗号化したいマスターキーを入力してください<br>(英数半角8文字以内)</td>
				</tr>
				<form action="$script" method="$method">
					<input type=hidden name=mode value="make_mpass">
					<tr>
						<td align=center><input type=password name=pass size=8 maxlength=8> <input type=submit value="-暗号化-"></td>
					</tr>
				</form>
				<tr>
					<td align=center>$message</td>
				</tr>
				<tr>
					<td align=center><hr size=1>| <a href="$script?">掲示板に戻る</a> |<td>
				</tr>
				<tr>
					<td align=right>$ver <a href="http://www.kaism.com">kaism</a></td>
				</tr>
			</table>
		</td>
	</tr>
</table>
</center>
</body>
</html>
EOM
	exit;
}                                                          
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

