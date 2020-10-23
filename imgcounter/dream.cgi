#!/usr/bin/perl

#---------------------------------------#
#  DREAM COUNTER v2.31 (2001/03/04)	#
#  Copyright(C) Kent Web 2001		#
#  webmaster@kent-web.com		#
#  http://www.kent-web.com/		#
#---------------------------------------#

#--- [���ӎ���] ------------------------------------------------#
# 1. ���̃X�N���v�g�̓t���[�\�t�g�ł��B���̃X�N���v�g���g�p����	#
#    �����Ȃ鑹�Q�ɑ΂��č�҂͈�؂̐ӔC�𕉂��܂���B		#
# 2. �ݒu�Ɋւ��鎿��̓T�|�[�g�f���ɂ��肢�������܂��B	#
#    ���ڃ��[���ɂ�鎿��͈�؂��󂯂������Ă���܂���B	#
#---------------------------------------------------------------#

# [�^�O�̏������̗�] (*** �̓��O�t�@�C����)
#
#  �E�J�E���^ <img src="count/dream.cgi?id=***">
#  �E�����\�� <img src="count/dream.cgi?mode=time">
#  �E�J�����_ <img src="count/dream.cgi?mode=date">
#  �E�t�@�C���̍X�V����
#             <img src="count/dream.cgi?file=/home/�`/index.html">
#             [����] --> /home/�`/index.html�̕����̓t���p�X���w��
#
#  * ���p��(id���� kent �Ɖ���)��
#    1.�摜��ύX����Ƃ��F(�ȉ���gif2�f�B���N�g���̉摜�w���)
#      <img src="�p�X/dream.cgi?id=kent&gif=2">
#    2.�����������_���ɕ\������Ƃ��F
#      <img src="�p�X/dream.cgi?mode=rand">
#    3.�J�E���^�������V���ɂ���Ƃ��F
#      <img src="�p�X/dream.cgi?id=kent&fig=7">
#
#  * �`�F�b�N���[�h ( mode=check �Ƃ������������ČĂяo���j
#    http://�`�`/dream.cgi?mode=check
#
# [�f�B���N�g���\���� (���������̓p�[�~�b�V����)]
#
#    public_html / index.html(�����ɃJ�E���^����\��)
#          |
#          +-- count [777] / dream.cgi  [755]
#                |           gifcat.pl  [644]
#                |           index.dat  [666] .. ���O�t�@�C��1
#                |           index2.dat [666] .. ���O�t�@�C��2
#                |              :                    :
#                |           xxxxx.dat  [666] .. ���O�t�@�C��x
#                |
#                +-- gif1 / 0.gif .. 9.gif, a.gif, p.gif, c.gif, d.gif
#                |
#                +-- gif2 / 0.gif .. 9.gif, a.gif, p.gif, c.gif, d.gif
#                     :

#============#
#  �ݒ荀��  #
#============#

# �摜�A�����C�u�����捞��
require './gifcat.pl';

# IP�A�h���X�̃`�F�b�N (0=no 1=yes) 
#   �� yes�̏ꍇ�A������IP�A�h���X�̓J�E���g�A�b�v���Ȃ�
$ip_chk = 1;

# ���O�̎������� (0=no 1=yes)
$id_creat = 0;

# ���O��u���T�[�o�f�B���N�g��
#   �� ���s�f�B���N�g���ł���΂��̂܂܂ł悢
#   �� �Ō�͕K�� / �ŕ���
#   �� �t���p�X�Ȃ� / ����n�߂�ihttp://����ł͂Ȃ��j
$LogDir = './';

# �t�@�C�����b�N�`�� (0=no 1=symlink�֐� 2=open�֐�)
$lockkey = 0;

# ���b�N�t�@�C���̃T�[�o�f�B���N�g��
#   �� ���s�f�B���N�g���ł���΂��̂܂܂ł悢
#   �� �Ō�͕K�� / �ŕ���
#   �� �t���p�X�Ȃ� / ����n�߂�ihttp://����ł͂Ȃ��j
$LockDir = './';

# �摜�̂���T�[�o�f�B���N�g���̎w��
#   �� �t���p�X�Ȃ� / ����n�߂�ihttp://����ł͂Ȃ��j
sub gif_path {
	$gifdir  = "./gif$gif"; # gif�摜�̂���f�B���N�g���̃p�X
	$defodir = "./gif1";	# �f�t�H���g�i�����l�j�̃f�B���N�g��
}

# ���T�C�g����A�N�Z�X��r������ꍇ
#   �� dream.cgi��ݒu����URL�� http://����L�q
$base_url = "";

#============#
#  �ݒ芮��  #
#============#

# ���T�C�g����̃A�N�Z�X��r��
if ($base_url) {
	$ref_url = $ENV{'HTTP_REFERER'};
	$ref_url =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	if ($ref_url !~ /$base_url/i) { &error; }
}

# �f�R�[�h����
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
# �������Ȃ���΃����_�����[�h
else {
	$mode = 'rand';
}

# GIF�f�B���N�g�����`
&gif_path;

# �f�t�H���g�f�B���N�g�����`
if ($gif eq "") { $gifdir = $defodir; }

## ���ԏ���
if ($mode eq "time") {
	# ���Ԃ��擾
	&get_time;

	# 24���Ԑ��̏ꍇ
	if ($in{'type'} == 24) {
		($t1,$t2) = split(//, $hour);
		($t3,$t4) = split(//, $min);

		@caras = ("$t1","$t2","c","$t3","$t4");
	}
	# 12���Ԑ��̏ꍇ
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
## �J�����_����
elsif ($mode eq "date") {
	# ���Ԃ��擾
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

## �X�V���ԕ\������
elsif ($in{'file'}) {
	# �t�@�C�����Ȃ���΃G���[
	unless (-e $in{'file'}) { &error; }

	# �X�V�������擾
	($mtime) = (stat("$in{'file'}"))[9];

	# �X�V���Ԃ𕶎�����
	&get_time($mtime);
	($y1,$y2,$y3,$y4) = split(//, $year);
	($mon1,$mon2) = split(//, $mon);
	($day1,$day2) = split(//, $mday);
	($hr1,$hr2)   = split(//, $hour);
	($min1,$min2) = split(//, $min);

	# �X���b�V�� "/" ���Ȃ���΃_�b�V�� "-" �ő�p
	if (-e "$gifdir\/s.gif") { $s = 's'; }
	else { $s = 'd'; }

	# �z��
	@caras = ("$y1","$y2","$y3","$y4","$s","$mon1","$mon2","$s",
			"$day1","$day2","d","$hr1","$hr2","c","$min1","$min2");
}

## �t�@�C���T�C�Y���\������
elsif ($in{'size'}) {
	# �t�@�C�����Ȃ���΃G���[
	unless (-e $in{'size'}) { &error; }

	# �T�C�Y�����擾 (bytes)
	($size) = (stat("$in{'size'}"))[7];

	# �P�ʕϊ��i�l�̌ܓ��j
	if ($in{'p'} eq 'k') { $size = int ($size / 1024 +0.5); }
	elsif ($in{'p'} eq 'm') { $size = int ($size / 1048576 +0.5); }

	# �T�C�Y����z��
	@caras=();
	foreach (0 .. length($size)-1) {
		$n = substr($size,$_,1);
		push(@caras,$n);
	}
}
## �`�F�b�N���[�h
elsif ($mode eq "check") {
	&check;
}

## �J�E���^����
if ($id ne "" && $mode ne "rand") {
	# ���O���`
	$logfile = "$LogDir$id\.dat";

	# ���O�̑��݂��`�F�b�N
	unless(-e $logfile) {
		# ���O���� [�Ȃ�] �Ȃ�v���O�������I��
		if ($id_creat == 0) { &error; }

		# ���O���� [����] �Ȃ烍�O�𐶐�
		else {
			open(OUT,">$logfile") || &error;
			print OUT "0";
			close(OUT);

			# �p�[�~�b�V������ 666 ��
			chmod (0666,"$logfile");
		}
	}

 	# ���b�N�t�@�C�������`
	$lockfile = "$LockDir$id\.lock";

	# �f�t�H���g�������`
	if ($fig eq "") { $fig = 5; }

	# IP�A�h���X���擾
	$addr = $ENV{'REMOTE_ADDR'};

	# ���b�N�J�n
	if ($lockkey == 1) { &lock1; }
	elsif ($lockkey == 2) { &lock2; }

	# �L�^�t�@�C������ǂݍ���
	open(IN,"$logfile") || &error;
	$data = <IN>;
	close(IN);

	# �O�o�[�W�����ϊ�����
	if ($data =~ /<>/) { ($daykey,$data) = split(/<>/, $data); }

	# �L�^�t�@�C���𕪉�
	($count,$ip) = split(/:/, $data);

	# IP�`�F�b�N
	$flag=0;
	if ($ip_chk && $addr eq "$ip") { $flag=1; }

	# ���O�X�V
	if (!$flag) {
		# �J�E���g�A�b�v
		$count++;

		# �t�@�C�����t�H�[�}�b�g
		if ($ip_chk) { $data = "$count\:$addr"; }
		else { $data = "$count"; }

		# �L�^�t�@�C�����X�V����
		open(OUT,">$logfile") || &error;
		print OUT $data;
		close(OUT);
	}

	# ���b�N����
	if (-e $lockfile) { unlink($lockfile); }
}

## ��������
if ($mode eq "rand") {
	srand;
	$count = rand;
	$count = int($count * 10000);

	# �f�t�H���g�������`
	if ($fig eq "") { $fig = 5; }
}

## GIF�摜���o��
&count_view;
exit;

#---------------#
#  GIF�o�͏���  #
#---------------#
sub count_view {
	# ���ԕ\������уJ�����_�\������
	if ($mode eq "time" || $mode eq "date" || $in{'file'} || $in{'size'}) {
		@GIF = ();
		foreach (0 .. $#caras) { push(@GIF, "$gifdir/$caras[$_].gif"); }
	}

	# �J�E���^�\������
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
#  ���b�N�t�@�C�������Fsymlink�֐�  #
#-----------------------------------#
sub lock1 {
	local($retry) = 5;
	while (!symlink(".", $lockfile)) {
		if (--$retry <= 0) { &error; }
		sleep(1);
	}
}

#--------------------------------#
#  ���b�N�t�@�C�������Fopen�֐�  #
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
#  ���Ԃ��擾  #
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
#  �G���[����  #
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
#  �`�F�b�N���[�h  #
#------------------#
sub check {
	print "Content-type: text/html\n\n";
	print "<html><head><title>DREAM COUNTER</title></head>\n";
	print "<body>\n<h2>Check Mode</h2>\n<UL>\n";

	# ���O�t�@�C������
	opendir(DIR,"$LogDir")
		|| print "<LI>�f�B���N�g����F���ł��܂���: $LogDir\n";
#	@dir = readdir(DIR);
	@dir = grep { /\.dat$/ && -f "$LogDir$_" } readdir(DIR);
	closedir(DIR);

	$flag=0;
	foreach (@dir) {
		$target = "$LogDir$_";
#		if (-d "$LogDir$_") { next; }
#		if ($_ !~ /(.+)\.dat$/) { next; }

		if (-r $target && -w $target) { print "<LI>$_ : �p�[�~�b�V����OK \n"; }
		elsif (!-r $target) { print "<LI>$_ : �Ǎ��݃p�[�~�b�V����NG \n"; }
		elsif (!-w $target) { print "<LI>$_ : �����݃p�[�~�b�V����NG \n"; }
		$flag=1;
	}
	if (!$flag) { print "<LI>���O�t�@�C�������݂��܂���\n"; }

	if ($gif ne "") { $target_dir = $gifdir; }
	else { $target_dir = $defodir; }

	# �摜�f�B���N�g���̃p�X�m�F
	if (-d $target_dir) { print "<LI>$target_dir : �摜�f�B���N�g���̃p�X : OK! \n"; }
	else { print "<LI>$target_dir : �摜�f�B���N�g��������܂���\n"; }

	# �摜�`�F�b�N
	@GifFile = ("0".."9", "a", "p", "c", "d");
	foreach (@GifFile) {
		$target = "$target_dir\/$_\.gif";
		if (-e "$target") { print "<LI>$target : �摜OK \n"; }
		else { print "<LI>$target : �摜������܂���\n"; }
	}

	# ���쌠�\���F�폜���ς��֎~���܂�
	print "</UL>\n<P><small><!-- $ver -->\n";
	print "Copyright(C) <a href='http://www.kent-web.com/' target='_top'>Kent Web</a> 2001\n";
	print "</small>\n</body></html>\n";
	exit;
}
