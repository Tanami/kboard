#!/usr/bin/perl

# �A�C�R���A�b�v���[�h�p�f����(^^)
# �����E�Ĕz�z��
# Copyright 1999,2000 Qz...?
#--------------------------------------------------------
# Modified by SHIRO 2001/06/08
# e-mail      s-o-yama@fa2.so-net.ne.jp
# homepage    www.kyoshin-sj.co.jp/oyama/
# KBOARD SHIRO'S VERSION �p�ɉ���
# "��p" �͎����@�\���Ă��܂���B
#--------------------------------------------------------
$| = 1;
$VER = '1.60';

#--�P�y�[�W�̕\������
$PageCount = 5;

#--���y�[�W�}�[�N�̐ݒ�
#  �摜�̎w����\�ł��B
$PrevPageMark = '<small>���O�̃y�[�W</small>';
$NextPageMark = '<small>���̃y�[�W��</small>';

#--URL�}�[�N�̐ݒ�
#  �摜�̎w����\�ł��B
$HomeMark = '[HOME]';

#--�Ǘ��җp�o�^�̂��߂̐ݒ�
$AdminName = '�Ǘ��l';               #���Ȃ��̂��Ȃ܂�
$AdminMail = 'xx@xx.xx.xx';              #���Ȃ��̃��[���A�h���X
$AdminComment = '�Ǘ��l�o�^�ł�';    #�o�^���b�Z�[�W

###################################
###�@�K�{���ڂ̐ݒ�@�@�@�@�@�@####
###################################

$JcodeLib = './jcode.pl';	#--�������C�u���� jcode.pl �̃t�@�C����
$CharCode = 'sjis';		#--�����R�[�h�i'sjis' 'euc' 'jis'�j
$addminpass = "0123";	#--�Ǘ��҃p�X���[�h(�K���ύX���Ă�������)
$ReturnBBS = "./kboard.cgi";	#--�߂��f���t�q�k
$icon_url = "gif/icon";         #Path�Ŏw�肵�Ă��������B
$IconPath = "gif/icon";

###################################
###�@�K�{���ڂ̐ݒ�̏I���@�@�@####
###################################

###################################
###�@�摜�ۑ��̓���ݒ�@�@    ####
###################################

#--�ۑ��n�j�̗e��(�P��KB, 0:������)
$MaxPicSize = 20;

#--�ۑ��n�j�̏c�T�C�Y(0:������)
$MaxPicHeight = 60;

#--�ۑ��n�j�̉��T�C�Y(0:������)
$MaxPicWidth = 60;

#--�ۑ�����(0:������)
$MaxSaveCount = 0;

#--�L���폜���̉摜�t�@�C���폜(1:�폜 0:�폜���Ȃ�)
$PicDeiMode = 1;

###################################
###�@�^�C�g���E��ʐF�̐ݒ�@�@####
###################################

#--Title�^�O�̖��O�  �^�O����ł̐ݒ�́A���Ȃ��ŉ������
$HeadTitle = "��p�A�C�R���o�^";

#--�f���^�C�g��
$TopTitle = <<'_____E_';
<Center>
<Font Color=#DD0000 Size=+2>
�A�C�R���o�^�R�[�i�[
</Font>
</Center>
_____E_
#�� _____E_ �͍폜���Ȃ��ł��������B

#--�e��F�ݒ�
$BackColor  = "#ADDEFC";			# �w�i�F���w��
$TextColor  = "#000000";			# �����F���w��
$LinkColor  = "#0000FF";			# �����N�F���w��i�������N�j
$VLinkColor = "#0000FF";			# �����N�F���w��i�������N�j
$ALinkColor = "#FF0000";			# �����N�F���w��i�����N���j

$IN_TBL_Color = "C0C0C0";			# ���͉�ʂ̃e�[�u���w�i�F
$IN_IMG_Color = "FF8040";			# ���͉�ʂ̃C���[�W���̐F

#--�w�i�摜(���w��Ȃ�A�\�����܂���)
$BackGround = "";

###############################################
###�@���p�ݒ�i�K�v�ɉ����ĕύX���ĉ������@####
###############################################

#--���̂b�f�h�̖��̂܂��͂t�q�k�  ���w��Ȃ�A�����擾
$ThisCGI = "pup.cgi";

#--�ۑ����O�t�@�C����
$SaveFile = "iconfile.log";

#--�ۑ��Z�L�����e�B�[���[�h
#  0-�N�ł��o�^�\
#  1-�p�X���[�h�ɂ�鐧��
#  2-��{�I�ɒN�ł��o�^�\�����ǁA�o�^���郊���[�g�z�X�g�ɐ�����������
$SaveMode = 0;

#--�o�^�p�p�X���[�h(�ۑ��Z�L�����e�B�[���[�h���P�̂Ƃ��ɕK�v)
$UserPass = "userpass";

#--�o�^�s�����[�g�z�X�g��(�ۑ��Z�L�����e�B�[���[�h���Q�̂Ƃ��ɕK�v)
$NGRemortHost =<<'_____E_';
a
aa
aaa
_____E_
#�� _____E_ �͍폜���Ȃ��ł��������B

#--�v���L�V��ʂ��Ă̓o�^�s��(0-OK 1-�s��)
#  ������āA���܂����삷�邩�A��:-)
$ProxyNG = 0;

#--�N�b�L�[�ɓo�^�p�p�X���[�h��ۑ�����(0:���Ȃ� 1:����)
$CookieUserPassSave = 1;

#--�N�b�L�[�ɕۑ��������
$CookieDay = 30;

#--�N�b�L�[���ʖ�
$CookieID = "pup";

#--���b�N(0:���Ȃ� 1:����)
$LockMode = 0;

#--���b�N�t�@�C����
$LockFile = "pup_lock";

###########################
###�@���p�ݒ�@�I��  �@####
###########################

#;___�ȏ�Őݒ�͏I���ł�____________________________;

#;_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
#;����
#;_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
#_�ȈՐݒ�`�F�b�N
&PrintErrHtml("$JcodeLib��������܂���B") unless(-e $JcodeLib);
&PrintErrHtml("$SaveFile��������܂���B") unless(-e $SaveFile);
&PrintErrHtml("$IconPath��������܂���B") unless(-e $IconPath);
require $JcodeLib;
#���w��Ȃ�A�����擾
unless($THIS_CGI){
	($THIS_CGI) = ($ENV{SCRIPT_NAME} || $0 ) =~ m|/([^/]+)$|;
}

#;���C������______________________________________________________________;
&FormDecord;
if($FORM{'ACTION'} eq "REGIST"){
	&ExecSave;
}elsif($FORM{'ACTION'} eq "DELETE"){
	&ExecDelete;
}else{
	&PrintLogHtml;
}
exit(0);


#;�ŏ㕔�\��______________________________________________________________;
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
<A Href="$ReturnBBS">�� �f���ɖ߂�</A>
$TopTitle
_____E_
}

#;�g�p���@�\��____________________________________________________________;
sub PrintGuidHtml
{
print <<"_____E_";
<Center>
<HR Width="80%">
<Table Width="80%">
<TR><TD>�� �A�C�R��(�摜�t�@�C��)���Q�X�g�̕��̃p\�\\�R\��\���璼�ځA�f���̃T�[�o�ɓo�^�o���܂��B</TD></TR>
<TR><TD>�� �o�^�ł���摜�́AJpeg�摜�AGIF�摜�APNG�摜�݂̂ƂȂ��Ă���܂��B</TD></TR>
<TR><TD>�� �摜�́A�t�@�C���T�C�Y�F$MaxPicSize Kbyte�A���F$MaxPicWidth �w�c�F$MaxPicHeight �ȓ��̂��̂��o�^�ł��܂��B</TD></TR>
<TR><TD>�� ���쌠�Ȃǂ��l�����āA���̂Ȃ��摜��o�^���Ă��������B</TD></TR>
<TR><TD>�� NetScape Navigater 3�ȏ�AInternet Explorler 4�ȏ�̕������A�����p�ł��܂���B</TD></TR>
<TR><TD>�� Internet Explorler 3.0 �����g���̕��́A�ȉ��̂t�q�k����v���O�C��������ł��܂��B</TD></TR>
<TR><TD Align=Center><a href="http://www.microsoft.com/ie_intl/ja/download/ie3add.htm">http://www.microsoft.com/ie_intl/ja/download/ie3add.htm</A></TD></TR>
</Table>
<HR Width="80%">
</Center>
_____E_
}

#;�o�^�ł��Ȃ���`���b�Z�[�W���\��__________________________________________;
sub PrintNoRegist
{ #���b�Z�[�W�͂��Ȃ肢�������H
print <<"_____E_";
<center>
<p><em>
�A�C�R���o�^�������A$MaxSaveCount���ɁA���B�����̂ŁA
���݁A�A�C�R���̓o�^�́A�ł��܂���B
</em><p>
</center>
_____E_
}

#;�ŉ����\���i���쌠�\���A�폜�s�I�j______________________________________;
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

#;�G���[�\��______________________________________________________________;
sub PrintErrHtml
{
	&FileUnLock if($LOCK_SW);
	&PrintTopHtml;
	print "<Table Width=\"100%\" Height=\"80%\"><TR><TD Align=Center Valign=Center>\n";
	print "<Table Width=400 Border=1>\n";
	print "<TR><TD Align=Center><B>�G���[</B></TD></TR>\n";
	print "<TR><TD Height=200 VAlign=Center Align=Center>\n";
	print $_[0];
	print "\n</TD></TR>\n";
	print "<TR><TD Align=Center>�u���E�U�̖߂�{�^���ł��߂肭�������B\n";
	print "\n</TD></TR></Table>\n";
	print "\n</TD></TR></Table>\n";
	&PrintBottomHtml;
	exit(0);
}

#;���O�\������____________________________________________________________;
sub PrintLogHtml
{
	#;�N�b�L�[�擾
	&GetCookie;

	#;���O�Ǎ�
	open(IN,"$SaveFile") || &PrintErrHtml("�ۑ��t�@�C���̓ǂݍ��݂Ɏ��s���܂����B<BR>����:$!");

	#���O�̌����𐔂���
	local($lcnt)= 0;
	$lcnt++ while(<IN>);
	
	&PrintTopHtml;

	if(($MaxSaveCount > 0) && ($MaxSaveCount <= $lcnt)){
		#�ۑ��������ő�ۑ��������傫���̂ŁA
		#�o�^�ł��Ȃ��悤�ɂ���
		
		#�o�^�ł��Ȃ����̕\��
		&PrintNoRegist;
		
	}else{

		#;���e�t�H�[���\��
		&PrintRegistForm;
	
		#;�������̕\��
		&PrintGuidHtml;
	}

	#���O�������߂�
	seek(IN, 0, 0);

	#;�L���ꗗ�\��
	print "<Form Action=\"$ThisCGI\" Method=\"POST\">\n";
	print "<Input Type=\"Hidden\" Name=\"ACTION\" Value=\"DELETE\">\n";
	print "<Center>\n";

	local($cnt) = 0;
	local($start_cnt) = $PageCount * $FORM{'PAGE'}; #�J�n�ʒu
	local($end_cnt)   = $start_cnt + $PageCount;    #�I���ʒu

	while(<IN>){
		next if($start_cnt > $cnt++);
		last if($end_cnt   < $cnt);
		
		($pfn, $ptitle, $ptime, $ppwd, $pno, $pdate, $pname, $pmail, $pmsg,
			$phost, $pw, $ph, $ptype, $plen, $progname, $purl, $only
		)= split(/\,/, $_);
		$LinkNmae = "<A Href=\"mailto:$pmail\">$pname</A>";
		if ($purl) { $LinkURL  = "<A Href=\"http://$purl\">$HomeMark</A>"; 
		}else 	   { $LinkURL  = ""; }
		if ($only) { $only = "�i$pname��p�j"; 
		}else	   { $only = "�i���p�A�C�R���j"; }
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
<TR><TD ColSpan=2> �o�^�ҁF$LinkNmae<Small> �o�^���F$pdate $LinkURL</Small></TD></TR>
<TR><TD ColSpan=2>�R�����g��$pmsg</TD></TR>
</Table></TR></TD></Table><BR>
<!-- _____________________________________________________ -->
_____E_
	} #-- end of loop

	close(IN); #�����ŁA�t�@�C�������

	#�y�[�W�{�^��
	#   ���C�A�E�g�I�ɂ����ł����̂��ȁE�E�E
	#  ���Ȃ݂ɁAqq �́A" �̑���Ɏg�p�ł�����̂ł��B
	#  "�ł����܂ꂽ���ɁA" ������ꍇ�A\ �������ɂ��ނ̂ŕ֗�
	#  q ���������̂Ƃ��́A' �̑���ɂ�����
	#  qq() ��Aqq!! q// �Ȃǂ̂悤�Ɏg�p���܂��B
	#  qq �̎��̕����ŁA�Ȃ��̕������͂߂܂��B
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
	print "<Small>�o�^�L�[�F</Small>\n";
	print "<Input Type=\"PassWord\" Size=10 Name=\"DELKEY\" Value=\"$COOKIE{'MYPWD'}\">\n";
	print "<Input Type=\"Submit\" Value=\"�폜\">\n";
	print "</TD></TR></Table></Form></Center>\n";

	&PrintBottomHtml;
}

#;���e�t�H�[���\��________________________________________________________;
#���L�̃t�H�[������1�s�폜
#<Input Type="Hidden" Name="ADMIN" Value="MATOME">
#if("ADMIN"=="MATOME"){$FORM{'ADMIN'} = 'MATOME'} �ǉ�����ꏊ�H

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
<TD Bgcolor=$IN_IMG_Color>�o�^�p�p�X���[�h</TD>
<TD Bgcolor=$IN_IMG_Color><Input Type="Password" Name="WRITEPASS" Size=20" Value="$COOKIE{'WRITEPASS'}"></TD>
</TR>
_____E_
} #-- end of if

print <<"_____E_";
<TR>
<TD Bgcolor=$IN_IMG_Color>�摜�^�C�g��</TD>
<TD Bgcolor=$IN_IMG_Color><Input Type="Text" Name="TITLE" Size=30 Maxlength=50">���C�x�߂ł����A������p�ɂ��������͌���(��p)�ƕt���ĉ������</TD>
</TR>
<TR>
<TD Bgcolor=$IN_IMG_Color>�摜�I��</TD>
<TD Bgcolor=$IN_IMG_Color><Input Type="FILE" Name="IMG" Size=50></TD>
</TR>
_____E_

if($FORM{'ADMIN'} ne 'MATOME'){
print <<"_____E_";
<TR>
<TD Bgcolor=$IN_TBL_Color>���Ȃ܂�</TD>
<TD Bgcolor=$IN_TBL_Color><Input Type="Text" Name="NAME" Size=25 Maxlength=50 Value="$COOKIE{'NAME'}">
</TD>
</TR>
<TR>
<TD Bgcolor=$IN_TBL_Color>�d�|��������</TD>
<TD Bgcolor=$IN_TBL_Color><Input Type="Text" Name="EMAIL" Size=40 Maxlength=40 Value="$COOKIE{'EMAIL'}"></TD>
</TR>
<TR>
<TD Bgcolor=$IN_TBL_Color>�g�������o������</TD>
<TD Bgcolor=$IN_TBL_Color><Input Type="Text" Name="HPURL" Size=60 Maxlength=60 Value="http://$COOKIE{'HPURL'}"></TD>
</TR>
<TR>
<TD Bgcolor=$IN_TBL_Color>�R�����g</TD>
<TD Bgcolor=$IN_TBL_Color><Input Type="Text" Name="MESSAGE" Size=80 Maxlength=100></TD>
</TR>
_____E_
} #-- end of if

print <<"_____E_";
<TR>
<TD Bgcolor=$IN_TBL_Color>�o�^�L�[</TD>
<TD Bgcolor=$IN_TBL_Color><Input Type="Password" Name="MYPWD" Size=10 Maxlength=10 Value="$COOKIE{'MYPWD'}">
<Input Type="Checkbox" Name="COOKIE" $CookieChecked>���̏�����������p����B
</TD>
</TR>
</Table>
<BR>
<Input Type="Submit" Value="--�o�^���s--">
<Input Type="Reset" Value="�N���A">
</Form>
</Center>
_____E_
}

#;�o�^����________________________________________________________________;
sub ExecSave
{
	if($FORM{'ADMIN'} eq 'MATOME'){
		if($FORM{'MYPWD'} ne $addminpass){
			&PrintErrHtml('�p�X���[�h���Ⴂ�܂��B');
		}else{
			$FORM{'NAME'} = $AdminName;
			$FORM{'MESSAGE'} = $AdminComment;
			$FORM{'EMAIL'} =$AdminMail;
		}
	}

	#;�ȈՃZ�L�����e�B�`�F�b�N
	&SeculityCheck;

	#;�����̓`�F�b�N

	&PrintErrHtml("�摜�^�C�g���������͂ł��B") unless($FORM{'TITLE'});

	if($FORM{'ADMIN'} ne 'MATOME'){
		&PrintErrHtml("���Ȃ܂��������͂ł��B") unless($FORM{'NAME'});
		&PrintErrHtml("���[���A�h���X�������͂ł��B") unless($FORM{'EMAIL'});
		&PrintErrHtml("�s���ȃ��[���A�h���X�ł��B") if(!($FORM{'EMAIL'} =~ /[-A-Za-z0-9.]+@[-a-z0-9.]+/));
		&PrintErrHtml("�R�����g�������͂ł��B") unless($FORM{'MESSAGE'});
	}
	&PrintErrHtml("�o�^�p�X���[�h�������͂ł��B") unless($FORM{'MYPWD'});

	#;�����擾
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

	#;���b�N�J�n
	&OpenFileLock;

	#;���O�Ǎ�
	open(IN,"$SaveFile") || &PrintErrHtml("�ۑ��t�@�C���̓ǂݍ��݂Ɏ��s���܂����B<BR>����:$!");
	@LINES = <IN>;
	close(IN);

	#;�Q�d�o�^�`�F�b�N
	foreach(@LINES){
		($pfn, $ptitle) = split(/\,/, $_);
		&PrintErrHtml("���̉摜���̂͂��łɓo�^����Ă��܂��B") if($ptitle eq $FORM{'TITLE'});
	}

	#;�摜�ۑ�
	&SaveBinFile;

	#;�Ō�̋L���̔ԍ����擾���P���Z
	($pfn, $ptitle, $ptime, $ppwd, $pno) = split(/\,/, $LINES[0]);
	$No = $pno + 1;

	#;�p�X���[�h�Í���
	$EncodePass = &EnCodeKey($FORM{'MYPWD'});
	
	#;�摜�t�@�C���l�[���ȑf��  ### Add by Season
	$PicFile = $FILE_NAME{'IMG'};
	$PicFile =~ /([^\\\/]+$)/;
	$PicFile = $1;
	
	#;�t�q�k�t�H�[�}�b�g  ### Add by Season
	$HPURL  = $FORM{'HPURL'};
	$HPURL  =~ s/^http\:\/\///;
	$HPURL  =~ s/\r//g;
	$HPURL  =~ s/\n//g;

	#�J���}( , )���͑΍�(������` by Q)
	$FORM{'TITLE'}   =~ s/\,/�A/g;
	$FORM{'NAME'}    =~ s/\,/�A/g;
	$FORM{'EMAIL'}   =~ s/\,/�A/g;
	$FORM{'MESSAGE'} =~ s/\,/�A/g;
	$HPURL           =~ s/\,/�A/g;
	#���Ԃ�A���̓t�H�[���͈ȏゾ�Ƃ������E�E�E����(^^;;
	#�ɂ��Ă��A�Ȃ�ŁA�f�[�^�̋�؂�ɁA�J���}���������񂾂낤�H
	#�����������Ƃ����������Ȃ��E�E�E

	#;�f�[�^�t�H�[�}�b�g��
	$NewLine = join("\,", $PicName, $FORM{'TITLE'}, $GTime, $EncodePass, $No, 
				$DateFormat, $FORM{'NAME'}, $FORM{'EMAIL'}, $FORM{'MESSAGE'},
				$Host, $PicWidth, $PicHeight, $PicType, $PicLen, $PicFile, 
				$HPURL, $FORM{'Only'}, 
				"\n"
			);

	#;���{�R�[�h�ϊ�&�^�O�̏���
	&jcode'convert(*NewLine, $CharCode);
	$NewLine =~ s/</&lt;/g;
	$NewLine =~ s/>/&gt;/g;

	#;�ۑ���������
	@LINES = ($NewLine, @LINES);
	if(($MaxSaveCount > 0) && ($MaxSaveCount < @LINES)){
		@DEL_ITEM = splice(@LINES, $MaxSaveCount);
		&DelIcon if($PicDeiMode);
	}

	#;���O����
	open(OUT,">$SaveFile") || &PrintErrHtml("�ۑ��t�@�C���̏������݂Ɏ��s���܂����B<BR>����:$!");
	print OUT @LINES;
	close(OUT);

	#;���b�N����
	&FileUnLock;

	#;�N�b�L�[���s
	&SetCookie;

	&PrintLogHtml;
}

#;�摜�ۑ�����____________________________________________________________;
sub SaveBinFile
{
	local($filename, $F);
	local($Len) = length($FILE_DATA{'IMG'});

	#;�e��`�F�b�N
	if($Len <= 0){
		&PrintErrHtml("�摜���I������Ă��܂���B");
	}

	#�}�b�N�o�C�i���Ȃ�A�}�b�N�o�C�i��������
	if($FILE_TYPE{'IMG'} eq 'application/x-macbinary'){
		$FILE_DATA{'IMG'} = &DelMacBin($FILE_DATA{'IMG'});
	}

	local($rtn, $w, $h) = &GetPicInf($FILE_DATA{'IMG'});

	if(($Len > $MaxPicSize * 1024) && ($MaxPicSize)){
		&PrintErrHtml("�摜�t�@�C�����A$MaxPicSize KByte���z���Ă��܂��B");
	}

	if(!$rtn){
		&PrintErrHtml("�摜�t�@�C��(GIF,JPEG)�ł͂Ȃ���\�\\��������܂��B<BR>��m�F���������B");
	}

	if(($w > $MaxPicWidth) && ($MaxPicWidth)){
		&PrintErrHtml("�摜�t�@�C���̉�ʃT�C�Y���傫�����܂��B<BR>��$MaxPicWidth �~ �c$MaxPicHeight�ȉ��̉摜�����󂯂��Ă���܂���<BR>��m�F���������B");
	}

	if(($h > $MaxPicHeight) && ($MaxPicHeight)){
		&PrintErrHtml("�摜�t�@�C���̉�ʃT�C�Y���傫�����܂��B<BR>��$MaxPicWidth �~ �c$MaxPicHeight�ȉ��̉摜�����󂯂��Ă���܂���<BR>��m�F���������B");
	}

	#;�ۑ�����
	$PicWidth = $w;
	$PicHeight = $h;
	$PicType = $rtn;
	$PicLen = $Len;

	$rtn =~ tr/A-Z/a-z/;

	$filename =  $DateFileName . "\.$rtn";

	$F = $IconPath . "\/" . $filename;
	if(-e $F){
		#;�O�̂��ߓ����t�@�C�������Ȃ����`�F�b�N
		&PrintErrHtml("�����̉摜�t�@�C�������ɓo�^����Ă��܂��B");
	}

	open(OUT, "> $F") || &PrintErrHtml("�摜�o�^�Ɏ��s���܂����B<BR>����:$!");
	binmode(OUT);
	print OUT $FILE_DATA{'IMG'};
	close(OUT);

	$PicName = $filename;
}

#;���O�폜���s____________________________________________________________;
sub ExecDelete
{
	if(scalar(keys %DELETE_ID)==0){
		#�폜
		#if($LocationMode){
		#	print "Location: $ThisCGI\n\n";
		#}else{
		#	&PrintLogHtml;
		#}
		&PrintLogHtml;
		return;
	}

	#;���b�N�J�n
	&OpenFileLock;

	#;���O�Ǎ�
	open(IN,"$SaveFile") || &PrintErrHtml("�ۑ��t�@�C���̓ǂݍ��݂Ɏ��s���܂����B<BR>����:$!");
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
				&PrintErrHtml("�폜�L�[�܂��͊Ǘ��҃p�X���[�h���Ⴂ�܂��B");
			}
		}
		$F = $IconPath . "\/" . $pfn;
		unlink($F) if($PicDeiMode && (-e $F));
	}

	#;���O����
	open(OUT,">$SaveFile") || &PrintErrHtml("�ۑ��t�@�C���̏������݂Ɏ��s���܂����B<BR>����:$!");
	print OUT @NEW_LINES;
	close(OUT);

	#;���b�N����
	&FileUnLock;

	&PrintLogHtml;
}

#;�摜�t�@�C���폜����____________________________________________________;
sub DelIcon
{
	foreach(@DEL_ITEM){
		($pfn, $ptitle) = split(/\,/, $_);
		$F = $IconPath . "\/" . $pfn;
		unlink($F) if(-e $F);
	}
}

#;�����[�g�z�X�g���擾____________________________________________________;
sub GetHost
{
	local($addr) = $ENV{'REMOTE_ADDR'};
	local($host) = $ENV{'REMOTE_HOST'};
	if(($host eq "") || ($host eq $addr)){

		#;���g���̃T�[�o�[���Agethostbyaddr�̎g�p���֎~���Ă���ꍇ�A
		#;���̍s���폜���Ă��������B
		#;�R�����g�ɂ��邾���ł́A�_���ȃT�[�o�[������悤�ł��B
		$host = gethostbyaddr(pack("C4", split(/\./, $addr)), 2);
		#;_______________________________________________________

		$host = $addr if($host eq "");
	}
	$Host  = $host;
}

#;�ȈՃZ�L�����e�B�`�F�b�N________________________________________________;
sub SeculityCheck
{
	&GetHost;
	
	if($SaveMode == 1){      #;1-�p�X���[�h�ɂ�鐧��
		return if($FORM{'WRITEPASS'} eq $UserPass);
		return if($FORM{'WRITEPASS'} eq $addminpass);
		&PrintErrHtml("�o�^�p�p�X���[�h���Ⴂ�܂��B<BR>�Ǘ��l�Ƀp�X���[�h�������Ă�����Ă��������B");
	}elsif($SaveMode == 2){  #;2-�����[�g�z�X�g�ɂ�鐧��
		@HOSTS = split(/\n/, $NGRemortHost);
		foreach(@HOSTS){
			if($Host =~ /$_/i){
				&PrintErrHtml("�o�^�ł��Ȃ������[�g�z�X�g�ł��B");
			}
		}
	}
	if($ProxyNG){
		if($Host =~ /proxy/i){
			&PrintErrHtml("�v���L�V�T�[�o�[����̓o�^�͂ł��܂���B");
		}
	}
}

#;�t�H�[�����f�R�[�h____________________________________________________;
sub FormDecord
{
	if($ENV{'CONTENT_TYPE'} =~ /multipart\/form-data; boundary=[^\0]*$/i){
		&InitFormMultiPart;
	}else{
		&InitFormNorm;
	}
}

#;�폜�p�t�H�[�����f�R�[�h______________________________________________;
#  ���y�[�W�ł��g�p����̂ŁAGET�Ή�
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

#;���e�p�t�H�[�����f�R�[�h______________________________________________;
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
	$que = undef; #�ꉞ�N���A���
}
#;�摜���擾����________________________________________________________;
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

#;GIF �̃T�C�Y���擾______________________________________________________;
#    USAGE:($sts,$width,$height) = &GetGifSize(data);
#    ����)
#        data: GIF�f�[�^
#    �Ԓl)
#        $sts   : true:GIF, false:GIF�t�@�C���ł͂Ȃ��B
#        $width : ���̒���
#        $height: �c�̒���
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

#;JPEG �̃T�C�Y���擾_____________________________________________________;
#    USAGE:($sts,$width,$height) = &GetJpegSize(data);
#    ����)
#        data: Jpeg�f�[�^
#    �Ԓl)
#        $sts   : true:Jpeg, false:Jpeg�t�@�C���ł͂Ȃ��B
#        $width : ���̒���
#        $height: �c�̒���
sub GetJpegSize
{
	local($buffer) = $_[0];

	#SOI APP0����
	local($FFD8Idx) = index($buffer, "\xFF\xD8\xFF\xE0");
	if($FFD8Idx == -1){
		return 0, "", "";
	}

	#JFIF���ʕ����񌟍�
	local($JFIFIdx) = index($buffer, "JFIF", $FFD8Idx + 4);
	if($JFIFIdx == -1){
		return 0, "", "";
	}

	#Get Jpeg Size
	local($SOFnIdx) = 2;
	local(%SOFn) = ("\xC0", 1, "\xC1", 1, "\xC2", 1, "\xC3", 1, "\xC5", 1, 
					"\xC6", 1, "\xC7", 1, "\xC8", 1, "\xC9", 1, "\xCA", 1, 
					"\xCB", 1, "\xCD", 1, "\xCE", 1, "\xCF", 1);

	#SOFn����
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
#;PNG �̃T�C�Y���擾_____________________________________________________;
#    USAGE:($sts,$width,$height) = &get_png_size(data);
#    ����)
#        data: PNG�f�[�^
#    �Ԓl)
#        $sts   : 1:PNG, 0:PNG�t�@�C���ł͂Ȃ��B
#        $width : ���̒���
#        $height: �c�̒���
sub get_png_size
{
	local($buffer) = $_[0];
	#����(8byte) 89 50 4E 47 0D 0A 1A 0A ����
	unless(substr($buffer, 0, 8) eq "\x89\x50\x4E\x47\x0D\x0A\x1A\x0A"){
		return 0, "", "";
	}

	#IHDR����
	#  �`�����N�\�� 
	#  1-4 �`�����N�̒���
	#  5-9 �`�����N�^�C�v
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
#;�}�b�N�o�C�i���̏���____________________________________________________;
sub DelMacBin
{
	local($bindata) = $_[0];
	local(@len, $size, $k);

	#�}�b�N�o�C�i���w�b�_����A�f�[�^�������擾
	@len = unpack("CCCC", substr($bindata, 83, 4));
	$size = 0;
	$k = 3;
	foreach(0..3){
		$size += $len[$_] * (256 ** $k);
		$k--;
	}
	
	return substr($bindata, 128, $size);
}
#;���{��R�[�h�ݒ�________________________________________________________;
sub GetJapanCode
{
	$Bit_1 = ord(substr("��", 0, 1));
	if($Bit_1 == 0xb4){
		$CharSet = "x-euc-jp";
	}elsif($Bit_1 == 0x1b) {
		$CharSet = "iso-2022-jp";
	}else{
		$CharSet = "x-sjis";
	}
}

#;�N�b�L�[���s____________________________________________________________;
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

#;�N�b�L�[�擾____________________________________________________________;
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

#;OpenFile���b�N__________________________________________________________;
sub OpenFileLock
{
	return unless($LockMode);
	local($Retry) = 5;
	foreach(1..$Retry){
		if(-e "$LockFile"){
			local($mtime) = (stat($LockFile))[9];
			if ($mtime < $GTime - 600){
				#;��������Ă���A�P�O���ȏ�o�߂���Ă�����폜
				unlink($LockFile);
			}else{
				sleep(1);
			}
		}else{
			open(LOCK, ">$LockFile") || &PrintErrHtml("���b�N�t�@�C���������s<BR>����:$!");
			close(LOCK);
			$LOCK_SW = 1;
			return;
		}
	}
	&PrintErrHtml("���݁A���̐l���o�^���s�Ȃ��Ă��܂��B<BR>�ēx�A�o�^�����s���Ă��������B");
}

#;���b�N����______________________________________________________________;
sub FileUnLock
{
	unlink($LockFile) if(-e "$LockFile");
	$LOCK_SW = 0;
}

#;�Í���__________________________________________________________________;
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

#;�Í��ƍ�________________________________________________________________;
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



