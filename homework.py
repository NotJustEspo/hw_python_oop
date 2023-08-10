class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65  # Шаги в метрах
    M_IN_KM: float = 1000  # перевод метров в километры
    M_IN_H: float = 60  # перевод минут в часы

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)
        self.speed = Training.get_mean_speed(self)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.speed
                 + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                / self.M_IN_KM * self.duration * self.M_IN_H)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEF_1: float = 0.035
    COEF_2: float = 0.029
    KMH_TO_MS: float = 0.278
    H_TO_M: float = 100

    def __init__(self, action: int, duration: float, weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height
        self.speed = Training.get_mean_speed(self)

    def get_spent_calories(self) -> float:
        return (((self.COEF_1 * self.weight
                  + (((self.speed * self.KMH_TO_MS) ** 2)
                     / (self.height / self.H_TO_M))
                  * self.COEF_2 * self.weight))
                * self.M_IN_H * self.duration)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    AVG_CONST: float = 1.1
    SPEED_CONST: float = 2

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: float, count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения при плавании."""

        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return (self.get_mean_speed() + self.AVG_CONST) * self.SPEED_CONST \
            * self.weight * self.duration


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    workout_dict = {'SWM': Swimming,
                    'RUN': Running,
                    'WLK': SportsWalking}

    if workout_type in workout_dict:
        return workout_dict[workout_type](*data)
    print('Такой тренировки не предусмотрено')


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
