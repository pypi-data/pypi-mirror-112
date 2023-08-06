import { __assign } from "tslib";
import * as Router from 'react-router';
import { ExtraErrorData } from '@sentry/integrations';
import * as Sentry from '@sentry/react';
import SentryRRWeb from '@sentry/rrweb';
import { Integrations } from '@sentry/tracing';
import { _browserPerformanceTimeOriginMode } from '@sentry/utils';
import { DISABLE_RR_WEB, SPA_DSN } from 'app/constants';
import { init as initApiSentryClient } from 'app/utils/apiSentryClient';
/**
 * We accept a routes argument here because importing `app/routes`
 * is expensive in regards to bundle size. Some entrypoints may opt to forgo
 * having routing instrumentation in order to have a smaller bundle size.
 * (e.g.  `app/views/integrationPipeline`)
 */
function getSentryIntegrations(hasReplays, routes) {
    if (hasReplays === void 0) { hasReplays = false; }
    var integrations = [
        new ExtraErrorData({
            // 6 is arbitrary, seems like a nice number
            depth: 6,
        }),
        new Integrations.BrowserTracing(__assign(__assign({}, (typeof routes === 'function'
            ? {
                routingInstrumentation: Sentry.reactRouterV3Instrumentation(Router.browserHistory, Router.createRoutes(routes()), Router.match),
            }
            : {})), { idleTimeout: 5000 })),
    ];
    if (hasReplays) {
        // eslint-disable-next-line no-console
        console.log('[sentry] Instrumenting session with rrweb');
        // TODO(ts): The type returned by SentryRRWeb seems to be somewhat
        // incompatible. It's a newer plugin, so this can be expected, but we
        // should fix.
        integrations.push(new SentryRRWeb({
            checkoutEveryNms: 60 * 1000, // 60 seconds
        }));
    }
    return integrations;
}
/**
 * Initialize the Sentry SDK
 *
 * If `routes` is passed, we will instrument react-router. Not all
 * entrypoints require this.
 */
export function initializeSdk(config, _a) {
    var _b = _a === void 0 ? {} : _a, routes = _b.routes;
    if (config.dsn_requests) {
        initApiSentryClient(config.dsn_requests);
    }
    var apmSampling = config.apmSampling, sentryConfig = config.sentryConfig, userIdentity = config.userIdentity;
    var tracesSampleRate = apmSampling !== null && apmSampling !== void 0 ? apmSampling : 0;
    var hasReplays = (userIdentity === null || userIdentity === void 0 ? void 0 : userIdentity.isStaff) && !DISABLE_RR_WEB;
    Sentry.init(__assign(__assign({}, sentryConfig), { 
        /**
         * For SPA mode, we need a way to overwrite the default DSN from backend
         * as well as `whitelistUrls`
         */
        dsn: SPA_DSN || (sentryConfig === null || sentryConfig === void 0 ? void 0 : sentryConfig.dsn), whitelistUrls: SPA_DSN
            ? ['localhost', 'dev.getsentry.net', 'sentry.dev', 'webpack-internal://']
            : sentryConfig === null || sentryConfig === void 0 ? void 0 : sentryConfig.whitelistUrls, integrations: getSentryIntegrations(hasReplays, routes), tracesSampleRate: tracesSampleRate, 
        /**
         * There is a bug in Safari, that causes `AbortError` when fetch is aborted, and you are in the middle of reading the response.
         * In Chrome and other browsers, it is handled gracefully, where in Safari, it produces additional error, that is jumping
         * outside of the original Promise chain and bubbles up to the `unhandledRejection` handler, that we then captures as error.
         * Ref: https://bugs.webkit.org/show_bug.cgi?id=215771
         */
        ignoreErrors: ['AbortError: Fetch is aborted'] }));
    // Track timeOrigin Selection by the SDK to see if it improves transaction durations
    Sentry.addGlobalEventProcessor(function (event, _hint) {
        event.tags = event.tags || {};
        event.tags['timeOrigin.mode'] = _browserPerformanceTimeOriginMode;
        return event;
    });
    if (userIdentity) {
        Sentry.setUser(userIdentity);
    }
    if (window.__SENTRY__VERSION) {
        Sentry.setTag('sentry_version', window.__SENTRY__VERSION);
    }
    Sentry.setTag('rrweb.active', hasReplays ? 'yes' : 'no');
}
//# sourceMappingURL=initializeSdk.jsx.map