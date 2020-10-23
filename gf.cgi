#!/usr/bin/perl

#
# ��������O���f�[�V�����\��������CGI �u�O���t�H���vVer2.44l
# Copyright (C) 1999 AID/All right reserved.
#                    http://www.garakutabeya.com/
# html�^�O�ŃO���f�[�V�������������c�[���ł��B
# �쐬��͂���𒣂�t�������Ƃ���ɓ\��Ί����ł��B
#
# Ver2.44l �S�p�Ɣ��p�������Ő؂�ւ���悤�ɂ��܂����B
#          ����p�Ƃ��Ĕ��p�J�^�J�i���g���Ȃ��Ȃ�܂����B
# Ver2.44  �Ƃ�ł��Ȃ��o�O�����B�Ƃ�������{�I�Ȏ��B
#          ���E���Ԉ���Ă��́E�E�E
# Ver2.4   ����\�[�X������ɏX���ύX
#          �T�C�Y�������������A�����������瑬���Ȃ��Ă��邩���E�E�E
# Ver2.3   checkbox�̌��ʂ����ɔ��f����l�ɕύX
# Ver2.2   �F�̑I���̌��ʂ����ɔ��f����l�ɕύX
# Ver2.1   �F�̕ω��̕����ׂ����ړ�����悤�ɕύX
# Ver2.0   �S�p�ɑΉ��i�Ƃ������S�p�Ɣ��p�̑g�ݍ��킹�̓_���j
# Ver1.3   �����[�h�ǉ����f�o�b�O
# Ver1.2   �܂�Ԃ��@�\�ǉ�
# Ver1.1   �\�[�X�\�����ǉ�
# Ver1.0   �Ƃ肠��������

# �����R�[�h
$code = "sjis";

### ���O�F���X�g
# $CT[x] ... ���ۂ̐F
# $CN[x] ... ���X�g�ɕ\������F�̖��O
$CT[0]  = '000000';	$CN[0] = "����";
$CT[1]  = '0000ff';	$CN[1] = "����";
$CT[2]  = '00ff00';	$CN[2] = "�݂ǂ�";
$CT[3]  = '00ffff';	$CN[3] = "�݂�����";
$CT[4]  = 'ff0000';	$CN[4] = "����";
$CT[5]  = 'ff00ff';	$CN[5] = "�ނ炳��";
$CT[6]  = 'ffff00';	$CN[6] = "������";
$CT[7]  = 'ffffff';	$CN[7] = "����";

$FN[1] = "�ŏ�";
$FN[2] = "��";
$FN[3] = "��⏬";
$FN[4] = "����";
$FN[5] = "����";
$FN[6] = "��";
$FN[7] = "�ő�";

require './jcode.pl';

########## ����������perl�̒m���̂���l�������������Ă�������
$version = "2.44l";

print "Content-type: text/html\n\n";

&main;
exit;

sub main{
	&init_variables;
	&check_input;
	&show_html;
}

##### �ϐ�������
sub init_variables{
	$flag = 0;			# �܂�Ԃ�����odd,even�̃t���O
	$s = 1;			# HSV�ʓx�p�ϐ�
	$v = 1;			# HSV���x�p�ϐ�
}

##### ���̓`�F�b�N
sub check_input{
	if ($ENV{'REQUEST_METHOD'} eq "POST"){
		read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
	}else{
		$buffer = $ENV{'QUERY_STRING'};
	}
	@pairs = split(/&/, $buffer);
	foreach $pair (@pairs) {
		($vn, $value) = split(/=/, $pair);
		$FORM{$vn} = $value;
	}

	$cmoji = &decode($FORM{'moji'});
	$mojisize = $FORM{'msize'};

	if($FORM{'fcol'}){
		$back_color = $FORM{'bfcol'};
		$start_color  = $FORM{'sfcol'};
		$end_color    = $FORM{'efcol'};
	}else{
		$back_color = $CT[$FORM{'bcol'}];
		$start_color  = $CT[$FORM{'scol'}];
		$end_color    = $CT[$FORM{'ecol'}];
	}

	$turnselect = "CHECKED" if($FORM{'turn'});
	$boldselect = "CHECKED" if($FORM{'bold'});
	$italselect = "CHECKED" if($FORM{'ital'});
	$fcolselect = "CHECKED" if($FORM{'fcol'});
	$rainselect = "CHECKED" if($FORM{'rain'});
}

##### �O���f�[�V�����t�H���g�쐬
# �m�[�}���i�ŏ�����Ō�֕ω��j
sub make_color{
	@scolor = &get_color($start_color);
	@ecolor = &get_color($end_color);
	@rgbint = &interval_color(@ecolor, @scolor, ($moji_leng-1));
	$htmlcolorbuf .= "<font color=\"#$start_color\">$mojibit[0]</font>";
	for($i=1; $i<$moji_leng; $i++){
		@scolor = &add_color(@scolor, @rgbint, 0);
		$colbuf = &make_color_code(@scolor);
		$htmlcolorbuf .= "<font color=\"#$colbuf\">$mojibit[$i]</font>";
	}
}

# �^�񒆂Ő܂�Ԃ�
sub make_color_turn{
	my ($s,$ce,$cs,$e);
	$moji_hlen = int($moji_leng/2);
	@scolor = &get_color($start_color);
	@ecolor = &get_color($end_color);
	$s = 1;
	$e = $moji_leng;
	if(($moji_leng%2) eq 1){
		$flag = 1;
		@rgbint = &interval_color(@ecolor, @scolor, $moji_hlen);
		$ce = $moji_hlen;
		$cs = $moji_hlen+1;
	}else{
		@rgbint = &interval_color(@ecolor, @scolor, $moji_hlen-1);
		$ce = $moji_hlen;
		$cs = $moji_hlen+1;
	}
	$htmlcolorbuf .= "<font color=\"#$start_color\">$mojibit[0]</font>";
	for($i=$s; $i<$ce; $i++){
		@scolor = &add_color(@scolor, @rgbint, 0);
		$colbuf = &make_color_code(@scolor);
		$htmlcolorbuf .= "<font color=\"#$colbuf\">$mojibit[$i]</font>";
	}
	if($flag){$htmlcolorbuf .= "<font color=\"#$end_color\">$mojibit[$moji_hlen]</font>";}
	else{$htmlcolorbuf .= "<font color=\"#$end_color\">$mojibit[$moji_hlen]</font>";}
	for($i=$cs; $i<$e; $i++){
		@ecolor = add_color(@ecolor, @rgbint, 1);
		$colbuf = &make_color_code(@ecolor);
		$htmlcolorbuf .= "<font color=\"#$colbuf\">$mojibit[$i]</font>";
	}
}

# �����[�h�iHSV�n�ŐF��ω�������j
sub make_color_rainbow{
	my ($h, $hh, $ii, $f, $p1, $p2, $p3, $i);
	$interval = 300 / $moji_leng;
	$h = 0;
	$s = $FORM{'shsv'};
	$v = $FORM{'vhsv'};
	$ii = 0;
	$f  = 0;
	$p1 = $v*(1-$s);
	$p3 = $v*(1-$s);
	$scolor[0]=$v*255;
	$scolor[1]=$p3*255;
	$scolor[2]=$p1*255;
	$colbuf = &make_color_code(@scolor);
	$htmlcolorbuf .= "<font color=\"#$colbuf\">$mojibit[0]</font>";
	for($i=1; $i<$moji_leng; $i++){
		$h  = $h + $interval;
		$ii = int($h/60);
		$f  = ($h%60)/60;
		$p1 = $v*(1-$s);
		$p2 = $v*(1-$s*$f);
		$p3 = $v*(1-$s*(1-$f));
		if($ii eq 0){$scolor[0]=$v;  $scolor[1]=$p3; $scolor[2]=$p1;}
		if($ii eq 1){$scolor[0]=$p2; $scolor[1]=$v;  $scolor[2]=$p1;}
		if($ii eq 2){$scolor[0]=$p1; $scolor[1]=$v;  $scolor[2]=$p3;}
		if($ii eq 3){$scolor[0]=$p1; $scolor[1]=$p2; $scolor[2]=$v; }
		if($ii eq 4){$scolor[0]=$p3; $scolor[1]=$p1; $scolor[2]=$v; }
		if($ii eq 5){$scolor[0]=$v;  $scolor[1]=$p1; $scolor[2]=$p2;}
		$scolor[0] = $scolor[0]*255;
		$scolor[1] = $scolor[1]*255;
		$scolor[2] = $scolor[2]*255;
		$colbuf = &make_color_code(@scolor);
		$htmlcolorbuf .= "<font color=\"#$colbuf\">$mojibit[$i]</font>";
    }
}

##### �F�����炷��
sub interval_color{
	my (@ic) = @_;
	my ($ans);
	$ans[0] = ($ic[0] - $ic[3]) / $ic[6];
	$ans[1] = ($ic[1] - $ic[4]) / $ic[6];
	$ans[2] = ($ic[2] - $ic[5]) / $ic[6];
	@ans;
}

##### �F�����Z
sub add_color{
	my (@ac) = @_;
	my ($ans);
	if($ac[6]==0){
		$ans[0] = $ac[0] + $ac[3];
		$ans[1] = $ac[1] + $ac[4];
		$ans[2] = $ac[2] + $ac[5];
	}else{
		$ans[0] = $ac[0] - $ac[3];
		$ans[1] = $ac[1] - $ac[4];
		$ans[2] = $ac[2] - $ac[5];
	}
	($ans[0],$ans[1],$ans[2]);
}

##### �F�̕���
sub get_color{
	my ($col) = @_;
	my ($gc);
	$gc[0] = hex(substr($col, 0, 2));
	$gc[1] = hex(substr($col, 2, 2));
	$gc[2] = hex(substr($col, 4, 2));
	@gc;
}

##### �F�쐬
sub make_color_code{
	my (@list) = @_;
	my ($i);
	$mcc[0] = int($list[0] >> 4);
	$mcc[1] = int($list[0] & 0x0f);
	$mcc[2] = int($list[1] >> 4);
	$mcc[3] = int($list[1] % 0x0f);
	$mcc[4] = int($list[2] >> 4);
	$mcc[5] = int($list[2] % 0x0f);
	for($i=0; $i<6; $i++){
		if($mcc[$i] > 9){
			if($mcc[$i] eq 10){$mcc[$i]="a";}
			elsif($mcc[$i] eq 11){$mcc[$i]="b";}
			elsif($mcc[$i] eq 12){$mcc[$i]="c";}
			elsif($mcc[$i] eq 13){$mcc[$i]="d";}
			elsif($mcc[$i] eq 14){$mcc[$i]="e";}
			else{$mcc[$i]="f";}
		}
	}
	"$mcc[0]$mcc[1]$mcc[2]$mcc[3]$mcc[4]$mcc[5]";
}

##### �S�p������̎��̏���
sub zenkaku_henkan{
	my ($length, @nihongo) = @_;
	my ($i, @henkan);
	$length = $length / 2;
	for($i=0; $i<$length; $i++){
		$henkan[$i] = "$nihongo[2*$i]$nihongo[2*$i+1]";
	}
	@henkan;
}

##### �\��
sub show_html{
	local($htmlbuf);

	### ���O�F�̑I�����X�g
	for(0..$#CT){
		$color_options1 .= "<option value=\"$_\"";
		$color_options1 .= "selected" if($FORM{'scol'} == $_);
		$color_options1 .=">$CN[$_]\n";
		$color_options2 .= "<option value=\"$_\"";
		$color_options2 .= "selected" if($FORM{'ecol'} == $_);
		$color_options2 .=">$CN[$_]\n";
		$color_options3 .= "<option value=\"$_\"";
		$color_options3 .= "selected" if($FORM{'bcol'} == $_);
		$color_options3 .=">$CN[$_]\n";
	}

	for(1..$#FN){
		$font_options .= "<option value=\"$_\"";
		$font_options .= "selected" if($mojisize == $_);
		$font_options .= ">$FN[$_]\n";
	}

	$htmlbuf  = &html_header;
	$htmlbuf .= &html_color_form;
	$htmlbuf .= &html_const_header;
	$htmlcolorbuf = "<font size=$mojisize>";
	if($FORM{'ital'}){$htmlcolorbuf .= "<i>";}
	if($FORM{'bold'}){$htmlcolorbuf .= "<b>";}
	@mojibit = split(//,$cmoji);
	$moji_leng = @mojibit;
#	if($FORM{'dbyt'}){
	if(&jcode'getcode(*cmoji)){
		@mojibit = &zenkaku_henkan($moji_leng, @mojibit);
		$moji_leng = $moji_leng / 2;
	}
	if($moji_leng ne 0){
		if($FORM{'turn'} && !$FORM{'rain'}){
			&make_color_turn;
		}elsif($FORM{'rain'}){
			&make_color_rainbow;
		}else{
			&make_color;
		}
	}
	if($FORM{'bold'}){$htmlcolorbuf .= "</b>";}
	if($FORM{'ital'}){$htmlcolorbuf .= "</i>";}
	$htmlcolorbuf .= "</font>";
	$htmlbuf .= $htmlcolorbuf;
	$htmlbuf .= &html_const_footer;
	$htmlcolorbuf =~ s/</&lt;/g;
	$htmlcolorbuf =~ s/>/&gt;/g;
	$htmlbuf .= "<table border><tr><td width=640><tt>";
	$htmlbuf .= $htmlcolorbuf;
	$htmlbuf .= "</tt></td></tr></table>";
	$htmlbuf .= &html_footer;

	print $htmlbuf;
}


##### �w�b�_
sub html_header{
	"
<html>
<head><title>Gradation Font</title></head>
<body bgcolor=white text=black>
<table border cellpadding=10><tr><td bgcolor=black>
<font size=7><font color=\"#ff0000\">G</font><font color=\"#ff3700\">r</font><font color=\"#ff7200\">a</font><font color=\"#ffaa00\">d</font><font color=\"#ffe500\">a</font><font color=\"#ddff00\">t</font><font color=\"#a5ff00\">i</font><font color=\"#6aff00\">o</font><font color=\"#2eff00\">n</font><font color=\"#00ff08\"> </font><font color=\"#00ff43\">F</font><font color=\"#00ff7f\">o</font><font color=\"#00ffb6\">n</font><font color=\"#00fff2\">t</font><font color=\"#00d4ff\"> </font><font color=\"#0099ff\">�u</font><font color=\"#005dff\">�O</font><font color=\"#0026ff\">��</font><font color=\"#1500ff\">�t</font><font color=\"#5000ff\">�H</font><font color=\"#8800ff\">��</font><font color=\"#c300ff\">�v</font></font>
<font color=white>Ver$version</font>
</td></tr></table>
<p>
<b>�����������O���f�[�V�����t�H���g������Ă�������</b><br><br>
��������<br>
�E�S�p�Ɣ��p�̍��݂͏o���܂���B<br>�E���p�J�^�J�i�͎g�p�o���܂���B<br>�E�����񂪒Z�����Y��ȃO���f�[�V�����ɂȂ�Ȃ��ꍇ������܂��B<br>
<br>
<A href=\"javascript:history.back()\">�f���ɖ߂�</A><hr>
";
}

##### input and establish
sub html_color_form{
	"
<form method=\"post\" action=\"gf.cgi\">
<table border cellpadding=\"0\" cellspacing=\"0\"><tr><td>
<table><tr><td>
�F��t���������������͂��Ă�������<br>
<input type=\"text\" name=\"moji\" value=\"$cmoji\" size=\"80\"><br>
<font color=\"#000000\">��</font><font color=\"#0000ff\">��</font><font color=\"#00ff00\">��</font><font color=\"#00ffff\">��</font><font color=\"#ff0000\">��</font><font color=\"#ff00ff\">��</font><font color=\"#ffff00\">��</font><font color=\"#000000\">��</font><br>
���̐F�F<select name=\"scol\">$color_options1</select>
�E�̐F�F<select name=\"ecol\">$color_options2</select>
�w�i�F<select name=\"bcol\">$color_options3</select>
�����T�C�Y�F<select name=\"msize\">$font_options</select>
</td></tr><tr><td>
<input type=\"checkbox\" name=\"turn\" value=\"1\" $turnselect>�^�񒆂Ő܂�Ԃ�\�@
<input type=\"checkbox\" name=\"bold\" value=\"1\" $boldselect>����\�@
<input type=\"checkbox\" name=\"ital\" value=\"1\" $italselect>�Α�\�@
<input type=\"checkbox\" name=\"fcol\" value=\"1\" $fcolselect>�F���ׂ����ݒ�<br>
���̐F<input type=\"text\" name=\"sfcol\" value=\"$start_color\" size=\"10\">
�E�̐F<input type=\"text\" name=\"efcol\" value=\"$end_color\" size=\"10\">
�w�i<input type=\"text\" name=\"bfcol\" value=\"$back_color\" size=\"10\"><br>
</td></tr><tr><td>
<input type=\"checkbox\" name=\"rain\" value=\"1\" $rainselect>��\�@
�ʓx�F<input type=\"text\" name=\"shsv\" size=\"5\" value=\"$s\">\�@
���x�F<input type=\"text\" name=\"vhsv\" size=\"5\" value=\"$v\">
�i0����1�̊ԂŎw�肵�Ă��������j<br>
</td></tr><tr><td>
<input type=\"submit\" value=\"�O���f�[�V�����t�H���g�쐬\">
</td></tr></table>
</td></tr></table>
<hr>
";
}

##### ����
# ���ʗp�w�b�_
sub html_const_header{
	"
<table cellpadding=20><tr><td bgcolor=$back_color><font size=$mojisize>
";
}

# ���ʗp�t�b�^
sub html_const_footer{
	"
</font></td></tr></table><hr>���̃\\�[�X���R�s�[���Ďg���Ă�������<br>
";
}

##### �t�b�^�i���������Ȃ��悤�Ɂj
sub html_footer{
	"
<div align=right>
<table border=1><tr><td bgcolor=yellow>
<a href=\"http://www.garakutabeya.com/\"><font color=blue><b>��y������</b></font></a></td></tr></table></div>
</font></body></html>
";
}

##### �f�R�[�h
sub decode{
	local($org, $tag) = @_;
	$org =~ tr/+/ /;
	$org =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	$org =~ s/\t//g;
	unless($tag){
		$org =~ s/</&LT;/g;
		$org =~ s/>/&GT;/g;
		$org =~ s/"/&#34;/g;
		$org =~ s/'/&#39;/g;
	}
	$org =~ s/\cM//g;
	$org =~ s/\n//g;
	&jcode'convert(*org, $code);
	$org;
}
