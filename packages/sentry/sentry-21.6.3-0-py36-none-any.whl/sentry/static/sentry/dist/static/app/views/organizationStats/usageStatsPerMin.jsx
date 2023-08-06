import { __extends, __makeTemplateObject } from "tslib";
import styled from '@emotion/styled';
import AsyncComponent from 'app/components/asyncComponent';
import { t } from 'app/locale';
import { Outcome } from './types';
import { formatUsageWithUnits, getFormatUsageOptions } from './utils';
/**
 * Making 1 extra API call to display this number isn't very efficient.
 * The other approach would be to fetch the data in UsageStatsOrg with 1min
 * interval and roll it up on the frontend, but that (1) adds unnecessary
 * complexity as it's gnarly to fetch + rollup 90 days of 1min intervals,
 * (3) API resultset has a limit of 1000, so 90 days of 1min would not work.
 *
 * We're going with this approach for simplicity sake. By keeping the range
 * as small as possible, this call is quite fast.
 */
var UsageStatsPerMin = /** @class */ (function (_super) {
    __extends(UsageStatsPerMin, _super);
    function UsageStatsPerMin() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    UsageStatsPerMin.prototype.getEndpoints = function () {
        return [['orgStats', this.endpointPath, { query: this.endpointQuery }]];
    };
    Object.defineProperty(UsageStatsPerMin.prototype, "endpointPath", {
        get: function () {
            var organization = this.props.organization;
            return "/organizations/" + organization.slug + "/stats_v2/";
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(UsageStatsPerMin.prototype, "endpointQuery", {
        get: function () {
            return {
                statsPeriod: '5m',
                interval: '1m',
                groupBy: ['category', 'outcome'],
                field: ['sum(quantity)'],
            };
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(UsageStatsPerMin.prototype, "minuteData", {
        get: function () {
            var dataCategory = this.props.dataCategory;
            var _a = this.state, loading = _a.loading, error = _a.error, orgStats = _a.orgStats;
            if (loading || error || !orgStats || orgStats.intervals.length === 0) {
                return undefined;
            }
            // The last minute in the series is still "in progress"
            // Read data from 2nd last element for the latest complete minute
            var intervals = orgStats.intervals, groups = orgStats.groups;
            var lastMin = Math.max(intervals.length - 2, 0);
            var eventsLastMin = groups.reduce(function (count, group) {
                var _a = group.by, outcome = _a.outcome, category = _a.category;
                // HACK: The backend enum are singular, but the frontend enums are plural
                if (!dataCategory.includes("" + category) || outcome !== Outcome.ACCEPTED) {
                    return count;
                }
                count += group.series['sum(quantity)'][lastMin];
                return count;
            }, 0);
            return formatUsageWithUnits(eventsLastMin, dataCategory, getFormatUsageOptions(dataCategory));
        },
        enumerable: false,
        configurable: true
    });
    UsageStatsPerMin.prototype.renderComponent = function () {
        if (!this.minuteData) {
            return null;
        }
        return (<Wrapper>
        {this.minuteData} {t('in last min')}
      </Wrapper>);
    };
    return UsageStatsPerMin;
}(AsyncComponent));
export default UsageStatsPerMin;
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: inline-block;\n  color: ", ";\n  font-size: ", ";\n"], ["\n  display: inline-block;\n  color: ", ";\n  font-size: ", ";\n"])), function (p) { return p.theme.success; }, function (p) { return p.theme.fontSizeMedium; });
var templateObject_1;
//# sourceMappingURL=usageStatsPerMin.jsx.map