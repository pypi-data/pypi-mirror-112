var platforms = [
    'dotnet',
    'android',
    'apple',
    'dart',
    'elixir',
    'flutter',
    'go',
    'java',
    'javascript',
    'native',
    'node',
    'perl',
    'php',
    'python',
    'react-native',
    'ruby',
    'rust',
    'unity',
];
var performancePlatforms = [
    'dotnet',
    'android',
    'apple',
    'go',
    'java',
    'javascript',
    'node',
    'php',
    'python',
    'react-native',
    'ruby',
];
function validDocPlatform(platform) {
    return platforms.includes(platform);
}
export function getDocsPlatform(platform, performanceOnly) {
    // react-native is the only platform that has a dash, and supports performance so we can skip that check
    if (platform === 'react-native') {
        return 'react-native';
    }
    var index = platform.indexOf('-');
    var prefix = index >= 0 ? platform.substring(0, index) : platform;
    if (validDocPlatform(prefix)) {
        var validPerformancePrefix = performancePlatforms.includes(prefix);
        if ((performanceOnly && validPerformancePrefix) || !performanceOnly) {
            return prefix;
        }
    }
    // can't find a matching docs platform
    return null;
}
export function getConfigureTracingDocsLink(project) {
    var _a;
    var platform = (_a = project === null || project === void 0 ? void 0 : project.platform) !== null && _a !== void 0 ? _a : null;
    var docsPlatform = platform ? getDocsPlatform(platform, true) : null;
    return docsPlatform === null
        ? null // this platform does not support performance
        : "https://docs.sentry.io/platforms/" + docsPlatform + "/performance/";
}
//# sourceMappingURL=docs.jsx.map