#include "stm32f1xx_hal.h"
#include "gpio.h"
#include "uart.h"

int main(void) {
    HAL_Init();
    SystemClock_Config();
    MX_GPIO_Init();
    MX_UART1_Init();

    while (1) {
        if (HAL_UART_Receive_IT(&huart1, &rxData, 1) == HAL_OK) {
            HAL_UART_Transmit_IT(&huart1, &rxData, 1);
        }
    }
}