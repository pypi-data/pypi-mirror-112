import { decodeScalar } from 'app/utils/queryString';
export function generateTagsRoute(_a) {
    var orgSlug = _a.orgSlug;
    return "/organizations/" + orgSlug + "/performance/summary/tags/";
}
export function decodeSelectedTagKey(location) {
    return decodeScalar(location.query.tagKey);
}
export function tagsRouteWithQuery(_a) {
    var orgSlug = _a.orgSlug, transaction = _a.transaction, projectID = _a.projectID, query = _a.query;
    var pathname = generateTagsRoute({
        orgSlug: orgSlug,
    });
    return {
        pathname: pathname,
        query: {
            transaction: transaction,
            project: projectID,
            environment: query.environment,
            statsPeriod: query.statsPeriod,
            start: query.start,
            end: query.end,
            query: query.query,
            tagKey: query.tagKey,
        },
    };
}
// TODO(k-fish): Improve meta of backend response to return these directly
export function parseHistogramBucketInfo(row) {
    var field = Object.keys(row).find(function (f) { return f.includes('histogram'); });
    if (!field) {
        return undefined;
    }
    var parts = field.split('_');
    return {
        histogramField: field,
        bucketSize: parseInt(parts[parts.length - 3], 10),
        offset: parseInt(parts[parts.length - 2], 10),
        multiplier: parseInt(parts[parts.length - 1], 10),
    };
}
//# sourceMappingURL=utils.jsx.map