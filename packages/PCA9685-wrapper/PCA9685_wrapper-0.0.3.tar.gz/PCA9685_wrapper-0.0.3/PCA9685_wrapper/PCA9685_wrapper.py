# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import atexit
from logging import DEBUG, INFO, WARN, Formatter, StreamHandler, getLogger

import Adafruit_PCA9685


class PWM:
    """python3でPCA9685でPWMを出力するサンプル
    """

    def __init__(self, channel: int):
        """PWM出力の初期化

        Args:
            channel (int): チャンネルごとにインスタンス化する

        Raises:
            ValueError: 16チャンネル以外はエラーを送出
        """

        # 16チャンネルであるのでそれ以外を指定した場合エラーを送出する
        if 0 <= channel <= 15:
            self.channel = channel
        else:
            raise ValueError("存在しないチャンネルを指定しています")

        # initialize PCA9685
        self.mPwm = Adafruit_PCA9685.PCA9685(address=0x40)

        # 60Hzにするとうまくいくらしい、なぜ？
        self.mPwm.set_pwm_freq(60)

        # パルスの最小最大値を設定する
        self.min_pulse = 0
        self.max_pulse = 4095

        # ロガーの設定
        self.init_logger(WARN)

        # 終了時に全出力を切る
        atexit.register(self.cleanup)

    def init_logger(self, level):
        """ロガーの初期化

        Args:
            level (loggingのレベル): INFO,WARN等で指定
        """

        self.logger = getLogger(__name__)
        self.logger.propagate = False
        self.logger.setLevel(level)

        handler = StreamHandler()
        handler.setFormatter(
            Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        handler.setLevel(DEBUG)
        self.logger.addHandler(handler)

    def setPWM(self, pulse: int):
        """pwm出力を設定する関数

        Args:
            pulse (int): 0-4095までのduty比
        """
        # int型以外が入力された場合は出力を0
        if not isinstance(pulse, int):
            self.logger.warning(
                f'{pulse=}はint型ではないため出力を最小値に設定します')
            pulse = self.min_pulse

        # 最小値より小さい値が入力された場合は出力を最小値
        elif pulse < self.min_pulse:
            self.logger.warning(
                f'{pulse=}は{self.min_pulse=}より小さいため出力を最小値に設定します')
            pulse = self.min_pulse

        # 最大値より大さい値が入力された場合は出力を最大値
        elif pulse > self.max_pulse:
            self.logger.warning(
                f'{pulse=}は{self.max_pulse=}より大きいため出力を最大値に設定します')
            pulse = self.max_pulse

        # 問題がなければそのまま
        else:
            pass
        
        # pwm出力
        self.mPwm.set_pwm(self.channel, 0, pulse)

    def cleanup(self):
        """出力を切る関数
        """
        self.setPWM(0)
