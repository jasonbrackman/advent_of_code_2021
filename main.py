import day_01
import day_02
import day_03
import day_04
import day_05
import day_06
import day_07

import helpers


if __name__ == "__main__":
    helpers.time_it_all(
        [
            day_01.run,
            day_02.run,
            day_03.run,
            day_04.run,
            day_05.run,
            day_06.run,
            day_07.run,
        ]
    )
