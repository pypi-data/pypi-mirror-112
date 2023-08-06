#ifndef __XLDT_DOC_H__
#define __XLDT_DOC_H__

#ifndef PyDoc_STRVAR
#error The Python header was not included or it's too old.
#endif

PyDoc_STRVAR(xldt__doc__,
"Excel compatible date and time helper functions for Python.\n\n\
This module manipulates date and time by using serial numbers, like\n\
Microsoft Excel. The serial numbers are identical between this module\n\
and Excel for dates starting with 1900-03-01 in the 1900 date system.");

PyDoc_STRVAR(xldt_date__doc__,
"date(year: float, month: float, day: float) -> float\n\n\
Return the value corresponding to the given date. The month and the\n\
day are optional, defaulting to 1.");

PyDoc_STRVAR(xldt_day__doc__,
"day(value: float) -> int\n\n\
Return the day (1 - 31) of month of the date corresponding to the\n\
given value.");

PyDoc_STRVAR(xldt_days__doc__,
"days(start_date: float, end_date: float) -> int\n\n\
Calculate the number of days between two dates.");

PyDoc_STRVAR(xldt_hour__doc__,
"hour(value: float) -> int\n\n\
Return the hour (0 - 23) corresponding to the given value.");

PyDoc_STRVAR(xldt_isweekend__doc__,
"isweekend(value: float, result_type: int) -> bool\n\n\
Return True if the date corresponding to the given value is a weekend.\n\
The optional result_type argument controls which of the days in a week\n\
are considered weekend. It can take on any of the constants:\n\
* WE_SAT_SUN - Saturday and Sunday are weekend (this is the default)\n\
* WE_SUN_MON - Sunday and Monday are weekend\n\
* WE_MON_TUE - Monday and Tuesday are weekend\n\
* WE_TUE_WED - Tuesday and Wednesday are weekend\n\
* WE_WED_THU - Wednesday and Thursday are weekend\n\
* WE_THU_FRI - Thursday and Friday are weekend\n\
* WE_FRI_SAT - Friday and Saturday are weekend\n\
* WE_SUN - Only Sunday is weekend\n\
* WE_MON - Only Monday is weekend\n\
* WE_TUE - Only Tuesday is weekend\n\
* WE_WED - Only Wednesday is weekend\n\
* WE_THU - Only Thursday is weekend\n\
* WE_FRI - Only Friday is weekend\n\
* WE_SAT - Only Saturday is weekend\n\
The result_type can also be a seven character string representing the\n\
days of the week starting with Monday, each character can be 1 for the\n\
weekend or 0 for a workday.\n\
The values of the constants are identical to those used by Excel with\n\
WORKDAY.INTL and could be used to implement equivalent functions in\n\
Python.");

PyDoc_STRVAR(xldt_isoweek__doc__,
"isoweek(serial: float) -> int\n\n\
Return the ISO week number of the year for a given date.\n\
It behaves like Excel's ISOWEEKNUM function.");

PyDoc_STRVAR(xldt_minute__doc__,
"minute(value: float) -> int\n\n\
Return the minute (0 - 59) corresponding to the given value.");

PyDoc_STRVAR(xldt_month__doc__,
"month(value: float) -> int\n\n\
Return the month (1 - 12) of the date corresponding to the given value.");

PyDoc_STRVAR(xldt_months__doc__,
"months(start_date: float, end_date: float) -> int\n\n\
Calculate the number of full months between the dates corresponding to\n\
the given values.");

PyDoc_STRVAR(xldt_now__doc__,
"now() -> float\n\n\
Return the value corresponding to the current local date and time.");

PyDoc_STRVAR(xldt_second__doc__,
"second(value: float) -> int\n\n\
Return the second (0 - 59) corresponding to the given value.");

PyDoc_STRVAR(xldt_time__doc__,
"time(hour: float, minute: float, second: float) -> float\n\n\
Return the value corresponding to the given time of the day. The \n\
minute and the second are optional, defaulting to 0.");

PyDoc_STRVAR(xldt_today__doc__,
"today() -> int\n\n\
Return the value corresponding to the current date (without time).");

PyDoc_STRVAR(xldt_week__doc__,
"week(serial: float, result_type: int) -> int\n\n\
Return the week number corresponding to the given serial number. The\n\
result_type argument is optional. It can take on any of the constants:\n\
* SUN_1 - The week begins on Sunday (this is the default)\n\
* MON_1 - The week begins on Monday\n\
* MON_1_EXT - The week begins on Monday\n\
* TUE_1_EXT - The week begins on Tuesday\n\
* WED_1_EXT - The week begins on Wednesday\n\
* THU_1_EXT - The week begins on Thursday\n\
* FRI_1_EXT - The week begins on Friday\n\
* SAT_1_EXT - The week begins on Saturday\n\
* SUN_1_EXT - The week begins on Sunday\n\
For the constants above, the first week of the year (numbered 1) is the\n\
week containing the 1st January.\n\
* MON_2 - The week begins on Monday\n\
For the constant MON_2, the week containing the first Thursday of the\n\
year is the first week of the year and is numbered as week 1.\n\
This function behaves like Excel's WEEKNUM function.");

PyDoc_STRVAR(xldt_weekday__doc__,
"weekday(value: float, result_type: float) -> int\n\n\
Return the weekday corresponding to the given value. The result_type\n\
argument is optional. It can take on any of the constants:\n\
* SUN_1 - The week begins on Sunday (this is the default)\n\
* MON_1 - The week begins on Monday\n\
* MON_1_EXT - The week begins on Monday\n\
* TUE_1_EXT - The week begins on Tuesday\n\
* WED_1_EXT - The week begins on Wednesday\n\
* THU_1_EXT - The week begins on Thursday\n\
* FRI_1_EXT - The week begins on Friday\n\
* SAT_1_EXT - The week begins on Saturday\n\
* SUN_1_EXT - The week begins on Sunday\n\
For the constants above, the first day of the week is numbered 1.\n\
* MON_0 - The week begins on Monday. The first day is numbered 0.\n\
This function behaves like Excel's WEEKDAY function.");

PyDoc_STRVAR(xldt_year__doc__,
"year(value: float) -> int\n\n\
Return the year of the date corresponding to the given value.");

PyDoc_STRVAR(xldt_years__doc__,
"years(start_date: float, end_date: float) -> int\n\n\
Calculate the number of full years between the dates corresponding to\n\
the given values.");

#endif
