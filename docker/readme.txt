��Youtube�`�����l�����ꗗ
�o�[�`����Youtuber�̃����L���O�����Q�Ƃł���UserLocal(https://virtual-youtuber.userlocal.jp/)�ɑ΂���python�X�N���v�g�ŃX�N���C�s���O���s���A
�X�N���C�s���O���ʂ����Youtube Data API�Ŏ擾�����`�����l�������x�[�V�b�N��Lamp���ŕ\������c�[���ł��B

readme.txt�̂���f�B���N�g���ňȉ��̃R�}���h�����s���Ă��������B
�Ȃ��A�菇2�ɂ��Ă͊O���iUserLocal�̕\���ύX�AYoutube Data API�̎g�p�ʐ����j�ɂ���Ď��s���邽�߁A
�\��MySQL�Ƀf�[�^�͓������Ă���A��΂��Ă���肠��܂���B


1.Docker���\�z
docker-compose up -d --build


2.python�̊���ŃX�N���v�g�����s
docker-compose exec python bash
python GetYoutubeStatistics.py

���X�N���C�s���O�y��Youtube API���ʂɍs�����ߔ��Ɏ��Ԃ�������܂��B
��MySQL�������オ�肫���Ă��Ȃ��ꍇ�̓G���[���������܂��B


3.Web�u���E�U�ňȉ��̃A�h���X�ɃA�N�Z�X���ăo�[�`����Youtuber�����ꗗ�\��
http://localhost:80

