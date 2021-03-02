/*
 baseado em https://vuedose.tips/create-a-i18n-plugin-with-composition-api-in-vuejs-3/
 O plugin vue-i18n não funcionou com Vue 3
*/

import { ref, provide, inject } from 'vue'


// relative time copied from https://stackoverflow.com/a/53800501/266362

const units = {
    year: 24 * 60 * 60 * 1000 * 365,
    month: 24 * 60 * 60 * 1000 * 365 / 12,
    day: 24 * 60 * 60 * 1000,
    hour: 60 * 60 * 1000,
    minute: 60 * 1000,
    second: 1000
}


const createI18n = config => ({
    locale: ref(config.locale),
    messages: config.messages,
    $t(key) {
        return this.messages[this.locale.value][key]
    },
    relative_time(d1, d2 = new Date()) {
        const rtf = new Intl.RelativeTimeFormat(this.locale.value, {
            localeMatcher: 'best fit',
            numeric: 'always',
            style: 'long',
        })
        const elapsed = d1 - d2

        // "Math.abs" accounts for both "past" & "future" scenarios
        for (let u in units)
            if (Math.abs(elapsed) > units[u] || u == 'second')
                return rtf.format(Math.round(elapsed / units[u]), u)
    }
})

const i18nSymbol = Symbol()

export function provideI18n(i18nConfig) {
    const i18n = createI18n(i18nConfig)
    provide(i18nSymbol, i18n)
}

export function useI18n() {
    const i18n = inject(i18nSymbol)
    if (!i18n) {
        throw new Error('No i18n provided!')
    }
    return i18n
}
