import { __assign, __extends, __makeTemplateObject } from "tslib";
import * as React from 'react';
import { withRouter } from 'react-router';
import styled from '@emotion/styled';
import map from 'lodash/map';
import Alert from 'app/components/alert';
import Button from 'app/components/button';
import DateTime from 'app/components/dateTime';
import DiscoverButton from 'app/components/discoverButton';
import FileSize from 'app/components/fileSize';
import ExternalLink from 'app/components/links/externalLink';
import Link from 'app/components/links/link';
import LoadingIndicator from 'app/components/loadingIndicator';
import { ErrorDot, ErrorLevel, ErrorMessageContent, ErrorMessageTitle, ErrorTitle, } from 'app/components/performance/waterfall/rowDetails';
import Pill from 'app/components/pill';
import Pills from 'app/components/pills';
import { generateIssueEventTarget, generateTraceTarget, } from 'app/components/quickTrace/utils';
import { ALL_ACCESS_PROJECTS } from 'app/constants/globalSelectionHeader';
import { IconAnchor, IconWarning } from 'app/icons';
import { t, tn } from 'app/locale';
import space from 'app/styles/space';
import { assert } from 'app/types/utils';
import EventView from 'app/utils/discover/eventView';
import { generateEventSlug } from 'app/utils/discover/urls';
import getDynamicText from 'app/utils/getDynamicText';
import withApi from 'app/utils/withApi';
import * as SpanEntryContext from './context';
import InlineDocs from './inlineDocs';
import { rawSpanKeys } from './types';
import { getTraceDateTimeRange, isGapSpan, isOrphanSpan, scrollToSpan } from './utils';
var DEFAULT_ERRORS_VISIBLE = 5;
var SIZE_DATA_KEYS = ['Encoded Body Size', 'Decoded Body Size', 'Transfer Size'];
var SpanDetail = /** @class */ (function (_super) {
    __extends(SpanDetail, _super);
    function SpanDetail() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            errorsOpened: false,
        };
        _this.toggleErrors = function () {
            _this.setState(function (_a) {
                var errorsOpened = _a.errorsOpened;
                return ({ errorsOpened: !errorsOpened });
            });
        };
        return _this;
    }
    SpanDetail.prototype.renderTraversalButton = function () {
        if (!this.props.childTransactions) {
            // TODO: Amend size to use theme when we eventually refactor LoadingIndicator
            // 12px is consistent with theme.iconSizes['xs'] but theme returns a string.
            return (<StyledDiscoverButton size="xsmall" disabled>
          <StyledLoadingIndicator size={12}/>
        </StyledDiscoverButton>);
        }
        if (this.props.childTransactions.length <= 0) {
            return (<StyledDiscoverButton size="xsmall" disabled>
          {t('No Children')}
        </StyledDiscoverButton>);
        }
        var _a = this.props, span = _a.span, trace = _a.trace, event = _a.event, organization = _a.organization;
        assert(!isGapSpan(span));
        if (this.props.childTransactions.length === 1) {
            // Note: This is rendered by this.renderSpanChild() as a dedicated row
            return null;
        }
        var orgFeatures = new Set(organization.features);
        var _b = getTraceDateTimeRange({
            start: trace.traceStartTimestamp,
            end: trace.traceEndTimestamp,
        }), start = _b.start, end = _b.end;
        var childrenEventView = EventView.fromSavedQuery({
            id: undefined,
            name: "Children from Span ID " + span.span_id,
            fields: [
                'transaction',
                'project',
                'trace.span',
                'transaction.duration',
                'timestamp',
            ],
            orderby: '-timestamp',
            query: "event.type:transaction trace:" + span.trace_id + " trace.parent_span:" + span.span_id,
            projects: orgFeatures.has('global-views')
                ? [ALL_ACCESS_PROJECTS]
                : [Number(event.projectID)],
            version: 2,
            start: start,
            end: end,
        });
        return (<StyledDiscoverButton data-test-id="view-child-transactions" size="xsmall" to={childrenEventView.getResultsViewUrlTarget(organization.slug)}>
        {t('View Children')}
      </StyledDiscoverButton>);
    };
    SpanDetail.prototype.renderSpanChild = function () {
        var childTransactions = this.props.childTransactions;
        if (!childTransactions || childTransactions.length !== 1) {
            return null;
        }
        var childTransaction = childTransactions[0];
        var transactionResult = {
            'project.name': childTransaction.project_slug,
            transaction: childTransaction.transaction,
            'trace.span': childTransaction.span_id,
            id: childTransaction.event_id,
        };
        var eventSlug = generateSlug(transactionResult);
        var viewChildButton = (<SpanEntryContext.Consumer>
        {function (_a) {
                var getViewChildTransactionTarget = _a.getViewChildTransactionTarget;
                var to = getViewChildTransactionTarget(__assign(__assign({}, transactionResult), { eventSlug: eventSlug }));
                if (!to) {
                    return null;
                }
                return (<StyledButton data-test-id="view-child-transaction" size="xsmall" to={to}>
              {t('View Transaction')}
            </StyledButton>);
            }}
      </SpanEntryContext.Consumer>);
        return (<Row title="Child Transaction" extra={viewChildButton}>
        {transactionResult.transaction + " (" + transactionResult['project.name'] + ")"}
      </Row>);
    };
    SpanDetail.prototype.renderTraceButton = function () {
        var _a = this.props, span = _a.span, organization = _a.organization, event = _a.event;
        if (isGapSpan(span)) {
            return null;
        }
        return (<StyledButton size="xsmall" to={generateTraceTarget(event, organization)}>
        {t('View Trace')}
      </StyledButton>);
    };
    SpanDetail.prototype.renderOrphanSpanMessage = function () {
        var span = this.props.span;
        if (!isOrphanSpan(span)) {
            return null;
        }
        return (<Alert system type="info" icon={<IconWarning size="md"/>}>
        {t('This is a span that has no parent span within this transaction. It has been attached to the transaction root span by default.')}
      </Alert>);
    };
    SpanDetail.prototype.renderSpanErrorMessage = function () {
        var _a = this.props, span = _a.span, organization = _a.organization, relatedErrors = _a.relatedErrors;
        var errorsOpened = this.state.errorsOpened;
        if (!relatedErrors || relatedErrors.length <= 0 || isGapSpan(span)) {
            return null;
        }
        var visibleErrors = errorsOpened
            ? relatedErrors
            : relatedErrors.slice(0, DEFAULT_ERRORS_VISIBLE);
        return (<Alert system type="error" icon={<IconWarning size="md"/>}>
        <ErrorMessageTitle>
          {tn('An error event occurred in this transaction.', '%s error events occurred in this transaction.', relatedErrors.length)}
        </ErrorMessageTitle>
        <ErrorMessageContent>
          {visibleErrors.map(function (error) { return (<React.Fragment key={error.event_id}>
              <ErrorDot level={error.level}/>
              <ErrorLevel>{error.level}</ErrorLevel>
              <ErrorTitle>
                <Link to={generateIssueEventTarget(error, organization)}>
                  {error.title}
                </Link>
              </ErrorTitle>
            </React.Fragment>); })}
        </ErrorMessageContent>
        {relatedErrors.length > DEFAULT_ERRORS_VISIBLE && (<ErrorToggle size="xsmall" onClick={this.toggleErrors}>
            {errorsOpened ? t('Show less') : t('Show more')}
          </ErrorToggle>)}
      </Alert>);
    };
    SpanDetail.prototype.partitionSizes = function (data) {
        var sizeKeys = SIZE_DATA_KEYS.reduce(function (keys, key) {
            if (data.hasOwnProperty(key)) {
                keys[key] = data[key];
            }
            return keys;
        }, {});
        var nonSizeKeys = __assign({}, data);
        SIZE_DATA_KEYS.forEach(function (key) { return delete nonSizeKeys[key]; });
        return {
            sizeKeys: sizeKeys,
            nonSizeKeys: nonSizeKeys,
        };
    };
    SpanDetail.prototype.renderSpanDetails = function () {
        var _a, _b, _c;
        var _d = this.props, span = _d.span, event = _d.event, location = _d.location, organization = _d.organization, scrollToHash = _d.scrollToHash;
        if (isGapSpan(span)) {
            return (<SpanDetails>
          <InlineDocs platform={((_a = event.sdk) === null || _a === void 0 ? void 0 : _a.name) || ''} orgSlug={organization.slug} projectSlug={event.projectSlug}/>
        </SpanDetails>);
        }
        var startTimestamp = span.start_timestamp;
        var endTimestamp = span.timestamp;
        var duration = (endTimestamp - startTimestamp) * 1000;
        var durationString = Number(duration.toFixed(3)).toLocaleString() + "ms";
        var unknownKeys = Object.keys(span).filter(function (key) {
            return !rawSpanKeys.has(key);
        });
        var _e = this.partitionSizes((_b = span === null || span === void 0 ? void 0 : span.data) !== null && _b !== void 0 ? _b : {}), sizeKeys = _e.sizeKeys, nonSizeKeys = _e.nonSizeKeys;
        var allZeroSizes = SIZE_DATA_KEYS.map(function (key) { return sizeKeys[key]; }).every(function (value) { return value === 0; });
        return (<React.Fragment>
        {this.renderOrphanSpanMessage()}
        {this.renderSpanErrorMessage()}
        <SpanDetails>
          <table className="table key-value">
            <tbody>
              <Row title={isGapSpan(span) ? (<SpanIdTitle>Span ID</SpanIdTitle>) : (<SpanIdTitle onClick={scrollToSpan(span.span_id, scrollToHash, location)}>
                      Span ID
                      <StyledIconAnchor />
                    </SpanIdTitle>)} extra={this.renderTraversalButton()}>
                {span.span_id}
              </Row>
              <Row title="Parent Span ID">{span.parent_span_id || ''}</Row>
              {this.renderSpanChild()}
              <Row title="Trace ID" extra={this.renderTraceButton()}>
                {span.trace_id}
              </Row>
              <Row title="Description">{(_c = span === null || span === void 0 ? void 0 : span.description) !== null && _c !== void 0 ? _c : ''}</Row>
              <Row title="Status">{span.status || ''}</Row>
              <Row title="Start Date">
                {getDynamicText({
                fixed: 'Mar 16, 2020 9:10:12 AM UTC',
                value: (<React.Fragment>
                      <DateTime date={startTimestamp * 1000}/>
                      {" (" + startTimestamp + ")"}
                    </React.Fragment>),
            })}
              </Row>
              <Row title="End Date">
                {getDynamicText({
                fixed: 'Mar 16, 2020 9:10:13 AM UTC',
                value: (<React.Fragment>
                      <DateTime date={endTimestamp * 1000}/>
                      {" (" + endTimestamp + ")"}
                    </React.Fragment>),
            })}
              </Row>
              <Row title="Duration">{durationString}</Row>
              <Row title="Operation">{span.op || ''}</Row>
              <Row title="Same Process as Parent">
                {span.same_process_as_parent !== undefined
                ? String(span.same_process_as_parent)
                : null}
              </Row>
              <Tags span={span}/>
              {allZeroSizes && (<TextTr>
                  The following sizes were not collected for security reasons. Check if
                  the host serves the appropriate
                  <ExternalLink href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Timing-Allow-Origin">
                    <span className="val-string">Timing-Allow-Origin</span>
                  </ExternalLink>
                  header. You may have to enable this collection manually.
                </TextTr>)}
              {map(sizeKeys, function (value, key) { return (<Row title={key} key={key}>
                  <React.Fragment>
                    <FileSize bytes={value}/>
                    {value >= 1024 && (<span>{" (" + (JSON.stringify(value, null, 4) || '') + " B)"}</span>)}
                  </React.Fragment>
                </Row>); })}
              {map(nonSizeKeys, function (value, key) { return (<Row title={key} key={key}>
                  {JSON.stringify(value, null, 4) || ''}
                </Row>); })}
              {unknownKeys.map(function (key) { return (<Row title={key} key={key}>
                  {JSON.stringify(span[key], null, 4) || ''}
                </Row>); })}
            </tbody>
          </table>
        </SpanDetails>
      </React.Fragment>);
    };
    SpanDetail.prototype.render = function () {
        return (<SpanDetailContainer data-component="span-detail" onClick={function (event) {
                // prevent toggling the span detail
                event.stopPropagation();
            }}>
        {this.renderSpanDetails()}
      </SpanDetailContainer>);
    };
    return SpanDetail;
}(React.Component));
var StyledDiscoverButton = styled(DiscoverButton)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: absolute;\n  top: ", ";\n  right: ", ";\n"], ["\n  position: absolute;\n  top: ", ";\n  right: ", ";\n"])), space(0.75), space(0.5));
var StyledButton = styled(Button)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  position: absolute;\n  top: ", ";\n  right: ", ";\n"], ["\n  position: absolute;\n  top: ", ";\n  right: ", ";\n"])), space(0.75), space(0.5));
export var SpanDetailContainer = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  border-bottom: 1px solid ", ";\n  cursor: auto;\n"], ["\n  border-bottom: 1px solid ", ";\n  cursor: auto;\n"])), function (p) { return p.theme.border; });
export var SpanDetails = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  padding: ", ";\n"], ["\n  padding: ", ";\n"])), space(2));
var ValueTd = styled('td')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
var StyledLoadingIndicator = styled(LoadingIndicator)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  height: ", ";\n  margin: 0;\n"], ["\n  display: flex;\n  align-items: center;\n  height: ", ";\n  margin: 0;\n"])), space(2));
var StyledText = styled('p')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  font-size: ", ";\n  margin: ", " ", ";\n"], ["\n  font-size: ", ";\n  margin: ", " ", ";\n"])), function (p) { return p.theme.fontSizeMedium; }, space(2), space(0));
var TextTr = function (_a) {
    var children = _a.children;
    return (<tr>
    <td className="key"/>
    <ValueTd className="value">
      <StyledText>{children}</StyledText>
    </ValueTd>
  </tr>);
};
var ErrorToggle = styled(Button)(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space(0.75));
var SpanIdTitle = styled('a')(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  display: flex;\n  color: ", ";\n  :hover {\n    color: ", ";\n  }\n"], ["\n  display: flex;\n  color: ", ";\n  :hover {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.textColor; }, function (p) { return p.theme.textColor; });
var StyledIconAnchor = styled(IconAnchor)(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  display: block;\n  color: ", ";\n  margin-left: ", ";\n"], ["\n  display: block;\n  color: ", ";\n  margin-left: ", ";\n"])), function (p) { return p.theme.gray300; }, space(1));
export var Row = function (_a) {
    var title = _a.title, keep = _a.keep, children = _a.children, _b = _a.extra, extra = _b === void 0 ? null : _b;
    if (!keep && !children) {
        return null;
    }
    return (<tr>
      <td className="key">{title}</td>
      <ValueTd className="value">
        <pre className="val">
          <span className="val-string">{children}</span>
        </pre>
        {extra}
      </ValueTd>
    </tr>);
};
export var Tags = function (_a) {
    var span = _a.span;
    var tags = span === null || span === void 0 ? void 0 : span.tags;
    if (!tags) {
        return null;
    }
    var keys = Object.keys(tags);
    if (keys.length <= 0) {
        return null;
    }
    return (<tr>
      <td className="key">Tags</td>
      <td className="value">
        <Pills style={{ padding: '8px' }}>
          {keys.map(function (key, index) { return (<Pill key={index} name={key} value={String(tags[key]) || ''}/>); })}
        </Pills>
      </td>
    </tr>);
};
function generateSlug(result) {
    return generateEventSlug({
        id: result.id,
        'project.name': result['project.name'],
    });
}
export default withApi(withRouter(SpanDetail));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10;
//# sourceMappingURL=spanDetail.jsx.map