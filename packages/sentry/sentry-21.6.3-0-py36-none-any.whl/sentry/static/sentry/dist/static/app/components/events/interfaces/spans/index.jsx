import { __assign, __extends, __makeTemplateObject, __read } from "tslib";
import { PureComponent } from 'react';
import * as ReactRouter from 'react-router';
import styled from '@emotion/styled';
import { Observer } from 'mobx-react';
import Alert from 'app/components/alert';
import GuideAnchor from 'app/components/assistant/guideAnchor';
import List from 'app/components/list';
import ListItem from 'app/components/list/listItem';
import { Panel } from 'app/components/panels';
import SearchBar from 'app/components/searchBar';
import { IconWarning } from 'app/icons';
import { t, tct, tn } from 'app/locale';
import space from 'app/styles/space';
import { objectIsEmpty } from 'app/utils';
import * as QuickTraceContext from 'app/utils/performance/quickTrace/quickTraceContext';
import withOrganization from 'app/utils/withOrganization';
import * as AnchorLinkManager from './anchorLinkManager';
import Filter from './filter';
import TraceView from './traceView';
import { parseTrace, scrollToSpan } from './utils';
import WaterfallModel from './waterfallModel';
var SpansInterface = /** @class */ (function (_super) {
    __extends(SpansInterface, _super);
    function SpansInterface() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            parsedTrace: parseTrace(_this.props.event),
            waterfallModel: new WaterfallModel(_this.props.event),
        };
        _this.handleSpanFilter = function (searchQuery) {
            var waterfallModel = _this.state.waterfallModel;
            waterfallModel.querySpanSearch(searchQuery);
        };
        return _this;
    }
    SpansInterface.getDerivedStateFromProps = function (props, state) {
        if (state.waterfallModel.isEvent(props.event)) {
            return state;
        }
        return __assign(__assign({}, state), { parsedTrace: parseTrace(props.event), waterfallModel: new WaterfallModel(props.event) });
    };
    SpansInterface.prototype.renderTraceErrorsAlert = function (_a) {
        var _this = this;
        var isLoading = _a.isLoading, errors = _a.errors, parsedTrace = _a.parsedTrace;
        if (isLoading) {
            return null;
        }
        if (!errors || errors.length <= 0) {
            return null;
        }
        var label = tn('There is an error event associated with this transaction event.', "There are %s error events associated with this transaction event.", errors.length);
        // mapping from span ids to the span op and the number of errors in that span
        var errorsMap = {};
        errors.forEach(function (error) {
            if (!errorsMap[error.span]) {
                // first check of the error belongs to the root span
                if (parsedTrace.rootSpanID === error.span) {
                    errorsMap[error.span] = {
                        operation: parsedTrace.op,
                        errorsCount: 0,
                    };
                }
                else {
                    // since it does not belong to the root span, check if it belongs
                    // to one of the other spans in the transaction
                    var span = parsedTrace.spans.find(function (s) { return s.span_id === error.span; });
                    if (!(span === null || span === void 0 ? void 0 : span.op)) {
                        return;
                    }
                    errorsMap[error.span] = {
                        operation: span.op,
                        errorsCount: 0,
                    };
                }
            }
            errorsMap[error.span].errorsCount++;
        });
        return (<AlertContainer>
        <Alert type="error" icon={<IconWarning size="md"/>}>
          <ErrorLabel>{label}</ErrorLabel>
          <AnchorLinkManager.Consumer>
            {function (_a) {
                var scrollToHash = _a.scrollToHash;
                return (<List symbol="bullet">
                {Object.entries(errorsMap).map(function (_a) {
                        var _b = __read(_a, 2), spanId = _b[0], _c = _b[1], operation = _c.operation, errorsCount = _c.errorsCount;
                        return (<ListItem key={spanId}>
                    {tct('[errors] in [link]', {
                                errors: tn('%s error in ', '%s errors in ', errorsCount),
                                link: (<ErrorLink onClick={scrollToSpan(spanId, scrollToHash, _this.props.location)}>
                          {operation}
                        </ErrorLink>),
                            })}
                  </ListItem>);
                    })}
              </List>);
            }}
          </AnchorLinkManager.Consumer>
        </Alert>
      </AlertContainer>);
    };
    SpansInterface.prototype.render = function () {
        var _this = this;
        var _a = this.props, event = _a.event, organization = _a.organization;
        var _b = this.state, parsedTrace = _b.parsedTrace, waterfallModel = _b.waterfallModel;
        return (<Container hasErrors={!objectIsEmpty(event.errors)}>
        <QuickTraceContext.Consumer>
          {function (quickTrace) {
                var _a;
                return (<AnchorLinkManager.Provider>
              {_this.renderTraceErrorsAlert({
                        isLoading: (quickTrace === null || quickTrace === void 0 ? void 0 : quickTrace.isLoading) || false,
                        errors: (_a = quickTrace === null || quickTrace === void 0 ? void 0 : quickTrace.currentEvent) === null || _a === void 0 ? void 0 : _a.errors,
                        parsedTrace: parsedTrace,
                    })}
              <Observer>
                {function () {
                        return (<Search>
                      <Filter operationNameCounts={waterfallModel.operationNameCounts} operationNameFilter={waterfallModel.operationNameFilters} toggleOperationNameFilter={waterfallModel.toggleOperationNameFilter} toggleAllOperationNameFilters={waterfallModel.toggleAllOperationNameFilters}/>
                      <StyledSearchBar defaultQuery="" query={waterfallModel.searchQuery || ''} placeholder={t('Search for spans')} onSearch={_this.handleSpanFilter}/>
                    </Search>);
                    }}
              </Observer>
              <Panel>
                <Observer>
                  {function () {
                        return (<TraceView waterfallModel={waterfallModel} organization={organization}/>);
                    }}
                </Observer>
                <GuideAnchorWrapper>
                  <GuideAnchor target="span_tree" position="bottom"/>
                </GuideAnchorWrapper>
              </Panel>
            </AnchorLinkManager.Provider>);
            }}
        </QuickTraceContext.Consumer>
      </Container>);
    };
    return SpansInterface;
}(PureComponent));
var GuideAnchorWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  height: 0;\n  width: 0;\n  margin-left: 50%;\n"], ["\n  height: 0;\n  width: 0;\n  margin-left: 50%;\n"])));
var Container = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), function (p) {
    return p.hasErrors &&
        "\n  padding: " + space(2) + " 0;\n\n  @media (min-width: " + p.theme.breakpoints[0] + ") {\n    padding: " + space(3) + " 0 0 0;\n  }\n  ";
});
var ErrorLink = styled('a')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  color: ", ";\n  :hover {\n    color: ", ";\n  }\n"], ["\n  color: ", ";\n  :hover {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.textColor; }, function (p) { return p.theme.textColor; });
var Search = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n  width: 100%;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  width: 100%;\n  margin-bottom: ", ";\n"])), space(1));
var StyledSearchBar = styled(SearchBar)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  flex-grow: 1;\n"], ["\n  flex-grow: 1;\n"])));
var AlertContainer = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(1));
var ErrorLabel = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(1));
export default ReactRouter.withRouter(withOrganization(SpansInterface));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=index.jsx.map