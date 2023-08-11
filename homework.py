from dataclasses import dataclass, asdict
from typing import ClassVar, Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.message.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP: ClassVar[float] = 0.65  # Шаги в метрах
    M_IN_KM: ClassVar[float] = 1000.0  # перевод метров в километры
    M_IN_H: ClassVar[float] = 60.0  # перевод минут в часы
    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Необходимо определить '
                                  'количество затраченных калорий')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


@dataclass
class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: ClassVar[float] = 18
    CALORIES_MEAN_SPEED_SHIFT: ClassVar[float] = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                / self.M_IN_KM * self.duration * self.M_IN_H)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEF_1: ClassVar[float] = 0.035
    COEF_2: ClassVar[float] = 0.029
    KMH_TO_MS: ClassVar[float] = 0.278
    H_TO_M: ClassVar[float] = 100.0
    action: int
    duration: float
    weight: float
    height: float

    def get_spent_calories(self) -> float:
        return (((self.COEF_1 * self.weight
                  + (((self.get_mean_speed() * self.KMH_TO_MS) ** 2)
                     / (self.height / self.H_TO_M))
                  * self.COEF_2 * self.weight))
                * self.M_IN_H * self.duration)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: ClassVar[float] = 1.38
    CALORIES_MEAN_SPEED: ClassVar[float] = 1.1
    CALORIES_WEIGHT_MULTIPLIER: ClassVar[float] = 2.0
    action: int
    duration: float
    weight: float
    length_pool: float
    count_pool: float

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения при плавании."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.CALORIES_MEAN_SPEED)
                * self.CALORIES_WEIGHT_MULTIPLIER
                * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout: Dict[str, Type[Training]] = {'SWM': Swimming,
                                          'RUN': Running,
                                          'WLK': SportsWalking}

    if workout_type in workout:
        return workout[workout_type](*data)
    raise ValueError(f'Тренировки - {workout_type}, не предусмотрено.')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
