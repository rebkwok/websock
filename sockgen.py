#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Pattern_info(object):

    def __init__(self, data):
        self.units = data.get("units", "inches")
        self.unit = "inch" if self.units == "inches" else "cm"
        self.unit_abbr = '"' if self.units == "inches" else "cm"
        self.stitches = data.get("stitches", 36.0)
        self.rows = data.get("rows", 40.0)
        self.ease = data.get("ease", -8.0)

        if self.units == "inches":
            self.st_gauge = self.stitches / 4
            self.r_gauge = self.rows / 4
        elif self.units == "cms":
            self.st_gauge = self.stitches / 10
            self.r_gauge = self.rows / 10
        else:
            raise Exception(f"unknown units {self.units}")


def cast_on_stitches(pattern_info, foot_circum, divisible_by=1):
    """
    Calculates number of stitches to provisionally cast on to start short row
    toe.
    Ease should be entered as a percentage, negative or positive (usually
    negative for socks).
    """
    sock_circum = foot_circum + (foot_circum * (pattern_info.ease / 100))
    cast_on = (sock_circum * pattern_info.st_gauge) / 2
    cast_on_rounded = round(cast_on / divisible_by) * divisible_by
    return cast_on_rounded


def short_row_end_stitches(cast_on_sts, percent_end):
    """
    Calcuates number of stitches at end of short row toe or heel; this number
    is even if the number of toe/heel stitches is even,
    and odd if the number of toe/heel stitches is odd.
    percent_end is the percentage of stitches at the end of toe/heel (usually
    40% for toe and 50% for heel)
    """

    percent_end = float(percent_end)
    x = round(cast_on_sts * (percent_end/100))

    if cast_on_sts % 2 == 0:  # if starting stitches are an even number
        if x % 2 == 0:
            return x
        else:
            if x > cast_on_sts * percent_end:
                return x - 1
            else:
                return x + 1
    else:  # if starting stitches are an odd number
        if x % 2 == 0:
            if x >= cast_on_sts * percent_end:
                return x + 1
            else:
                return x - 1
        else:
            return x


def short_row_length(cast_on_sts, short_row_end_stitches, pattern_info):
    """
    Calculate length of the short row toe or heel.
    """
    short_rows = cast_on_sts - short_row_end_stitches
    sr_length = short_rows / pattern_info.r_gauge
    return sr_length


def calculate_gusset(pattern_info, additional_instep):
    """
    :param additional_instep: in ins/cms, amount of extra measurement in the
    instep compared to ball of foot
    :return: number of gusset sts needed, length of gusset in ins/cms
    """
    # additional instep circumference with ease calculated
    sock_gusset = additional_instep + \
        (additional_instep * (pattern_info.ease / 100))
    gusset_sts_raw = sock_gusset * pattern_info.st_gauge
    # Round to nearest even number
    gusset_sts = round(gusset_sts_raw / 2) * 2
    # calculate gusset length; gusset will be increased 2 sts every other row
    gusset_length = gusset_sts / pattern_info.r_gauge

    return gusset_sts, gusset_length


def pattern(pattern_info, foot_circum, foot_length, instep_circum, divisible_by):

    cast_on = cast_on_stitches(pattern_info, foot_circum, divisible_by)
    heel_end = short_row_end_stitches(cast_on, 50)
    toe_end = short_row_end_stitches(cast_on, 40)
    gusset_sts, gusset_length = calculate_gusset(
        pattern_info, instep_circum - foot_circum
    )
    heel_length = short_row_length(cast_on + gusset_sts, heel_end, pattern_info)
    foot_length_before_gusset = foot_length - heel_length - gusset_length

    return {
        'cast_on': cast_on,
        'heel_end': heel_end,
        'toe_end': toe_end,
        'heel_length': heel_length,
        'gusset_sts': gusset_sts,
        'heel_sts': cast_on + gusset_sts,
        'foot_length_before_gusset': foot_length_before_gusset
    }


def main():
    pass


if __name__ == '__main__':
    main()