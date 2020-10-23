#!/usr/bin/perl
#�n���X�^�[�J�E���^(GIF+fly)��(c)p4room(http://p4room.mda.or.jp/)
#Modified by SHIRO (http://www.kyoshin-sj.co.jp/oyama/�j

$fly = "./fly";			#fly�R�}���h
$tmpdir = "./tmp";			#�ꎞ�I�Ƀt�@�C�������f�B���N�g��

### �J�E���g����

@urls = (				#�A�N�Z�X�𖳎������������N��URL
  "hogehoge.net",			#�J���}�ŋ�؂��ĕ����w��\
  "oyama/page1",			#��F"yahoo.co.jp",
);
$logfile = "./count.log";		#�J�E���^�ۑ��p�t�@�C��
$aclogfile ="./access.log";		#�A�N�Z�X�L�^�p�t�@�C��
$addr      = $ENV{'REMOTE_ADDR'};	#���K�҂̃z�X�g�A�h���X
$referer   = $ENV{'HTTP_REFERER'};	#�����N��URL
$keep      = 20;			#�A�N�Z�X�L�^�̕ۑ����ԁi�b�j
$now       = time;			#���݂̎���

open(FILE,"+<$aclogfile");		#�A�N�Z�X���O���J��
flock(FILE,2);				#���b�N����
@logs = <FILE>;				#�z��ɃA�N�Z�X�L�^��ǂݍ���
@logs = grep($_ > $now - $keep, @logs); #$keep�b�ȓ��̐V�A�N�Z�X�L�^�̂ݎc��
seek(FILE,0,0);				#�t�@�C���|�C���^��擪��
print FILE "$now\t$addr\n";		#����̃A�N�Z�X�L�^����������
print FILE @logs;			#@logs����������
truncate(FILE, tell);			#�]���ȃf�[�^��؂�l�߂�
close(FILE);				#�N���[�Y

open(FILE,"+<$logfile");		
flock(FILE,2);
chop($count = <FILE>);			#�J�E���^��ǂݍ���
if (&from_outside()) {			#�O������̃A�N�Z�X�ł���A
  if (&is_newcomer()) {			#�V�K�K��҂ɂ��A�N�Z�X�Ȃ�
    $count++;				#�J�E���^��+1����
    seek(FILE,0,0);			#�t�@�C���|�C���^��擪�ɖ߂�
    print FILE "$count\n";		#�J�E���^���t�@�C���ɏ����o��
  }
}
flock(FILE,8);				#���b�N����
close(FILE);				#�N���[�Y

$count = sprintf("%05d", $count);	#�Œ�5���ɐ��`����
@suuji = split(//, $count);		#�X�̐����ɕ���

### fly�R�}���h�𗘗p�����J�E���^�摜�̍쐬

unless (-x $fly) {			#fly�R�}���h�����s�ł��Ȃ����
  print "Location: bad.gif\n\n";	#���s�摜���o�͂��Ē��f
  exit;					#�X�N���v�g�I��
}

$imgfile = "$tmpdir/#$$.gif";		#�ꎞ�I�ɍ��摜�t�@�C����

$xsize = 16;				#�X�̐���GIF�̉���
$ysize = 33;				#�X�̐���GIF�̍���

open(FLY, "|$fly -q -o $imgfile");		#fly�R�}���h���N��
print FLY "new\n";				#������
print FLY "size 134,82\n";			#�w�i�摜�T�C�Y��ݒ�
print FLY "copy 0,0,-1,-1,-1,-1,backpic.gif\n";	#�w�i�摜���R�s�[
$x = (134 - $xsize * @suuji) / 2;		#�����J�n�ʒu
foreach $n (@suuji) {
  print FLY "copy $x,60,-1,-1,-1,-1,$n.gif\n";	#������z�u
  $x += $xsize;					#�����̕������E�Ɉړ�
}
print FLY "transparent 0,0,0\n";		#�����F��ݒ�iRGB=0,0,0)
close(FLY);					#fly�R�}���h�I���i�摜�쐬�����j

### �摜���o�͂��ďI��

$date = &gmt_date(time);		#���݂̎�����
print "Last-Modified: $date\n";		#�X�V�����Ƃ��ďo��
print "Expires: 0\n";			#�L��������0 (�L���b�V���Ȃ�)
print "Content-Type: image/gif\n\n";	#GIF�摜��HTTP�w�b�_���o��

open(FILE, $imgfile);			#�摜�t�@�C�����I�[�v��
print <FILE>;				#�S�f�[�^���o��
close(FILE);				#�t�@�C�����N���[�Y

unlink($imgfile);			#�摜�t�@�C�����폜

exit;					#�X�N���v�g�I��

### �ȉ��T�u���[�`��

sub from_outside {			#�O������̃A�N�Z�X���ǂ����`�F�b�N
  foreach $url (@urls){
	  if ($referer =~ /$url/) {	#�����̃y�[�W����̃A�N�Z�X�Ȃ�
	    return 0;			#0��Ԃ�
	  }
  }
  return 1;				#�����łȂ���ΊO������̃A�N�Z�X
}

sub is_newcomer {			#�V�K�A�N�Z�X���ǂ����`�F�b�N
  foreach $line (@logs){		#$keep�b�ȓ��̑S�L�^�𒲂ׂ�
	chop($line);
	($t, $a) = split(/\t/, $line);	#�����ƃz�X�g�A�h���X�ɕ���
	if ($addr eq $a) {		#�����z�X�g����̃A�N�Z�X�L�^������΂O��Ԃ�
		return 0;
	}
  }
  return 1;				#�����łȂ����1��Ԃ�
}

### ���E�W�����̕�����𓾂�

sub gmt_date {
  local($t) = @_;
  @wdays = ("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat");
  @month = ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec");
  ($sec, $min, $hour, $day, $mon, $year, $wday) = gmtime($t);
  return sprintf("%s, %02d %s %04d %02d:%02d:%02d GMT",
           $wdays[$wday], $day, $month[$mon], $year+1900, $hour, $min, $sec);
}