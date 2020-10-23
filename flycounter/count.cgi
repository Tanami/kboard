#!/usr/bin/perl
#ハムスターカウンタ(GIF+fly)▲(c)p4room(http://p4room.mda.or.jp/)
#Modified by SHIRO (http://www.kyoshin-sj.co.jp/oyama/）

$fly = "./fly";			#flyコマンド
$tmpdir = "./tmp";			#一時的にファイルを作るディレクトリ

### カウント処理

@urls = (				#アクセスを無視したいリンク元URL
  "hogehoge.net",			#カンマで区切って複数指定可能
  "oyama/page1",			#例："yahoo.co.jp",
);
$logfile = "./count.log";		#カウンタ保存用ファイル
$aclogfile ="./access.log";		#アクセス記録用ファイル
$addr      = $ENV{'REMOTE_ADDR'};	#来訪者のホストアドレス
$referer   = $ENV{'HTTP_REFERER'};	#リンク元URL
$keep      = 20;			#アクセス記録の保存期間（秒）
$now       = time;			#現在の時刻

open(FILE,"+<$aclogfile");		#アクセスログを開く
flock(FILE,2);				#ロックする
@logs = <FILE>;				#配列にアクセス記録を読み込む
@logs = grep($_ > $now - $keep, @logs); #$keep秒以内の新アクセス記録のみ残す
seek(FILE,0,0);				#ファイルポインタを先頭に
print FILE "$now\t$addr\n";		#今回のアクセス記録を書き込む
print FILE @logs;			#@logsを書き込む
truncate(FILE, tell);			#余分なデータを切り詰める
close(FILE);				#クローズ

open(FILE,"+<$logfile");		
flock(FILE,2);
chop($count = <FILE>);			#カウンタを読み込む
if (&from_outside()) {			#外部からのアクセスであり、
  if (&is_newcomer()) {			#新規訪問者によるアクセスなら
    $count++;				#カウンタを+1する
    seek(FILE,0,0);			#ファイルポインタを先頭に戻す
    print FILE "$count\n";		#カウンタをファイルに書き出す
  }
}
flock(FILE,8);				#ロック解除
close(FILE);				#クローズ

$count = sprintf("%05d", $count);	#最低5桁に整形する
@suuji = split(//, $count);		#個々の数字に分割

### flyコマンドを利用したカウンタ画像の作成

unless (-x $fly) {			#flyコマンドが実行できなければ
  print "Location: bad.gif\n\n";	#失敗画像を出力して中断
  exit;					#スクリプト終了
}

$imgfile = "$tmpdir/#$$.gif";		#一時的に作る画像ファイル名

$xsize = 16;				#個々の数字GIFの横幅
$ysize = 33;				#個々の数字GIFの高さ

open(FLY, "|$fly -q -o $imgfile");		#flyコマンドを起動
print FLY "new\n";				#初期化
print FLY "size 134,82\n";			#背景画像サイズを設定
print FLY "copy 0,0,-1,-1,-1,-1,backpic.gif\n";	#背景画像をコピー
$x = (134 - $xsize * @suuji) / 2;		#数字開始位置
foreach $n (@suuji) {
  print FLY "copy $x,60,-1,-1,-1,-1,$n.gif\n";	#数字を配置
  $x += $xsize;					#数字の幅だけ右に移動
}
print FLY "transparent 0,0,0\n";		#透明色を設定（RGB=0,0,0)
close(FLY);					#flyコマンド終了（画像作成完了）

### 画像を出力して終了

$date = &gmt_date(time);		#現在の時刻を
print "Last-Modified: $date\n";		#更新時刻として出力
print "Expires: 0\n";			#有効期限は0 (キャッシュなし)
print "Content-Type: image/gif\n\n";	#GIF画像のHTTPヘッダを出力

open(FILE, $imgfile);			#画像ファイルをオープン
print <FILE>;				#全データを出力
close(FILE);				#ファイルをクローズ

unlink($imgfile);			#画像ファイルを削除

exit;					#スクリプト終了

### 以下サブルーチン

sub from_outside {			#外部からのアクセスかどうかチェック
  foreach $url (@urls){
	  if ($referer =~ /$url/) {	#自分のページからのアクセスなら
	    return 0;			#0を返す
	  }
  }
  return 1;				#そうでなければ外部からのアクセス
}

sub is_newcomer {			#新規アクセスかどうかチェック
  foreach $line (@logs){		#$keep秒以内の全記録を調べる
	chop($line);
	($t, $a) = split(/\t/, $line);	#時刻とホストアドレスに分割
	if ($addr eq $a) {		#同じホストからのアクセス記録があれば０を返す
		return 0;
	}
  }
  return 1;				#そうでなければ1を返す
}

### 世界標準時の文字列を得る

sub gmt_date {
  local($t) = @_;
  @wdays = ("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat");
  @month = ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec");
  ($sec, $min, $hour, $day, $mon, $year, $wday) = gmtime($t);
  return sprintf("%s, %02d %s %04d %02d:%02d:%02d GMT",
           $wdays[$wday], $day, $month[$mon], $year+1900, $hour, $min, $sec);
}
