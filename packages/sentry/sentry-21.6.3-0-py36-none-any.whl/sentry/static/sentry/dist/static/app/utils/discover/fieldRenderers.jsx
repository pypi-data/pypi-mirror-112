import { __assign, __makeTemplateObject, __read, __spreadArray } from "tslib";
import * as React from 'react';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import partial from 'lodash/partial';
import Count from 'app/components/count';
import Duration from 'app/components/duration';
import ProjectBadge from 'app/components/idBadge/projectBadge';
import UserBadge from 'app/components/idBadge/userBadge';
import { RowRectangle } from 'app/components/performance/waterfall/rowBar';
import { pickBarColour, toPercent } from 'app/components/performance/waterfall/utils';
import Tooltip from 'app/components/tooltip';
import UserMisery from 'app/components/userMisery';
import Version from 'app/components/version';
import { t } from 'app/locale';
import { defined } from 'app/utils';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import { AGGREGATIONS, getAggregateAlias, getSpanOperationName, isEquation, isRelativeSpanOperationBreakdownField, SPAN_OP_BREAKDOWN_FIELDS, SPAN_OP_RELATIVE_BREAKDOWN_FIELD, } from 'app/utils/discover/fields';
import { getShortEventId } from 'app/utils/events';
import { formatFloat, formatPercentage } from 'app/utils/formatters';
import getDynamicText from 'app/utils/getDynamicText';
import Projects from 'app/utils/projects';
import { filterToLocationQuery, SpanOperationBreakdownFilter, stringToFilter, } from 'app/views/performance/transactionSummary/filter';
import ArrayValue from './arrayValue';
import KeyTransactionField from './keyTransactionField';
import { BarContainer, Container, FlexContainer, NumberContainer, OverflowLink, StyledDateTime, StyledShortId, UserIcon, VersionContainer, } from './styles';
import TeamKeyTransactionField from './teamKeyTransactionField';
var EmptyValueContainer = styled('span')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.gray300; });
var emptyValue = <EmptyValueContainer>{t('n/a')}</EmptyValueContainer>;
/**
 * A mapping of field types to their rendering function.
 * This mapping is used when a field is not defined in SPECIAL_FIELDS
 * and the field is not being coerced to a link.
 *
 * This mapping should match the output sentry.utils.snuba:get_json_type
 */
var FIELD_FORMATTERS = {
    boolean: {
        isSortable: true,
        renderFunc: function (field, data) {
            var value = data[field] ? t('true') : t('false');
            return <Container>{value}</Container>;
        },
    },
    date: {
        isSortable: true,
        renderFunc: function (field, data) { return (<Container>
        {data[field]
                ? getDynamicText({
                    value: <StyledDateTime date={data[field]}/>,
                    fixed: 'timestamp',
                })
                : emptyValue}
      </Container>); },
    },
    duration: {
        isSortable: true,
        renderFunc: function (field, data) { return (<NumberContainer>
        {typeof data[field] === 'number' ? (<Duration seconds={data[field] / 1000} fixedDigits={2} abbreviation/>) : (emptyValue)}
      </NumberContainer>); },
    },
    integer: {
        isSortable: true,
        renderFunc: function (field, data) { return (<NumberContainer>
        {typeof data[field] === 'number' ? <Count value={data[field]}/> : emptyValue}
      </NumberContainer>); },
    },
    number: {
        isSortable: true,
        renderFunc: function (field, data) { return (<NumberContainer>
        {typeof data[field] === 'number' ? formatFloat(data[field], 4) : emptyValue}
      </NumberContainer>); },
    },
    percentage: {
        isSortable: true,
        renderFunc: function (field, data) { return (<NumberContainer>
        {typeof data[field] === 'number' ? formatPercentage(data[field]) : emptyValue}
      </NumberContainer>); },
    },
    string: {
        isSortable: true,
        renderFunc: function (field, data) {
            // Some fields have long arrays in them, only show the tail of the data.
            var value = Array.isArray(data[field])
                ? data[field].slice(-1)
                : defined(data[field])
                    ? data[field]
                    : emptyValue;
            return <Container>{value}</Container>;
        },
    },
    array: {
        isSortable: true,
        renderFunc: function (field, data) {
            var value = Array.isArray(data[field]) ? data[field] : [data[field]];
            return <ArrayValue value={value}/>;
        },
    },
};
/**
 * "Special fields" either do not map 1:1 to an single column in the event database,
 * or they require custom UI formatting that can't be handled by the datatype formatters.
 */
var SPECIAL_FIELDS = {
    id: {
        sortField: 'id',
        renderFunc: function (data) {
            var id = data === null || data === void 0 ? void 0 : data.id;
            if (typeof id !== 'string') {
                return null;
            }
            return <Container>{getShortEventId(id)}</Container>;
        },
    },
    trace: {
        sortField: 'trace',
        renderFunc: function (data) {
            var id = data === null || data === void 0 ? void 0 : data.trace;
            if (typeof id !== 'string') {
                return null;
            }
            return <Container>{getShortEventId(id)}</Container>;
        },
    },
    'issue.id': {
        sortField: 'issue.id',
        renderFunc: function (data, _a) {
            var organization = _a.organization;
            var target = {
                pathname: "/organizations/" + organization.slug + "/issues/" + data['issue.id'] + "/",
            };
            return (<Container>
          <OverflowLink to={target} aria-label={data['issue.id']}>
            {data['issue.id']}
          </OverflowLink>
        </Container>);
        },
    },
    issue: {
        sortField: null,
        renderFunc: function (data, _a) {
            var organization = _a.organization;
            var issueID = data['issue.id'];
            if (!issueID) {
                return (<Container>
            <StyledShortId shortId={"" + data.issue}/>
          </Container>);
            }
            var target = {
                pathname: "/organizations/" + organization.slug + "/issues/" + issueID + "/",
            };
            return (<Container>
          <OverflowLink to={target} aria-label={issueID}>
            <StyledShortId shortId={"" + data.issue}/>
          </OverflowLink>
        </Container>);
        },
    },
    project: {
        sortField: 'project',
        renderFunc: function (data, _a) {
            var organization = _a.organization;
            return (<Container>
          <Projects orgId={organization.slug} slugs={[data.project]}>
            {function (_a) {
                    var projects = _a.projects;
                    var project = projects.find(function (p) { return p.slug === data.project; });
                    return (<ProjectBadge project={project ? project : { slug: data.project }} avatarSize={16}/>);
                }}
          </Projects>
        </Container>);
        },
    },
    user: {
        sortField: 'user',
        renderFunc: function (data) {
            if (data.user) {
                var _a = __read(data.user.split(':'), 2), key = _a[0], value = _a[1];
                var userObj = {
                    id: '',
                    name: '',
                    email: '',
                    username: '',
                    ip_address: '',
                };
                userObj[key] = value;
                var badge = <UserBadge user={userObj} hideEmail avatarSize={16}/>;
                return <Container>{badge}</Container>;
            }
            return <Container>{emptyValue}</Container>;
        },
    },
    'user.display': {
        sortField: 'user.display',
        renderFunc: function (data) {
            if (data['user.display']) {
                var userObj = {
                    id: '',
                    name: data['user.display'],
                    email: '',
                    username: '',
                    ip_address: '',
                };
                var badge = <UserBadge user={userObj} hideEmail avatarSize={16}/>;
                return <Container>{badge}</Container>;
            }
            return <Container>{emptyValue}</Container>;
        },
    },
    'count_unique(user)': {
        sortField: 'count_unique(user)',
        renderFunc: function (data) {
            var count = data.count_unique_user;
            if (typeof count === 'number') {
                return (<FlexContainer>
            <NumberContainer>
              <Count value={count}/>
            </NumberContainer>
            <UserIcon size="20"/>
          </FlexContainer>);
            }
            return <Container>{emptyValue}</Container>;
        },
    },
    release: {
        sortField: 'release',
        renderFunc: function (data) {
            return data.release ? (<VersionContainer>
          <Version version={data.release} anchor={false} tooltipRawVersion truncate/>
        </VersionContainer>) : (<Container>{emptyValue}</Container>);
        },
    },
    'error.handled': {
        sortField: 'error.handled',
        renderFunc: function (data) {
            var values = data['error.handled'];
            // Transactions will have null, and default events have no handled attributes.
            if (values === null || (values === null || values === void 0 ? void 0 : values.length) === 0) {
                return <Container>{emptyValue}</Container>;
            }
            var value = Array.isArray(values) ? values.slice(-1)[0] : values;
            return <Container>{[1, null].includes(value) ? 'true' : 'false'}</Container>;
        },
    },
    key_transaction: {
        sortField: null,
        renderFunc: function (data, _a) {
            var _b;
            var organization = _a.organization;
            return (<Container>
        <KeyTransactionField isKeyTransaction={((_b = data.key_transaction) !== null && _b !== void 0 ? _b : 0) !== 0} organization={organization} projectSlug={data.project} transactionName={data.transaction}/>
      </Container>);
        },
    },
    team_key_transaction: {
        sortField: null,
        renderFunc: function (data, _a) {
            var _b;
            var organization = _a.organization;
            return (<Container>
        <TeamKeyTransactionField isKeyTransaction={((_b = data.team_key_transaction) !== null && _b !== void 0 ? _b : 0) !== 0} organization={organization} projectSlug={data.project} transactionName={data.transaction}/>
      </Container>);
        },
    },
    'trend_percentage()': {
        sortField: 'trend_percentage()',
        renderFunc: function (data) { return (<NumberContainer>
        {typeof data.trend_percentage === 'number'
                ? formatPercentage(data.trend_percentage - 1)
                : emptyValue}
      </NumberContainer>); },
    },
    'timestamp.to_hour': {
        sortField: 'timestamp.to_hour',
        renderFunc: function (data) { return (<Container>
        {getDynamicText({
                value: <StyledDateTime date={data['timestamp.to_hour']} format="lll z"/>,
                fixed: 'timestamp.to_hour',
            })}
      </Container>); },
    },
    'timestamp.to_day': {
        sortField: 'timestamp.to_day',
        renderFunc: function (data) { return (<Container>
        {getDynamicText({
                value: <StyledDateTime date={data['timestamp.to_day']} format="MMM D, YYYY"/>,
                fixed: 'timestamp.to_day',
            })}
      </Container>); },
    },
};
/**
 * "Special functions" are functions whose values either do not map 1:1 to a single column,
 * or they require custom UI formatting that can't be handled by the datatype formatters.
 */
var SPECIAL_FUNCTIONS = {
    user_misery: function (fieldName) { return function (data) {
        var userMiseryField = fieldName;
        if (!(userMiseryField in data)) {
            return <NumberContainer>{emptyValue}</NumberContainer>;
        }
        var userMisery = data[userMiseryField];
        if (userMisery === null || isNaN(userMisery)) {
            return <NumberContainer>{emptyValue}</NumberContainer>;
        }
        var projectThresholdConfig = 'project_threshold_config';
        var countMiserableUserField = '';
        var miseryLimit = parseInt(userMiseryField.split('_').pop() || '', 10);
        if (isNaN(miseryLimit)) {
            countMiserableUserField = 'count_miserable_user';
            if (projectThresholdConfig in data) {
                miseryLimit = data[projectThresholdConfig][1];
            }
            else {
                miseryLimit = undefined;
            }
        }
        else {
            countMiserableUserField = "count_miserable_user_" + miseryLimit;
        }
        var uniqueUsers = data.count_unique_user;
        var miserableUsers;
        if (countMiserableUserField in data) {
            var countMiserableMiseryLimit = parseInt(countMiserableUserField.split('_').pop() || '', 10);
            miserableUsers =
                countMiserableMiseryLimit === miseryLimit ||
                    (isNaN(countMiserableMiseryLimit) && projectThresholdConfig)
                    ? data[countMiserableUserField]
                    : undefined;
        }
        return (<BarContainer>
        <UserMisery bars={10} barHeight={20} miseryLimit={miseryLimit} totalUsers={uniqueUsers} userMisery={userMisery} miserableUsers={miserableUsers}/>
      </BarContainer>);
    }; },
};
/**
 * Get the sort field name for a given field if it is special or fallback
 * to the generic type formatter.
 */
export function getSortField(field, tableMeta) {
    if (SPECIAL_FIELDS.hasOwnProperty(field)) {
        return SPECIAL_FIELDS[field].sortField;
    }
    if (!tableMeta) {
        return field;
    }
    if (isEquation(field)) {
        return field;
    }
    for (var alias in AGGREGATIONS) {
        if (field.startsWith(alias)) {
            return AGGREGATIONS[alias].isSortable ? field : null;
        }
    }
    var fieldType = tableMeta[field];
    if (FIELD_FORMATTERS.hasOwnProperty(fieldType)) {
        return FIELD_FORMATTERS[fieldType].isSortable
            ? field
            : null;
    }
    return null;
}
var isDurationValue = function (data, field) {
    return field in data && typeof data[field] === 'number';
};
var spanOperationRelativeBreakdownRenderer = function (data, _a) {
    var _b, _c;
    var location = _a.location, organization = _a.organization, eventView = _a.eventView;
    var sumOfSpanTime = SPAN_OP_BREAKDOWN_FIELDS.reduce(function (prev, curr) { return (isDurationValue(data, curr) ? prev + data[curr] : prev); }, 0);
    var cumulativeSpanOpBreakdown = Math.max(sumOfSpanTime, data['transaction.duration']);
    if (!isDurationValue(data, 'spans.total.time') ||
        SPAN_OP_BREAKDOWN_FIELDS.every(function (field) { return !isDurationValue(data, field); }) ||
        cumulativeSpanOpBreakdown === 0) {
        return FIELD_FORMATTERS.duration.renderFunc(SPAN_OP_RELATIVE_BREAKDOWN_FIELD, data);
    }
    var otherPercentage = 1;
    var orderedSpanOpsBreakdownFields;
    var sortingOnField = (_c = (_b = eventView === null || eventView === void 0 ? void 0 : eventView.sorts) === null || _b === void 0 ? void 0 : _b[0]) === null || _c === void 0 ? void 0 : _c.field;
    if (sortingOnField && SPAN_OP_BREAKDOWN_FIELDS.includes(sortingOnField)) {
        orderedSpanOpsBreakdownFields = __spreadArray([
            sortingOnField
        ], __read(SPAN_OP_BREAKDOWN_FIELDS.filter(function (op) { return op !== sortingOnField; })));
    }
    else {
        orderedSpanOpsBreakdownFields = SPAN_OP_BREAKDOWN_FIELDS;
    }
    return (<RelativeOpsBreakdown>
      {orderedSpanOpsBreakdownFields.map(function (field) {
            var _a;
            if (!isDurationValue(data, field)) {
                return null;
            }
            var operationName = (_a = getSpanOperationName(field)) !== null && _a !== void 0 ? _a : 'op';
            var spanOpDuration = data[field];
            var widthPercentage = spanOpDuration / cumulativeSpanOpBreakdown;
            otherPercentage = otherPercentage - widthPercentage;
            if (widthPercentage === 0) {
                return null;
            }
            return (<div key={operationName} style={{ width: toPercent(widthPercentage || 0) }}>
            <Tooltip title={<div>
                  <div>{operationName}</div>
                  <div>
                    <Duration seconds={spanOpDuration / 1000} fixedDigits={2} abbreviation/>
                  </div>
                </div>} containerDisplayMode="block">
              <RectangleRelativeOpsBreakdown spanBarHatch={false} style={{
                    backgroundColor: pickBarColour(operationName),
                    cursor: 'pointer',
                }} onClick={function (event) {
                    event.stopPropagation();
                    var filter = stringToFilter(operationName);
                    if (filter === SpanOperationBreakdownFilter.None) {
                        return;
                    }
                    trackAnalyticsEvent({
                        eventName: 'Performance Views: Select Relative Breakdown',
                        eventKey: 'performance_views.relative_breakdown.selection',
                        organization_id: parseInt(organization.id, 10),
                        action: filter,
                    });
                    browserHistory.push({
                        pathname: location.pathname,
                        query: __assign(__assign({}, location.query), filterToLocationQuery(filter)),
                    });
                }}/>
            </Tooltip>
          </div>);
        })}
      <div key="other" style={{ width: toPercent(otherPercentage || 0) }}>
        <Tooltip title={<div>{t('Other')}</div>} containerDisplayMode="block">
          <OtherRelativeOpsBreakdown spanBarHatch={false}/>
        </Tooltip>
      </div>
    </RelativeOpsBreakdown>);
};
var RelativeOpsBreakdown = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  position: relative;\n  display: flex;\n"], ["\n  position: relative;\n  display: flex;\n"])));
var RectangleRelativeOpsBreakdown = styled(RowRectangle)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  position: relative;\n  width: 100%;\n"], ["\n  position: relative;\n  width: 100%;\n"])));
var OtherRelativeOpsBreakdown = styled(RectangleRelativeOpsBreakdown)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  background-color: ", ";\n"], ["\n  background-color: ", ";\n"])), function (p) { return p.theme.gray100; });
/**
 * Get the field renderer for the named field and metadata
 *
 * @param {String} field name
 * @param {object} metadata mapping.
 * @returns {Function}
 */
export function getFieldRenderer(field, meta) {
    if (SPECIAL_FIELDS.hasOwnProperty(field)) {
        return SPECIAL_FIELDS[field].renderFunc;
    }
    if (isRelativeSpanOperationBreakdownField(field)) {
        return spanOperationRelativeBreakdownRenderer;
    }
    var fieldName = getAggregateAlias(field);
    var fieldType = meta[fieldName];
    for (var alias in SPECIAL_FUNCTIONS) {
        if (fieldName.startsWith(alias)) {
            return SPECIAL_FUNCTIONS[alias](fieldName);
        }
    }
    if (FIELD_FORMATTERS.hasOwnProperty(fieldType)) {
        return partial(FIELD_FORMATTERS[fieldType].renderFunc, fieldName);
    }
    return partial(FIELD_FORMATTERS.string.renderFunc, fieldName);
}
/**
 * Get the field renderer for the named field only based on its type from the given
 * metadata.
 *
 * @param {String} field name
 * @param {object} metadata mapping.
 * @returns {Function}
 */
export function getFieldFormatter(field, meta) {
    var fieldName = getAggregateAlias(field);
    var fieldType = meta[fieldName];
    if (FIELD_FORMATTERS.hasOwnProperty(fieldType)) {
        return partial(FIELD_FORMATTERS[fieldType].renderFunc, fieldName);
    }
    return partial(FIELD_FORMATTERS.string.renderFunc, fieldName);
}
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=fieldRenderers.jsx.map