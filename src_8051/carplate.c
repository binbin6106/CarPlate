#include <intrins.h>
#include "stc89c52rc.h"
typedef unsigned char uchar;
#define FOSC 11059200L
#define BAUD 9600
bit busy;
bit is_work;
bit manual_mode;
sbit PWM = P1^1;
uchar time;
uchar gan;

void open_the_door();
void close_the_door();
void stop_work();
void start_work();
void manual_open();
void manual_close();
void alawys_open();

void init_external_interrupt() //�ⲿ�ж���ؼĴ�����ʼ������
{
	IT0 = 1;
	IT1 = 1; //�����ⲿ�жϷ�ʽ��Ϊ�½��ش���	
	EX0 = 1;
	EX1 = 1; //����0��1�ⲿ�ж�
}

void UartInit(void)		//9600bps@11.0592MHz
{
	SCON = 0x50;		//8λ����,�ɱ䲨����
	TMOD = 0x20;		//�趨��ʱ��1Ϊ8λ�Զ���װ��ʽ
	TL1 = TH1 = -(FOSC/12/32/BAUD);
	TR1 = 1;		//������ʱ��1
	ES = 1;
}

void pwm_init()
{	
	TMOD=0x21;//��ʱ��0������ʽ1	 
	TH0=(65536-46)/256;//����ֵ��ʱ	 
	TL0=(65536-46)%256;//1ms
//	TL0 = 0x5C;		//���ö�ʱ��ֵ
//	TH0 = 0xF7;		//���ö�ʱ��ֵ	
}

void judge(uchar dat)
{
	switch(dat)
	{
		case 0x00: open_the_door();break;
		case 0x01: close_the_door();break;
		case 0x02: start_work();break;
		case 0x03: stop_work();break;
		case 0x04: manual_open();break;
		case 0x05: alawys_open();break;
		default: break;
	}
}
void open_the_door()
{
	gan = 21;
}

void close_the_door()
{
	gan = 29;
}

void start_work()
{
	close_the_door();
	is_work = 1;
	manual_mode = 0;
}

void stop_work()
{
	is_work = 0;
}

void manual_open()
{
	manual_mode = 1;
	open_the_door();	
}

//void manual_close()
//{
//	close_the_door();	
//}

void alawys_open()
{
	is_work = 0;
	open_the_door();
}

void SendData(uchar dat)
{
	while(busy);
	busy = 1;
	SBUF = dat;
}

//void SendString(char *s)
//{
//	while(*s)
//	{
//		SendData(*s++);
//	}
//}

void main()
{
	init_external_interrupt();
	UartInit();
	pwm_init();
	//IPH = 0x12;
	IP = 0x15;
	EA = 1; //�������ж�
	ET0=1;//����ʱ��0�ж� 
	TR0=1;//������ʱ��0
	close_the_door();
	while(1)
	{
	}	
}


void tim0() interrupt 1
{
	TR0=0;//����ֵʱ���رն�ʱ�� 
	TH0=(65536-46)/256;//����ֵ��ʱ	 
	TL0=(65536-46)%256;//0.2ms 
//	TL0 = 0x5C;		//���ö�ʱ��ֵ
//	TH0 = 0xF7;		//���ö�ʱ��ֵ
	TR0=1;//�򿪶�ʱ��  
	time++; 
	if(time>=400) //50hz 
		time=0; 
	if(time<=gan) //ռ�ձ�̧��21�����29
		PWM=1; 
	else 
		PWM=0; 
}
 
void Uart_interrupt() interrupt 4 using 1
{
	if(RI) //���մ����ж�
	{
	   uchar dat;
	   RI = 0;
	   dat = SBUF;
	   judge(dat);
	}
	if(TI) //���ʹ����ж�
	{
	   TI = 0;
	   busy = 0;
	}
}
void ext0_interrupt() interrupt 0 //�����ⲿ�ж�0��������������⵽��̧��
{
	if(is_work && !manual_mode)
	{
		SendData(0xff);
	}
}

void ext1_interrupt() interrupt 2 //�����ⲿ�ж�1��������������⵽���뿪
{
	if(is_work)
	{
		close_the_door();
	}
}