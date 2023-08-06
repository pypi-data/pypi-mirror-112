#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <time.h>

#include "xldt_doc.h"
#include "xldt_msg.h"

/* 
** A base year y must be chosen so that y % 400 == 1. It must be lesser
** than the base year used by Excel (1900).
*/
#define BASE_YEAR 1601

/*
** A normal year has 365 days. Every 4th year is leap if it's not multiple
** of 100 or if it's multiple of 400. A leap year has 366 days.
** The second month has 28 days in a normal year, 29 days in a leap year.
*/
#define IS_LEAP(y) ((y) % 4 == 0 && (y) % 100 != 0 || (y) % 400 == 0)

/*
** A cycle of 4 years has 365 * 3 + 366 = 4 * 365 + 1 = 1461 days.
** The last year of every 25th cycle of 4 years is a multiple of 100, so it
** isn't leap, it has one day less.
** A cycle of 100 years has 25 * 1461 - 1 = 36524 days.
** The last year of every 4th cycle of 100 years is a multiple of 400, so
** it's leap, it has one more day.
** A cycle of 400 years has 4 * 36524 + 1 = 146097 days.
*/
#define DAYS_IN_YEAR      365
#define DAYS_IN_4_YEARS   1461
#define DAYS_IN_100_YEARS 36524
#define DAYS_IN_400_YEARS 146097

/*
** The DAYS_IN_YEARS macro calculates the number of full days in the given
** number of years starting with the 1st January of the BASE_YEAR.
** The argument must be greater than or equal to 0.
*/
#define DAYS_IN_YEARS(n) ((n) * 365 + (n) / 400 - (n) / 100 + (n) / 4)

/*
** The calendar assigns a serial number to each date.
** The serial number 1 represents 1899-12-31, so that the numbers produced
** by this module are identical with those produced by Excel for dates
** starting with 1900-03-01 when using the 1900 based date system (the
** identity is lost for previous dates because of Lotus bug, also present
** in Excel).
** The base offset is the difference in days between the date corresponding
** to the serial number 1 and 1st January of BASE_YEAR. It is used for
** internal calculations.
*/
#define BASE_OFFSET (DAYS_IN_YEARS(1900 - BASE_YEAR) - 1)

/*
** Every year has 12 months.
*/
#define MONTHS_IN_YEAR 12
/*
** The number of days contained in the given number of months of a non-leap
** year is stored in the array below.
*/
static long DAYS_IN_MONTHS[] = {
    0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365
};

/*
** Every week has 7 days.
*/
#define DAYS_IN_WEEK 7

/*
** A day has 24 hours, an hour has 60 minutes, a minute has 60 seconds, so
** an hour has 3600 seconds, a day has 1440 minutes or 86400 seconds.
*/
#define HOURS_IN_DAY      24
#define MINUTES_IN_HOUR   60
#define MINUTES_IN_DAY    1440
#define SECONDS_IN_MINUTE 60
#define SECONDS_IN_HOUR   3600
#define SECONDS_IN_DAY    86400

/*
** Return the nearest lesser integer regardless of the sign of the value.
*/
static long
x_floor(double v)
{
    return (long)floor(v);
}

/*
** Round to the nearest integer when the decimal part is not 0.5 and to the
** nearest even integer when the decimal part is exactly 0.5.
*/
static long
x_round(double v)
{
    long x = (long)round(v);
    if (x < v) {
        double d = v - x;
        if (d > 0.5 || (d == 0.5 && x % 2 != 0)) {
            return x + 1;
        }
    }
    else if (x > v) {
        double d = x - v;
        if (d > 0.5 || (d == 0.5 && x % 2 != 0)) {
            return x - 1;
        }
    }
    return x;
}

/*
** Return the quotient of the Euclidean division between n and d.
*/
static long
x_quotient(long n, long d)
{
    if (n < 0) {
        if (d < 0) {
            return (- n - 1) / (- d) + 1;
        }
        return - ((- n - 1) / d) - 1;
    }
    if (d < 0) {
        return - (n / (- d));
    }
    return n / d;
}

/*
** Return the remainder of the Euclidean division between n and d.
*/
static long
x_remainder(long n, long d)
{
    return n - d * x_quotient(n, d);
}

/*
** Return the number of days passed between the 1st January BASE_YEAR and
** the 1st January of the given year. The result is negative for the years
** before BASE_YEAR.
*/
static long
days_before_year(long year)
{
    long n_cycles = 0, n_days = 0, n_years = year - BASE_YEAR;
    if (n_years < 0) {
        n_cycles = x_quotient(n_years, 400);
        n_years -= n_cycles * 400;
        n_days += n_cycles * DAYS_IN_400_YEARS;
    }
    return n_days + DAYS_IN_YEARS(n_years);
}

/*
** Return the number of days passed between the 1st January and the 1st of
** the given month (1 - 12) of the year.
** Return -1 if the month number isn't valid.
*/
static long
year_days_before_month(long year, long month)
{
    long days = -1;
    if (month >= 1 || month <= MONTHS_IN_YEAR) {
        days = DAYS_IN_MONTHS[month - 1];
        if (month > 2 && IS_LEAP(year)) {
            days += 1;
        }
    }
    return days;
}

/*
** Write the year, month and day corresponding to the serial number at the
** addresses given as arguments (can't be NULL).
*/
static void
serial_to_date(long serial, long *year, long *month, long *day)
{
    long n, n_days;
    /* Translate to absolute serial (where 1 is 1st January of BASE_YEAR) */
    serial += BASE_OFFSET;
    n_days = serial - 1;
    *year = BASE_YEAR;
    n = x_quotient(n_days, DAYS_IN_400_YEARS);
    *year += n * 400;
    n_days -= n * DAYS_IN_400_YEARS;
    n = x_quotient(n_days, DAYS_IN_100_YEARS);
    n -= n >> 2;
    *year += n * 100;
    n_days -= n * DAYS_IN_100_YEARS;
    n = x_quotient(n_days, DAYS_IN_4_YEARS);
    *year += n * 4;
    n_days -= n * DAYS_IN_4_YEARS;
    n = x_quotient(n_days, DAYS_IN_YEAR);
    n -= n >> 2;
    *year += n;
    n_days -= n * DAYS_IN_YEAR;
    *month = 1 + n_days / 31;
    if (*month < MONTHS_IN_YEAR && 
        n_days >= year_days_before_month(*year, *month + 1)) 
    {
        *month += 1;
    }
    n_days -= year_days_before_month(*year, *month);
    *day = n_days + 1;
}

/*
** Return the serial corresponding to the given year, month and day, so that
** 1 corresponds to 1899-12-31.
*/
static long
date_as_serial(long year, long month, long day)
{
    if (month < 1 || month > MONTHS_IN_YEAR) {
        long n_years;
        n_years = x_quotient(month - 1, MONTHS_IN_YEAR);
        year += n_years;
        month -= n_years * MONTHS_IN_YEAR;
    }
    day += year_days_before_month(year, month);
    day += days_before_year(year);
    /* Return translation from absolute serial */
    return day - BASE_OFFSET;
}

#define SUN_1 1
#define MON_1 2
#define MON_0 3
#define MON_1_EXT 11
#define TUE_1_EXT 12
#define WED_1_EXT 13
#define THU_1_EXT 14
#define FRI_1_EXT 15
#define SAT_1_EXT 16
#define SUN_1_EXT 17

/*
** Return the weekday according to the week type values defined above.
** Return -1 if the type isn't valid.
*/
static long
serial_as_weekday(long serial, long type)
{
    /*
    ** Since the 1st January 2001 was a Monday and 2001 is a first year of
    ** a cycle, BASE_YEAR (which must be a first year of a cycle) has the
    ** 1st January on a Monday.
    ** It is at BASE_OFFSET days before the date represented by serial 1.
    */
    long base = 1 - BASE_OFFSET, days;
    /* Translate the base according to the required result type. */
    if (type == SUN_1) {
        base -= 1;
    }
    else if (MON_1_EXT <= type && type <= SUN_1_EXT) {
        base += type - MON_1_EXT;
    }
    else if (type != MON_0 && type != MON_1) {
        return -1;
    }
    days = serial - base;
    days = x_remainder(days, DAYS_IN_WEEK);
    if (type == MON_0) {
        return days;
    }
    return days + 1;
}

#define MON_2 21

/*
** Return the week number according to the week type value defined above or
** to the values used by the 'serial_as_weekday' function.
** Return 0 if the type isn't valid.
*/
static long
serial_as_week(long serial, long type)
{
    long base, day, last, month, year;
    serial_to_date(serial, &year, &month, &day);
    if (type == SUN_1 || 
        type == MON_1 || (type >= MON_1_EXT && type <= SUN_1_EXT))
    {
        base = date_as_serial(year, 1, 1);
        base -= serial_as_weekday(base, type) - 1;
        return (serial - base) / DAYS_IN_WEEK + 1;
    }
    if (type == MON_2) {
        long wday;
        /* Find the Monday of the ISO week 1 of the year. */
        base = date_as_serial(year, 1, 1);
        wday = serial_as_weekday(base, MON_1);
        if (wday <= 4) {
            base -= wday - 1;
        }
        else {
            base += DAYS_IN_WEEK - wday + 1;
        }
        if (serial < base) {
            base = date_as_serial(year - 1, 1, 1);
            wday = serial_as_weekday(base, MON_1);
            if (wday <= 4) {
                base -= wday - 1;
            }
            else {
                base += DAYS_IN_WEEK - wday + 1;
            }
        }
        else {
            last = date_as_serial(year, 12, 31);
            wday = serial_as_weekday(last, SUN_1);
            if (wday <= 4) {
                last -= wday - 1;
            }
            else {
                last += DAYS_IN_WEEK - wday + 1;
            }
            if (serial > last) {
                return 1;
            }
        }
        return (serial - base) / DAYS_IN_WEEK + 1;
    }
    return 0;
}

static PyObject *
xldt_year(PyObject *self, PyObject *args)
{
    double a_value;
    long day, month, year;
    if (!PyArg_ParseTuple(args, "d", &a_value)) {
        return NULL;
    }
    serial_to_date(x_floor(a_value), &year, &month, &day);
    return PyLong_FromLong(year);
}

static PyObject *
xldt_month(PyObject *self, PyObject *args)
{
    double a_value;
    long day, month, year;
    if (!PyArg_ParseTuple(args, "d", &a_value)) {
        return NULL;
    }
    serial_to_date(x_floor(a_value), &year, &month, &day);
    return PyLong_FromLong(month);
}

static PyObject *
xldt_day(PyObject *self, PyObject *args)
{
    double a_value;
    long day, month, year;
    if (!PyArg_ParseTuple(args, "d", &a_value)) {
        return NULL;
    }
    serial_to_date(x_floor(a_value), &year, &month, &day);
    return PyLong_FromLong(day);
}

static PyObject *
add_week_types(PyObject *module)
{
    if (module == NULL) {
        return NULL;
    }
    if (PyModule_AddIntMacro(module, SUN_1) < 0 ||
        PyModule_AddIntMacro(module, MON_1) < 0 ||
        PyModule_AddIntMacro(module, MON_0) < 0 ||
        PyModule_AddIntMacro(module, MON_2) < 0)
    {
        Py_DECREF(module);
        return NULL;
    }
    if (PyModule_AddIntMacro(module, MON_1_EXT) < 0 ||
        PyModule_AddIntMacro(module, TUE_1_EXT) < 0 ||
        PyModule_AddIntMacro(module, WED_1_EXT) < 0 ||
        PyModule_AddIntMacro(module, THU_1_EXT) < 0 ||
        PyModule_AddIntMacro(module, FRI_1_EXT) < 0 ||
        PyModule_AddIntMacro(module, SAT_1_EXT) < 0 ||
        PyModule_AddIntMacro(module, SUN_1_EXT) < 0)
    {
        Py_DECREF(module);
        return NULL;
    }
    return module;
}

static PyObject *
xldt_weekday(PyObject *self, PyObject *args)
{
    double a_value;
    long a_type = SUN_1, day;
    if (!PyArg_ParseTuple(args, "d|l", &a_value, &a_type)) {
        return NULL;
    }
    day = serial_as_weekday(x_floor(a_value), a_type);
    if (day < 0) {
        PyErr_Format(PyExc_ValueError, WEEKDAY_TYPE_ERRMSG, a_type);
        return NULL;
    }
    return PyLong_FromLong(day);
}

static PyObject *
xldt_date(PyObject *self, PyObject *args)
{
    double a_day = 1.0, a_month = 1.0, a_year;
    if (!PyArg_ParseTuple(args, "d|dd", &a_year, &a_month, &a_day)) {
        return NULL;
    }
    return PyFloat_FromDouble(date_as_serial((long)a_year, 
                                             (long)a_month, 
                                             (long)a_day));
}

static PyObject *
xldt_hour(PyObject *self, PyObject *args)
{
    double a_value;
    long second;
    if (!PyArg_ParseTuple(args, "d", &a_value)) {
        return NULL;
    }
    second = x_round((a_value - floor(a_value)) * SECONDS_IN_DAY);
    return PyLong_FromLong(second / SECONDS_IN_HOUR);
}

static PyObject *
xldt_minute(PyObject *self, PyObject *args)
{
    double a_value;
    long second;
    if (!PyArg_ParseTuple(args, "d", &a_value)) {
        return NULL;
    }
    second = x_round((a_value - floor(a_value)) * SECONDS_IN_DAY);
    return PyLong_FromLong((second % SECONDS_IN_HOUR) / SECONDS_IN_MINUTE);
}

static PyObject *
xldt_second(PyObject *self, PyObject *args)
{
    double a_value;
    long second;
    if (!PyArg_ParseTuple(args, "d", &a_value)) {
        return NULL;
    }
    second = x_round((a_value - floor(a_value)) * SECONDS_IN_DAY);
    return PyLong_FromLong(second % SECONDS_IN_MINUTE);
}

static PyObject *
xldt_time(PyObject *self, PyObject *args)
{
    double a_hour, a_minute = 0, a_second = 0;
    if (!PyArg_ParseTuple(args, "d|dd", &a_hour, &a_minute, &a_second)) {
        return NULL;
    }
    a_minute += a_hour * MINUTES_IN_HOUR;
    a_second += a_minute * SECONDS_IN_MINUTE;
    a_second = x_remainder((long)a_second, SECONDS_IN_DAY);
    return PyFloat_FromDouble(a_second / SECONDS_IN_DAY);
}

static PyObject *
xldt_days(PyObject *self, PyObject *args)
{
    double a_start, a_end;
    if (!PyArg_ParseTuple(args, "dd", &a_start, &a_end)) {
        return NULL;
    }
    return PyLong_FromLong(x_floor(a_end) - x_floor(a_start));
}

static PyObject *
xldt_months(PyObject *self, PyObject *args)
{
    double a_start, a_end;
    long start_year, start_month, start_day;
    long end_year, end_month, end_day;
    long delta;
    if (!PyArg_ParseTuple(args, "dd", &a_start, &a_end)) {
        return NULL;
    }
    serial_to_date(x_floor(a_start), &start_year, &start_month,
                   &start_day);
    serial_to_date(x_floor(a_end), &end_year, &end_month,
                   &end_day);
    delta = (end_year - start_year) * 12 + end_month - start_month;
    if (start_day > end_day) {
        delta -= 1;
    }
    return PyLong_FromLong(delta);
}

static PyObject *
xldt_years(PyObject *self, PyObject *args)
{
    double a_start, a_end;
    long start_year, start_month, start_day;
    long end_year, end_month, end_day;
    long delta;
    if (!PyArg_ParseTuple(args, "dd", &a_start, &a_end)) {
        return NULL;
    }
    serial_to_date(x_floor(a_start), &start_year, &start_month, &start_day);
    serial_to_date(x_floor(a_end), &end_year, &end_month, &end_day);
    delta = end_year - start_year;
    if (start_month > end_month || (start_month == end_month &&
                                    start_day > end_day))
    {
        delta -= 1;
    }
    return PyLong_FromLong(delta);
}

/*
** These are the limits of time_t when it's stored on 32 bit.
*/
#define TIME_T_32_LOWER -2145916800
#define TIME_T_32_UPPER  2145916800

static PyObject *
xldt_now(PyObject *self, PyObject *args)
{
    time_t t;
    struct tm now;
#ifdef _WIN32
    int err_code;
#endif
    long day, month, year, second;
    time(&t);
#ifdef _WIN32
    err_code = localtime_s(&now, &t);
    if (err_code != 0) {
        errno = err_code;
        PyErr_SetFromErrno(PyExc_OSError);
        return NULL;
    }
#else
    if ((t < TIME_T_32_LOWER || t > TIME_T_32_UPPER) && sizeof(t) < 8) {
        errno = EINVAL;
        PyErr_SetString(PyExc_OverflowError, TIME_T_SIZE_ERRMSG);
        return NULL;
    }
    errno = 0;
    if (localtime_r(&t, &now) == NULL && errno == 0) {
        errno = EINVAL;
        PyErr_SetFromErrno(PyExc_OSError);
        return NULL;
    }
#endif
    day = now.tm_mday;
    month = now.tm_mon + 1;
    year = now.tm_year + 1900;
    second = now.tm_sec + now.tm_min * SECONDS_IN_MINUTE +
             now.tm_hour * SECONDS_IN_HOUR;
    return PyFloat_FromDouble((double)date_as_serial(year, month, day) + 
                              (double)second / SECONDS_IN_DAY);
}

static PyObject *
xldt_today(PyObject *self, PyObject *args)
{
    PyObject *now = xldt_now(self, args);
    if (now != NULL) {
        PyObject *day = PyLong_FromLong(x_floor(PyFloat_AsDouble(now)));
        Py_DECREF(now);
        return day;
    }
    return NULL;
}

static PyObject *
xldt_week(PyObject *self, PyObject *args)
{
    double a_value;
    long a_type = SUN_1, week;
    if (!PyArg_ParseTuple(args, "d|l", &a_value, &a_type)) {
        return NULL;
    }
    week = serial_as_week(x_floor(a_value), a_type);
    if (week < 1) {
        PyErr_Format(PyExc_ValueError, WEEK_TYPE_ERRMSG, a_type);
        return NULL;
    }
    return PyLong_FromLong(week);
}

static PyObject *
xldt_isoweek(PyObject *self, PyObject *args)
{
    double a_value;
    long week;
    if (!PyArg_ParseTuple(args, "d", &a_value)) {
        return NULL;
    }
    week = serial_as_week(x_floor(a_value), MON_2);
    return PyLong_FromLong(week);
}

#define WE_SAT_SUN 1
#define WE_SUN_MON 2
#define WE_MON_TUE 3
#define WE_TUE_WED 4
#define WE_WED_THU 5
#define WE_THU_FRI 6
#define WE_FRI_SAT 7
#define WE_SUN 11
#define WE_MON 12
#define WE_TUE 13
#define WE_WED 14
#define WE_THU 15
#define WE_FRI 16
#define WE_SAT 17

static PyObject *
add_weekend_types(PyObject *module)
{
    if (module == NULL) {
        return NULL;
    }
    if (PyModule_AddIntMacro(module, WE_SAT_SUN) < 0 ||
        PyModule_AddIntMacro(module, WE_SUN_MON) < 0 ||
        PyModule_AddIntMacro(module, WE_MON_TUE) < 0 ||
        PyModule_AddIntMacro(module, WE_TUE_WED) < 0 ||
        PyModule_AddIntMacro(module, WE_WED_THU) < 0 ||
        PyModule_AddIntMacro(module, WE_THU_FRI) < 0 ||
        PyModule_AddIntMacro(module, WE_FRI_SAT) < 0)
    {
        Py_DECREF(module);
        return NULL;
    }
    if (PyModule_AddIntMacro(module, WE_SUN) < 0 ||
        PyModule_AddIntMacro(module, WE_MON) < 0 ||
        PyModule_AddIntMacro(module, WE_TUE) < 0 ||
        PyModule_AddIntMacro(module, WE_WED) < 0 ||
        PyModule_AddIntMacro(module, WE_THU) < 0 ||
        PyModule_AddIntMacro(module, WE_FRI) < 0 ||
        PyModule_AddIntMacro(module, WE_SAT) < 0)
    {
        Py_DECREF(module);
        return NULL;
    }
    return module;
}

static PyObject *
xldt_isweekend(PyObject *self, PyObject *args)
{
    double a_value;
    long serial;
    PyObject *a_type = Py_None;
    if (!PyArg_ParseTuple(args, "d|O", &a_value, &a_type)) {
        return NULL;
    }
    serial = x_floor(a_value);
    if (a_type == Py_None) {
        long day = serial_as_weekday(serial, MON_1);
        return PyBool_FromLong(day == 6 || day == 7);
    }
    if (PyLong_Check(a_type)) {
        long day, we_type = PyLong_AsLong(a_type);
        if (we_type >= WE_SAT_SUN && we_type <= WE_FRI_SAT) {
            day = serial_as_weekday(serial, MON_1_EXT + we_type - WE_SAT_SUN);
            return PyBool_FromLong(day == 6 || day == 7);
        }
        if (we_type >= WE_SUN && we_type <= WE_SAT) {
            day = serial_as_weekday(serial, MON_1_EXT + we_type - WE_SUN);
            return PyBool_FromLong(day == 6 || day == 7);
        }
    }
    else if (PyUnicode_Check(a_type)) {
        long day;
        Py_ssize_t i = 0, n = PyUnicode_GET_LENGTH(a_type);
        day = serial_as_weekday(serial, MON_0);
        if (n == 7) {
            long test = 0;
            while (i < n) {
                Py_UCS4 rune = PyUnicode_READ_CHAR(a_type, i);
                if (i == day && rune == '1') {
                    test = 1;
                }
                else if (rune != '0' && rune != '1') {
                    break;
                }
                i += 1;
            }
            if (i == n) {
                return PyBool_FromLong(test);
            }
        }
    }
    PyErr_Format(PyExc_TypeError, WEEKEND_TYPE_ERRMSG, a_type);
    return NULL;
}

static PyMethodDef xldt_methods[] = {
    {"date", xldt_date, METH_VARARGS, xldt_date__doc__},
    {"day", xldt_day, METH_VARARGS, xldt_day__doc__},
    {"days", xldt_days, METH_VARARGS, xldt_days__doc__},
    {"hour", xldt_hour, METH_VARARGS, xldt_hour__doc__},
    {"isweekend", xldt_isweekend, METH_VARARGS, xldt_isweekend__doc__},
    {"isoweek", xldt_isoweek, METH_VARARGS, xldt_isoweek__doc__},
    {"minute", xldt_minute, METH_VARARGS, xldt_minute__doc__},
    {"month", xldt_month, METH_VARARGS, xldt_month__doc__},
    {"months", xldt_months, METH_VARARGS, xldt_months__doc__},
    {"now", xldt_now, METH_NOARGS, xldt_now__doc__},
    {"second", xldt_second, METH_VARARGS, xldt_second__doc__},
    {"time", xldt_time, METH_VARARGS, xldt_time__doc__},
    {"today", xldt_today, METH_NOARGS, xldt_today__doc__},
    {"weekday", xldt_weekday, METH_VARARGS, xldt_weekday__doc__},
    {"week", xldt_week, METH_VARARGS, xldt_week__doc__},
    {"year", xldt_year, METH_VARARGS, xldt_year__doc__},
    {"years", xldt_years, METH_VARARGS, xldt_years__doc__},
    {NULL, NULL, 0, NULL}
};

static int
xldt_exec(PyObject *module)
{
    if (add_week_types(module) == NULL || add_weekend_types(module) == NULL) 
    {
        return -1;
    }
    return 0;
}

static PyModuleDef_Slot xldt_slots[] = {
    {Py_mod_exec, xldt_exec},
    {0, NULL}
};

static PyModuleDef xldt_module = {
    PyModuleDef_HEAD_INIT
};

PyMODINIT_FUNC 
PyInit_xldt(void) {
    xldt_module.m_name = "xldt";
    xldt_module.m_doc = xldt__doc__;
    xldt_module.m_size = 0;
    xldt_module.m_methods = xldt_methods;
    xldt_module.m_slots = xldt_slots;
    return PyModuleDef_Init(&xldt_module);
}
