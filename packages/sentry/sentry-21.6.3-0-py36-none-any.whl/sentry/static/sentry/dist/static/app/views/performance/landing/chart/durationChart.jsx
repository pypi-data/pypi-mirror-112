import { __assign, __makeTemplateObject, __read, __rest, __spreadArray } from "tslib";
import withRouter from 'react-router/lib/withRouter';
import styled from '@emotion/styled';
import ErrorPanel from 'app/components/charts/errorPanel';
import EventsRequest from 'app/components/charts/eventsRequest';
import { HeaderTitleLegend } from 'app/components/charts/styles';
import TransparentLoadingMask from 'app/components/charts/transparentLoadingMask';
import { getInterval } from 'app/components/charts/utils';
import { getParams } from 'app/components/organizations/globalSelectionHeader/getParams';
import Placeholder from 'app/components/placeholder';
import QuestionTooltip from 'app/components/questionTooltip';
import { IconWarning } from 'app/icons';
import space from 'app/styles/space';
import { getUtcToLocalDateObject } from 'app/utils/dates';
import getDynamicText from 'app/utils/getDynamicText';
import withApi from 'app/utils/withApi';
import Chart from '../../charts/chart';
import { DoubleHeaderContainer } from '../../styles';
import { getFieldOrBackup } from '../display/utils';
function DurationChart(props) {
    var organization = props.organization, api = props.api, eventView = props.eventView, location = props.location, router = props.router, field = props.field, title = props.title, titleTooltip = props.titleTooltip, backupField = props.backupField, usingBackupAxis = props.usingBackupAxis;
    // construct request parameters for fetching chart data
    var globalSelection = eventView.getGlobalSelection();
    var start = globalSelection.datetime.start
        ? getUtcToLocalDateObject(globalSelection.datetime.start)
        : null;
    var end = globalSelection.datetime.end
        ? getUtcToLocalDateObject(globalSelection.datetime.end)
        : null;
    var utc = getParams(location.query).utc;
    var _backupField = backupField ? [backupField] : [];
    var apiPayload = eventView.getEventsAPIPayload(location);
    return (<EventsRequest organization={organization} api={api} period={globalSelection.datetime.period} project={globalSelection.projects} environment={globalSelection.environments} team={apiPayload.team} start={start} end={end} interval={getInterval({
            start: start,
            end: end,
            period: globalSelection.datetime.period,
        }, true)} showLoading={false} query={apiPayload.query} includePrevious={false} yAxis={__spreadArray([field], __read(_backupField))} partial hideError>
      {function (_a) {
            var loading = _a.loading, reloading = _a.reloading, errored = _a.errored, singleAxisResults = _a.timeseriesData, multiAxisResults = _a.results;
            var _field = usingBackupAxis ? getFieldOrBackup(field, backupField) : field;
            var results = singleAxisResults
                ? singleAxisResults
                : [multiAxisResults === null || multiAxisResults === void 0 ? void 0 : multiAxisResults.find(function (r) { return r.seriesName === _field; })].filter(Boolean);
            var series = results
                ? results.map(function (_a) {
                    var rest = __rest(_a, []);
                    return __assign(__assign({}, rest), { seriesName: _field });
                })
                : [];
            if (errored) {
                return (<ErrorPanel>
              <IconWarning color="gray300" size="lg"/>
            </ErrorPanel>);
            }
            return (<div>
            <DoubleHeaderContainer>
              <HeaderTitleLegend>
                {title}
                <QuestionTooltip position="top" size="sm" title={titleTooltip}/>
              </HeaderTitleLegend>
            </DoubleHeaderContainer>
            {results && (<ChartContainer>
                <MaskContainer>
                  <TransparentLoadingMask visible={loading}/>
                  {getDynamicText({
                        value: (<Chart height={250} data={series} loading={loading || reloading} router={router} statsPeriod={globalSelection.datetime.period} start={start} end={end} utc={utc === 'true'} grid={{
                                left: space(3),
                                right: space(3),
                                top: space(3),
                                bottom: loading || reloading ? space(4) : space(1.5),
                            }} disableMultiAxis/>),
                        fixed: <Placeholder height="250px" testId="skeleton-ui"/>,
                    })}
                </MaskContainer>
              </ChartContainer>)}
          </div>);
        }}
    </EventsRequest>);
}
var ChartContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding-top: ", ";\n"], ["\n  padding-top: ", ";\n"])), space(1));
var MaskContainer = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
export default withRouter(withApi(DurationChart));
var templateObject_1, templateObject_2;
//# sourceMappingURL=durationChart.jsx.map