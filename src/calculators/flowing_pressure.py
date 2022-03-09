from typing import Optional
from math import sin, pi

GRAVITY = 9.81


# TODO: тегом #CUT помечены строки, которые потом можно будет убрать для полуготового задания

class FPCalculator:
    """
    Класс-калькулятор забойного давления в скважине с ЭЦН
    """

    def __init__(self, md_bh: float, angle: float, md_esp: float,
                 rho_wat: Optional[float] = 1000, rho_oil: Optional[float] = 800):
        """
        Конструктор, создающий объект расчётника

        :param md_bh: измеренная по стволу глубина забоя скважина, м
        :param angle: угол искривления ствола скважины от горизонтали, % - const по стволу
        :param rho_wat: плотность воды, кг/м3
        :param rho_oil: плотность нефти, кг/м3
        """
        self.rho_wat = rho_wat
        self.rho_oil = rho_oil
        self.angle = angle  # CUT
        self.tvd_bh = self.md_to_tvd(md_bh, angle)  # CUT
        self.tvd_esp = self.md_to_tvd(md_esp, angle)

    @staticmethod
    def md_to_tvd(value, angle):
        return value * sin(angle * pi / 180)

    def rho_liq(self, wct):
        return self.rho_wat * wct / 100 + self.rho_oil * (1 - wct / 100)  # CUT

    @staticmethod
    def pa_to_atm(value):
        return value / 101325

    def calc_fp(self, p_wh: float, wct: float, h_dyn: Optional[float] = None, p_int: Optional[float] = None) -> float:
        """
        Метод, выполняющий расчёт забойного давления в скважине с ЭЦН

        :param p_wh: давление на устье (буферное), атм
        :param wct: обводненность жидкости, %
        :param h_dyn: динамический уровень, м
        :param p_int: давление на приеме насоса, атм
        :return: давление на забое, атм
        """
        if p_int is None:
            if h_dyn is None:  # CUT
                raise ValueError("Не задано давление на приеме и динамический уровень, расчёт невозможен")  # CUT
            fp = p_wh + self.pa_to_atm(
                (self.tvd_bh - self.md_to_tvd(h_dyn, self.angle)) * self.rho_liq(wct) * GRAVITY)  # CUT
        else:
            fp = p_int + self.pa_to_atm((self.tvd_bh - self.tvd_esp) * self.rho_liq(wct) * GRAVITY)  # CUT
        return fp
