#!/usr/bin/perl

# Dream Editor v2.3 (2001/02/17)
# Copyright(C) Kent Web 2001
# webmaster@kent-web.com
# http://www.kent-web.com/

#============#
#  �ݒ荀��  #
#============#

# �p�X���[�h (�p�����Ŏw��)
$pass = '0123';

# �X�N���v�g��
$script = './edit.cgi';

# method�`�� (POST or GET)
$method = 'POST';

# ���O��u���T�[�o�f�B���N�g��
#   �� ���s�f�B���N�g���ł���΂��̂܂܂ł悢
#   �� �Ō�͕K�� / �ŕ���
#   �� �t���p�X�Ȃ� / ����n�߂�ihttp://����ł͂Ȃ��j
$LogDir = './';

#============#
#  �ݒ芮��  #
#============#

&decode;
if ($in{'pass'} ne "$pass") { &enter; }
if ($mode eq "mente") { &mente; }
elsif ($mode eq "make") { &make; }
elsif ($mode eq "del") { &id_del; }
&admin;


#------------#
#  �Ǘ����  #
#------------#
sub admin {
	&header;
	print <<"EOM";
<table width="100%"><tr><th bgcolor="#0000A0">
<font color="#FFFFFF">�Ǘ����</font>
</th></tr></table>
<blockquote>
<P>
<OL>
<B><LI>�J�E���^�l�̕ύX�����e�i���X</B>
<P>
  <DL>
  <DT>ID������͂��A���M�L�[�������ĉ������B
  </DL>
<P>
<form action="$script" method="$method">
<input type=hidden name=mode value="mente">
<input type=hidden name=pass value="$in{'pass'}">
ID�� <input type=text name=id size=12>
<input type=submit value="���M����">
</form>
<hr>
<P>
<B><LI>���O�t�@�C���̍폜</B>
<P>
  <DL>
  <DT>ID������͂��A�폜�L�[�������ĉ������B
  </DL>
<P>
<form action="$script" method="$method">
<input type=hidden name=mode value="del">
<input type=hidden name=pass value="$in{'pass'}">
ID�� <input type=text name=id size=12>
<input type=submit value="�폜����">
</form>
<hr>
<P>
<B><LI>���O�t�@�C���̐���</B>
<P>
  <DL>
  <DT>ID������͂��A�����L�[�������ĉ������B
  </DL>
<P>
<form action="$script" method="$method">
<input type=hidden name=mode value="make">
<input type=hidden name=pass value="$in{'pass'}">
�쐬ID�� <input type=text name=id size=12> (�K�����p�p������)<br>
�J�n�J�E���g�� <input type=text name=count size=12 value="0">
<P>
<input type=submit value="��������">
</form>
</OL>
</blockquote>
</body></html>
EOM
	exit;
}

#------------------#
#  �p�X���[�h���  #
#------------------#
sub enter {
	&header;
	print <<"EOM";
<center>
<h4>- �p�X���[�h����͂��Ă������� -</h4>
<form action="$script" method="$method">
<input type=password name=pass size=8><input type=submit value=" �F�� ">
</form></center>
</body></html>
EOM
	exit;
}

#------------------#
#  �����e�������  #
#------------------#
sub mente {
	# ���O�t�@�C�����`
	$logfile = "$LogDir$id\.dat";
	if ($id =~ /\W/) { &error("ID���͔��p�̉p�����Ŏw�肵�ĉ�����"); }

	# ���O�̑��݂��`�F�b�N
	unless (-e $logfile) {
		&error("�w���ID���O�t�@�C�� <B>$id</B> ��������܂���");
	}

	# ���O��ǂݍ���
	open(IN,"$logfile") || &error("Can't open $logfile");
	$line = <IN>;
	close(IN);

	# ���O�𕪉�
	($count,$ip) = split(/:/,$line);

	# �����e���s
	if ($flag) {
		$line = "$in{'count'}\:$ip";

		# ���O���X�V
		open(OUT,">$logfile") || &error("Can't write $logfile");
		print OUT $line;
		close(OUT);

		# �����ʒm
		&header;
		print "<center><h3>�����e�����͐���Ɋ������܂���</h3>\n";
		print "<hr width='400'>\n";
		print "<table><tr><td>ID���F<b>$id</b>\n";
		print "<P>�J�E���g���F<b>$in{'count'}</b></td></tr></table>\n";
		print "<hr width='400'>\n";
		print "<form action=\"$script\" method=$method>\n";
		print "<input type=hidden name=mode value=admin>\n";
		print "<input type=hidden name=pass value=\"$in{'pass'}\">\n";
		print "<input type=submit value=\"�Ǘ���ʂɂ��ǂ�\"></form>\n";
		print "</center>\n";
		print "</body></html>\n";
	}

	# ���O��\��
	else {
		&header;
		print <<"EOM";
<center>
��<b>$id</b>�̃J�E���g���C�����܂��B
<P>
<form action="$script" method="$method">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=mode value="mente">
<input type=hidden name=id value="$id">
<input type=hidden name=flag value="1">
�J�E���g�� <input type=text name=count size=12 value="$count">
<input type=submit value="�C������">
</form>
</center>
</body></html>
EOM
	}
	exit;
}

#------------------#
#  ID�t�@�C���폜  #
#------------------#
sub id_del {
	# ���O�t�@�C�����`
	$logfile = "$LogDir$id\.dat";
	if ($id =~ /\W/) { &error("ID���͔��p�̉p�����Ŏw�肵�ĉ�����"); }

	# ���O�̑��݂��`�F�b�N
	unless (-e $logfile) {
		&error("�w���ID���O�t�@�C�� <B>$id</B> ��������܂���");
	}

	# �폜���s
	if ($flag) {
		unlink($logfile);

		# �����ʒm
		&header;
		print <<"EOM";
<center>
<hr width='400'>
ID�t�@�C�� <B>$id</B> �͍폜����܂���
<hr width='400'>
<form action="$script" method=$method>
<input type=hidden name=mode value=admin>
<input type=hidden name=pass value="$in{'pass'}">
<input type=submit value=�Ǘ���ʂɂ��ǂ�></form>
</center>
</body></html>
EOM
	}

	# �Ċm�F���
	else {
		&header;
		print <<"EOM";
<center><hr width="400">
ID�t�@�C�� <font color=#DD0000><B>$id</B></font> ��{���ɍ폜���܂����H
<hr width="400">
<P><form action="$script" method="$method">
<input type=hidden name=id value="$id">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=mode value="del">
<input type=hidden name=flag value="1">
<input type=submit value="�폜����"></form>
</center>
</body></html>
EOM
	}
	exit;
}

#----------------------#
#  ID�t�@�C����������  #
#----------------------#
sub make {
	if ($id =~ /\W/) { &error("ID���͔��p�̉p�����Ŏw�肵�ĉ�����"); }

	# ���O�t�@�C�����`
	$logfile = "$LogDir$id\.dat";

	# ���O�̑��݂��`�F�b�N
	if (-e $logfile) {
		&error("�w���ID <B>$id</B> �͊��Ɏg�p����Ă��܂��B<br>
			�ʂ�ID�����w�肵�ĉ�����");
	}

	# ���O���t�H�[�}�b�g
	$new_file = $in{'count'};

	# ���O���쐬
	open(OUT,">$logfile") || &error("Can't write $logfile");
	print OUT $new_file;
	close(OUT);

	# �p�[�~�b�V������ 666 ��
	chmod (0666,$logfile);

	# �����ʒm
	&header;
	print "<center><h3>ID�쐬�����͐���Ɋ������܂���</h3>\n";
	print "<hr width='60%'>\n";
	print "<table><tr><td>�쐬ID���F<b>$id</b><P>\n";
	print "�J�E���g���F<b>$in{'count'}</b></td></tr></table>\n";
	print "<hr width='60%'>\n";
	print "<form action=\"$script\" method=$method>\n";
	print "<input type=hidden name=mode value=admin>\n";
	print "<input type=hidden name=pass value=\"$in{'pass'}\">\n";
	print "<input type=submit value=\"�Ǘ���ʂɂ��ǂ�\"></form>\n";
	print "</center>\n";
	print "</body></html>\n";
	exit;
}

#----------------#
#  �f�R�[�h����  #
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

	# �����̎擾
	$ENV{'TZ'} = "JST-9";
	($sec,$min,$hour,$mday,$mon,$year,$dmy,$dmy) = localtime(time);
}

#----------------#
#  HTML�w�b�_�[  #
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
#  �G���[����  #
#--------------#
sub error {
	&header;
	print "<center><h3>ERROR !</h3>\n";
	print "<font color='#DD0000'>$_[0]</font>\n";
	print "</center>\n";
	print "</body></html>\n";
	exit;
}
