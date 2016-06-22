this['localeData'] = this['localeData'] || {};
this['localeData']['ru_ru'] = [{"dashboard":{"metarubrics":[{"code":"cafe","rubricQuery":"Поесть"},{"code":"hotel","rubricQuery":"Гостиницы"},{"code":"sport","rubricQuery":"Спорттовары"},{"code":"newlyBuilt","rubricQuery":"Новостройки"},{"code":"all"}],"makhachkala":{"metarubrics":[{"code":"cafe","rubricQuery":"Поесть"},{"code":"hotel","rubricQuery":"Гостиницы"},{"code":"banquetHalls","rubricQuery":"Банкетные залы"},{"code":"newlyBuilt","rubricQuery":"Новостройки"},{"code":"all"}]}},"noresults":{"metarubrics":[{"code":"cafe","rubricQuery":"Поесть"},{"code":"hotel","rubricQuery":"Гостиницы"},{"code":"pharmacy","rubricQuery":"Аптеки"},{"code":"newlyBuilt","rubricQuery":"Новостройки"}]},"socials":["vkontakte","facebook","twitter","odnoklassniki"],"cityselect":{"countries":["ru","ua","kz","kg"]},"geoobjects":{"avoidAddressInName":false,"infoStrategy":"default","showNearStationDistance":false},"landmarksEnabled":false,"mobileAppPlatforms":["android","ios","windowsphone","blackberry"],"firms":{"useDrilldownInAddress":false},"feedback":{"reverseRatingOrder":false,"phone":["ekaterinburg","kazan","krasnoyarsk","moscow","n_novgorod","novosibirsk","omsk","perm","samara","spb","togliatti","ufa","chelyabinsk","saransk","staroskol"],"chat":["chelyabinsk","ekaterinburg","kazan","krasnoyarsk","moscow","n_novgorod","novosibirsk","omsk","perm","samara","spb","togliatti","ufa","yoshkarola"]},"traffic":{"isLeftHand":false},"parkingsMode":{"radius":250,"disable":false,"differentIcon":false},"map":{"onlyAdsMushrooms":false,"mapAdsEnabled":true},"filtersInTitles":true,"tools":{"extension":true,"extensionInlineInstall":true,"downloadBtn":true,"downloadBetaVersion":true},"entrancesPromo":{"firmQuery":"2ГИС, городской информационный справочник","excludeProjects":[]},"promoMobile":true,"advWarning":true,"weather":{"cities":[],"promoLinks":[{"type":"taxi","dashboardText":"Сегодня можно и на такси","linkText":"В такую погоду можно и на такси","staticText":"","searchText":"Такси","temperature":[-99,-25],"excludeCities":["spb"]},{"type":"sauna","dashboardText":"В сауне теплее","linkText":"В сауне теплее","staticText":"","temperature":[-24,-10],"searchText":"Бани и сауны","filters":{"sauna_steam_type_russian_bath":"true"},"excludeCities":["spb"]},{"type":"cinema","dashboardText":"Может, в кино?","linkText":"Может, в кино?","staticText":"","searchText":"Кинотеатры","temperature":[-9,10],"excludeCities":["spb"]},{"type":"cinema","dashboardText":"Может, в кино?","linkText":"Может, в кино?","staticText":"","searchText":"Кинотеатры","temperature":[11,19],"cities":{"chita":{},"noyabrsk":{}}},{"type":"baza_otdyha","dashboardText":"За город на выходные","linkText":"За город на выходные","staticText":"","searchText":"Базы отдыха","temperature":[11,19],"excludeCities":["spb","chita","noyabrsk"]},{"type":"conditioner","dashboardText":"Сделать прохладней","linkText":"Сделать прохладней","staticText":"","searchText":"Кондиционеры","temperature":[20,99],"excludeCities":["spb"]},{"type":"ginza","dashboardText":"Лето в ресторанах Ginza Project","linkText":"Лето в ресторанах Ginza Project","staticText":"","searchText":"Ginza Project","temperature":[-99,98],"cities":{"spb":{}}}]},"zoom":{"nearZoom":17,"focusZoom":16},"transport":{"metroShowLineNote":true},"isCIS":true,"ads":{"mkb":{"rotate":false},"dashboard":{"intervalRotation":40000},"teaser":{"intervalRotation":40000}},"webvisor":[{"city":"novosibirsk","turnOnProbability":0.0175},{"city":"moscow","turnOnProbability":0.0175}]},{"time":{"weekFirstDayOffset":1,"short":"HH:mm","is12h":false,"dashboard":"HH:mm, dddd, D MMMM","zone":"Z"},"currency":{"id":"RUB","symbol":"руб.","standard":"# ##0,00 ¤","short":"# ##0,## ¤"},"number":{"standard":"# ##0,###","short":"# ##0,###"},"address":{"order":"straight"},"string":{"quotationStart":"«","quotationEnd":"»"}},null];
if (typeof window != 'undefined') { window.moment = require('moment');
//! moment.js locale configuration
//! locale : russian (ru)
//! author : Viktorminator : https://github.com/Viktorminator
//! Author : Menelion Elensúle : https://github.com/Oire

(function (global, factory) {
   typeof exports === 'object' && typeof module !== 'undefined' ? factory(require('../moment')) :
   typeof define === 'function' && define.amd ? define(['moment'], factory) :
   factory(global.moment)
}(this, function (moment) { 'use strict';


    function plural(word, num) {
        var forms = word.split('_');
        return num % 10 === 1 && num % 100 !== 11 ? forms[0] : (num % 10 >= 2 && num % 10 <= 4 && (num % 100 < 10 || num % 100 >= 20) ? forms[1] : forms[2]);
    }
    function relativeTimeWithPlural(number, withoutSuffix, key) {
        var format = {
            'mm': withoutSuffix ? 'минута_минуты_минут' : 'минуту_минуты_минут',
            'hh': 'час_часа_часов',
            'dd': 'день_дня_дней',
            'MM': 'месяц_месяца_месяцев',
            'yy': 'год_года_лет'
        };
        if (key === 'm') {
            return withoutSuffix ? 'минута' : 'минуту';
        }
        else {
            return number + ' ' + plural(format[key], +number);
        }
    }
    function monthsCaseReplace(m, format) {
        var months = {
            'nominative': 'январь_февраль_март_апрель_май_июнь_июль_август_сентябрь_октябрь_ноябрь_декабрь'.split('_'),
            'accusative': 'января_февраля_марта_апреля_мая_июня_июля_августа_сентября_октября_ноября_декабря'.split('_')
        },
        nounCase = (/D[oD]?(\[[^\[\]]*\]|\s+)+MMMM?/).test(format) ?
            'accusative' :
            'nominative';
        return months[nounCase][m.month()];
    }
    function monthsShortCaseReplace(m, format) {
        var monthsShort = {
            'nominative': 'янв_фев_март_апр_май_июнь_июль_авг_сен_окт_ноя_дек'.split('_'),
            'accusative': 'янв_фев_мар_апр_мая_июня_июля_авг_сен_окт_ноя_дек'.split('_')
        },
        nounCase = (/D[oD]?(\[[^\[\]]*\]|\s+)+MMMM?/).test(format) ?
            'accusative' :
            'nominative';
        return monthsShort[nounCase][m.month()];
    }
    function weekdaysCaseReplace(m, format) {
        var weekdays = {
            'nominative': 'воскресенье_понедельник_вторник_среда_четверг_пятница_суббота'.split('_'),
            'accusative': 'воскресенье_понедельник_вторник_среду_четверг_пятницу_субботу'.split('_')
        },
        nounCase = (/\[ ?[Вв] ?(?:прошлую|следующую|эту)? ?\] ?dddd/).test(format) ?
            'accusative' :
            'nominative';
        return weekdays[nounCase][m.day()];
    }

    var ru = moment.defineLocale('ru', {
        months : monthsCaseReplace,
        monthsShort : monthsShortCaseReplace,
        weekdays : weekdaysCaseReplace,
        weekdaysShort : 'вс_пн_вт_ср_чт_пт_сб'.split('_'),
        weekdaysMin : 'вс_пн_вт_ср_чт_пт_сб'.split('_'),
        monthsParse : [/^янв/i, /^фев/i, /^мар/i, /^апр/i, /^ма[й|я]/i, /^июн/i, /^июл/i, /^авг/i, /^сен/i, /^окт/i, /^ноя/i, /^дек/i],
        longDateFormat : {
            LT : 'HH:mm',
            LTS : 'HH:mm:ss',
            L : 'DD.MM.YYYY',
            LL : 'D MMMM YYYY г.',
            LLL : 'D MMMM YYYY г., HH:mm',
            LLLL : 'dddd, D MMMM YYYY г., HH:mm'
        },
        calendar : {
            sameDay: '[Сегодня в] LT',
            nextDay: '[Завтра в] LT',
            lastDay: '[Вчера в] LT',
            nextWeek: function () {
                return this.day() === 2 ? '[Во] dddd [в] LT' : '[В] dddd [в] LT';
            },
            lastWeek: function (now) {
                if (now.week() !== this.week()) {
                    switch (this.day()) {
                    case 0:
                        return '[В прошлое] dddd [в] LT';
                    case 1:
                    case 2:
                    case 4:
                        return '[В прошлый] dddd [в] LT';
                    case 3:
                    case 5:
                    case 6:
                        return '[В прошлую] dddd [в] LT';
                    }
                } else {
                    if (this.day() === 2) {
                        return '[Во] dddd [в] LT';
                    } else {
                        return '[В] dddd [в] LT';
                    }
                }
            },
            sameElse: 'L'
        },
        relativeTime : {
            future : 'через %s',
            past : '%s назад',
            s : 'несколько секунд',
            m : relativeTimeWithPlural,
            mm : relativeTimeWithPlural,
            h : 'час',
            hh : relativeTimeWithPlural,
            d : 'день',
            dd : relativeTimeWithPlural,
            M : 'месяц',
            MM : relativeTimeWithPlural,
            y : 'год',
            yy : relativeTimeWithPlural
        },
        meridiemParse: /ночи|утра|дня|вечера/i,
        isPM : function (input) {
            return /^(дня|вечера)$/.test(input);
        },
        meridiem : function (hour, minute, isLower) {
            if (hour < 4) {
                return 'ночи';
            } else if (hour < 12) {
                return 'утра';
            } else if (hour < 17) {
                return 'дня';
            } else {
                return 'вечера';
            }
        },
        ordinalParse: /\d{1,2}-(й|го|я)/,
        ordinal: function (number, period) {
            switch (period) {
            case 'M':
            case 'd':
            case 'DDD':
                return number + '-й';
            case 'D':
                return number + '-го';
            case 'w':
            case 'W':
                return number + '-я';
            default:
                return number;
            }
        },
        week : {
            dow : 1, // Monday is the first day of the week.
            doy : 7  // The week that contains Jan 1st is the first week of the year.
        }
    });

    return ru;

}));
};