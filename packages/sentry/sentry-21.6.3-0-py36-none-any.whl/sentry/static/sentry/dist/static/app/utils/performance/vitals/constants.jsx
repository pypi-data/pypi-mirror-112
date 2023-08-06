var _a, _b;
import { t } from 'app/locale';
import { measurementType, MobileVital, WebVital } from 'app/utils/discover/fields';
export var WEB_VITAL_DETAILS = (_a = {},
    _a[WebVital.FP] = {
        slug: 'fp',
        name: t('First Paint'),
        acronym: 'FP',
        description: t('Render time of the first pixel loaded in the viewport (may overlap with FCP).'),
        poorThreshold: 3000,
        type: measurementType(WebVital.FP),
    },
    _a[WebVital.FCP] = {
        slug: 'fcp',
        name: t('First Contentful Paint'),
        acronym: 'FCP',
        description: t('Render time of the first image, text or other DOM node in the viewport.'),
        poorThreshold: 3000,
        type: measurementType(WebVital.FCP),
    },
    _a[WebVital.LCP] = {
        slug: 'lcp',
        name: t('Largest Contentful Paint'),
        acronym: 'LCP',
        description: t('Render time of the largest image, text or other DOM node in the viewport.'),
        poorThreshold: 4000,
        type: measurementType(WebVital.LCP),
    },
    _a[WebVital.FID] = {
        slug: 'fid',
        name: t('First Input Delay'),
        acronym: 'FID',
        description: t('Response time of the browser to a user interaction (clicking, tapping, etc).'),
        poorThreshold: 300,
        type: measurementType(WebVital.FID),
    },
    _a[WebVital.CLS] = {
        slug: 'cls',
        name: t('Cumulative Layout Shift'),
        acronym: 'CLS',
        description: t('Sum of layout shift scores that measure the visual stability of the page.'),
        poorThreshold: 0.25,
        type: measurementType(WebVital.CLS),
    },
    _a[WebVital.TTFB] = {
        slug: 'ttfb',
        name: t('Time to First Byte'),
        acronym: 'TTFB',
        description: t("The time that it takes for a user's browser to receive the first byte of page content."),
        poorThreshold: 600,
        type: measurementType(WebVital.TTFB),
    },
    _a[WebVital.RequestTime] = {
        slug: 'ttfb.requesttime',
        name: t('Request Time'),
        acronym: 'RT',
        description: t('Captures the time spent making the request and receiving the first byte of the response.'),
        poorThreshold: 600,
        type: measurementType(WebVital.RequestTime),
    },
    _a);
export var MOBILE_VITAL_DETAILS = (_b = {},
    _b[MobileVital.AppStartCold] = {
        slug: 'app_start_cold',
        name: t('App Start Cold'),
        description: t('Cold start is a measure of the application start up time from scratch.'),
        type: measurementType(MobileVital.AppStartCold),
    },
    _b[MobileVital.AppStartWarm] = {
        slug: 'app_start_warm',
        name: t('App Start Warm'),
        description: t('Warm start is a measure of the application start up time while still in memory.'),
        type: measurementType(MobileVital.AppStartWarm),
    },
    _b[MobileVital.FramesTotal] = {
        slug: 'frames_total',
        name: t('Total Frames'),
        description: t('Total frames is a count of the number of frames recorded within a transaction.'),
        type: measurementType(MobileVital.FramesTotal),
    },
    _b[MobileVital.FramesSlow] = {
        slug: 'frames_slow',
        name: t('Slow Frames'),
        description: t('Slow frames is a count of the number of slow frames recorded within a transaction.'),
        type: measurementType(MobileVital.FramesSlow),
    },
    _b[MobileVital.FramesFrozen] = {
        slug: 'frames_frozen',
        name: t('Frozen Frames'),
        description: t('Frozen frames is a count of the number of frozen frames recorded within a transaction.'),
        type: measurementType(MobileVital.FramesFrozen),
    },
    _b);
//# sourceMappingURL=constants.jsx.map