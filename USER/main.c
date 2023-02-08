//////////////////////////////////////////////////////////////////////////////////	 
//  文 件 名   : main.c
//  版 本 号   : v2.0
//  作    者   : luxban
//  生成日期   : 2022-6-01
//  最近修改   : 
//  功能描述   :演示例程(STM32F103系列)
//              接口说明: 
//              LED:PA8
//   
//              TFT-LCD: 
//              GND   电源地
//              VCC   3.3v电源
//              SCL   PB4（SCLK）
//              SDA   PB5（MOSI）
//              RES   PB6
//              DC    PB7
//              CS    PB8
//              BLK   PB9
//              ----------------------------------------------------------------
//******************************************************************************/
#include "delay.h"
#include "sys.h"
#include "led.h"
#include "lcd_init.h"
#include "lcd.h"
#include "pic.h"
#include "usart.h"

typedef union float_data{
	float f_data;
	u8 byte[4];
}MyFloat;

void MyLCD_ShowStr(u16 len,u16 fc,u16 bc,u8 sizey,u8 mode);

uint16_t Sentback = 0;
MyFloat SentbackF;
u8* pfloat = (void*)(&SentbackF);
// uint16_t temp;
int main(void)
{
	u32 temp = 0xff000000;
	u16 len=0;
	u16 t;
	
	//float t=0;
	delay_init();
	LED_Init();//LED初始化
	LCD_Init();//LCD初始化
	uart_init(9600); //
	LCD_Fill(0,0,LCD_W,LCD_H,BLACK);
	LCD_ShowPicture(0,0,128,111,gImage_1);
	while(1)
	{
		// LCD_ShowPicture(1,1,126,127,gImage_2);
		// LCD_ShowFloatNum1(20,130,t,4,RED,WHITE,16);
		if((USART_RX_STA&0x8000)){
			// LCD_Fill(0,0,128,128,BLACK);
			len = USART_RX_STA&0x3fff;
			Sentback = 0;
			/*
			for(t=0;t<len;t++){
				//Sentback += (USART_RX_BUF[t]<<(8*t));
				*(pfloat+t) = USART_RX_BUF[t];
			}
			*/
			/*
			if(len==4){
				for(t=0;t<len;t++){
					SentbackF.byte[t]=USART_RX_BUF[t];
				}
			}
			*/
			
			MyLCD_ShowStr(len,BLUE,BLACK,12,0);
			
			USART_RX_STA = 0;
		}
		// LCD_ShowIntNum(0,0,Sentback,8,RED,WHITE,16,0); // uint16  1:without backcolor,0 with bc
	//	LCD_ShowFloatNum1(0,0,SentbackF.f_data,10,RED,BLACK,16);
	//	LCD_ShowIntNum(0,32,SentbackF.byte[3],3,BLUE,WHITE,16,0);
	//	LCD_ShowIntNum(30,32,SentbackF.byte[2],3,BLUE,WHITE,16,0);
	//	LCD_ShowIntNum(60,32,SentbackF.byte[1],3,BLUE,WHITE,16,0);
		//LCD_ShowIntNum(90,32,SentbackF.byte[0],3,BLUE,WHITE,16,0);
		LCD_ShowIntNum(0,110,len,8,RED,BLACK,16,0);
	}
}


void USART1_IRQHandler(void){
	u8 Res;
	if(USART_GetITStatus(USART1, USART_IT_RXNE) != RESET)
	{
		LED = ~LED;
		Res = USART_ReceiveData(USART1);
		if((USART_RX_STA&0x8000)==0){
			if(USART_RX_STA&0x4000){
				if(Res!=0x0a)USART_RX_STA=0;//接收错误,重新开始
				else USART_RX_STA|=0x8000;	//接收完成了 
			}else{	
				if(Res==0x0d) USART_RX_STA|=0x4000;
				else{
					USART_RX_BUF[USART_RX_STA&0x3fff]=Res ;
					USART_RX_STA++;
					if((USART_RX_STA&0x3fff)>USART_REC_LEN-1) USART_RX_STA = 0; //接收数据错误,重新开始接收	  
				}		 
			}
		}
		LED=~LED;
	}	
}


void MyLCD_ShowStr(u16 len,u16 fc,u16 bc,u8 sizey,u8 mode){
	u16 t=0;
	u8 r=0;
	u16 x,y;
	for(;t<len;t++){
		x = 0;
		y = sizey*r;
		while(t<len && USART_RX_BUF[t]!='#'){
			LCD_ShowChar(x,y,USART_RX_BUF[t],fc,bc,sizey,mode);
			x+=sizey/2;
			if((x+3)>=LCD_W)
				break;
			t++;
		}
		while(x<LCD_W){
			LCD_ShowChar(x,y,' ',fc,bc,sizey,mode);
			x+=sizey/2;
		}
		r++;
	}
}