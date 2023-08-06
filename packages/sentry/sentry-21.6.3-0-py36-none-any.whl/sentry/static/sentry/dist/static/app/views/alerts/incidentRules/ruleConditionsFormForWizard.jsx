var _a;
import { __assign, __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import * as React from 'react';
import styled from '@emotion/styled';
import { addErrorMessage } from 'app/actionCreators/indicator';
import SearchBar from 'app/components/events/searchBar';
import SelectControl from 'app/components/forms/selectControl';
import ListItem from 'app/components/list/listItem';
import { Panel, PanelBody } from 'app/components/panels';
import Tooltip from 'app/components/tooltip';
import { IconQuestion } from 'app/icons';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import { getDisplayName } from 'app/utils/environment';
import theme from 'app/utils/theme';
import { convertDatasetEventTypesToSource, DATA_SOURCE_LABELS, DATA_SOURCE_TO_SET_AND_EVENT_TYPES, } from 'app/views/alerts/utils';
import { getFunctionHelpText } from 'app/views/alerts/wizard/options';
import FormField from 'app/views/settings/components/forms/formField';
import SelectField from 'app/views/settings/components/forms/selectField';
import { DEFAULT_AGGREGATE, DEFAULT_TRANSACTION_AGGREGATE } from './constants';
import MetricField from './metricField';
import { Datasource, TimeWindow } from './types';
var TIME_WINDOW_MAP = (_a = {},
    _a[TimeWindow.ONE_MINUTE] = t('1 minute'),
    _a[TimeWindow.FIVE_MINUTES] = t('5 minutes'),
    _a[TimeWindow.TEN_MINUTES] = t('10 minutes'),
    _a[TimeWindow.FIFTEEN_MINUTES] = t('15 minutes'),
    _a[TimeWindow.THIRTY_MINUTES] = t('30 minutes'),
    _a[TimeWindow.ONE_HOUR] = t('1 hour'),
    _a[TimeWindow.TWO_HOURS] = t('2 hours'),
    _a[TimeWindow.FOUR_HOURS] = t('4 hours'),
    _a[TimeWindow.ONE_DAY] = t('24 hours'),
    _a);
var RuleConditionsFormForWizard = /** @class */ (function (_super) {
    __extends(RuleConditionsFormForWizard, _super);
    function RuleConditionsFormForWizard() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            environments: null,
        };
        return _this;
    }
    RuleConditionsFormForWizard.prototype.componentDidMount = function () {
        this.fetchData();
    };
    RuleConditionsFormForWizard.prototype.fetchData = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, api, organization, projectSlug, environments, _err_1;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, organization = _a.organization, projectSlug = _a.projectSlug;
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/projects/" + organization.slug + "/" + projectSlug + "/environments/", {
                                query: {
                                    visibility: 'visible',
                                },
                            })];
                    case 2:
                        environments = _b.sent();
                        this.setState({ environments: environments });
                        return [3 /*break*/, 4];
                    case 3:
                        _err_1 = _b.sent();
                        addErrorMessage(t('Unable to fetch environments'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    RuleConditionsFormForWizard.prototype.render = function () {
        var _a;
        var _b = this.props, organization = _b.organization, disabled = _b.disabled, onFilterSearch = _b.onFilterSearch, allowChangeEventTypes = _b.allowChangeEventTypes, alertType = _b.alertType;
        var environments = this.state.environments;
        var environmentOptions = (_a = environments === null || environments === void 0 ? void 0 : environments.map(function (env) { return ({
            value: env.name,
            label: getDisplayName(env),
        }); })) !== null && _a !== void 0 ? _a : [];
        var anyEnvironmentLabel = (<React.Fragment>
        {t('All')}
        <div className="all-environment-note">
          {tct("This will count events across every environment. For example,\n             having 50 [code1:production] events and 50 [code2:development]\n             events would trigger an alert with a critical threshold of 100.", { code1: <code />, code2: <code /> })}
        </div>
      </React.Fragment>);
        environmentOptions.unshift({ value: null, label: anyEnvironmentLabel });
        var dataSourceOptions = [
            {
                label: t('Errors'),
                options: [
                    {
                        value: Datasource.ERROR_DEFAULT,
                        label: DATA_SOURCE_LABELS[Datasource.ERROR_DEFAULT],
                    },
                    {
                        value: Datasource.DEFAULT,
                        label: DATA_SOURCE_LABELS[Datasource.DEFAULT],
                    },
                    {
                        value: Datasource.ERROR,
                        label: DATA_SOURCE_LABELS[Datasource.ERROR],
                    },
                ],
            },
        ];
        if (organization.features.includes('performance-view') && alertType === 'custom') {
            dataSourceOptions.push({
                label: t('Transactions'),
                options: [
                    {
                        value: Datasource.TRANSACTION,
                        label: DATA_SOURCE_LABELS[Datasource.TRANSACTION],
                    },
                ],
            });
        }
        var formElemBaseStyle = {
            padding: "" + space(0.5),
            border: 'none',
        };
        var _c = getFunctionHelpText(alertType), intervalLabelText = _c.labelText, timeWindowText = _c.timeWindowText;
        return (<React.Fragment>
        <ChartPanel>
          <StyledPanelBody>{this.props.thresholdChart}</StyledPanelBody>
        </ChartPanel>
        <StyledListItem>{t('Filter events')}</StyledListItem>
        <FormRow>
          <SelectField name="environment" placeholder={t('All')} style={__assign(__assign({}, formElemBaseStyle), { minWidth: 180, flex: 1 })} styles={{
                singleValue: function (base) { return (__assign(__assign({}, base), { '.all-environment-note': { display: 'none' } })); },
                option: function (base, state) { return (__assign(__assign({}, base), { '.all-environment-note': __assign(__assign({}, (!state.isSelected && !state.isFocused
                        ? { color: theme.gray400 }
                        : {})), { fontSize: theme.fontSizeSmall }) })); },
            }} options={environmentOptions} isDisabled={disabled || this.state.environments === null} isClearable inline={false} flexibleControlStateSize inFieldLabel={t('Env: ')}/>
          {allowChangeEventTypes && (<FormField name="datasource" inline={false} style={__assign(__assign({}, formElemBaseStyle), { minWidth: 300, flex: 2 })} flexibleControlStateSize>
              {function (_a) {
                    var onChange = _a.onChange, onBlur = _a.onBlur, model = _a.model;
                    var formDataset = model.getValue('dataset');
                    var formEventTypes = model.getValue('eventTypes');
                    var mappedValue = convertDatasetEventTypesToSource(formDataset, formEventTypes);
                    return (<SelectControl value={mappedValue} inFieldLabel={t('Events: ')} onChange={function (optionObj) {
                            var _a;
                            var optionValue = optionObj.value;
                            onChange(optionValue, {});
                            onBlur(optionValue, {});
                            // Reset the aggregate to the default (which works across
                            // datatypes), otherwise we may send snuba an invalid query
                            // (transaction aggregate on events datasource = bad).
                            optionValue === 'transaction'
                                ? model.setValue('aggregate', DEFAULT_TRANSACTION_AGGREGATE)
                                : model.setValue('aggregate', DEFAULT_AGGREGATE);
                            // set the value of the dataset and event type from data source
                            var _b = (_a = DATA_SOURCE_TO_SET_AND_EVENT_TYPES[optionValue]) !== null && _a !== void 0 ? _a : {}, dataset = _b.dataset, eventTypes = _b.eventTypes;
                            model.setValue('dataset', dataset);
                            model.setValue('eventTypes', eventTypes);
                        }} options={dataSourceOptions} isDisabled={disabled} required/>);
                }}
            </FormField>)}
          <FormField name="query" inline={false} style={__assign(__assign({}, formElemBaseStyle), { flex: '6 0 500px' })} flexibleControlStateSize>
            {function (_a) {
                var _b;
                var onChange = _a.onChange, onBlur = _a.onBlur, onKeyDown = _a.onKeyDown, initialData = _a.initialData, model = _a.model;
                return (<SearchContainer>
                <StyledSearchBar defaultQuery={(_b = initialData === null || initialData === void 0 ? void 0 : initialData.query) !== null && _b !== void 0 ? _b : ''} omitTags={['event.type']} disabled={disabled} useFormWrapper={false} organization={organization} placeholder={model.getValue('dataset') === 'events'
                        ? t('Filter events by level, message, or other properties...')
                        : t('Filter transactions by URL, tags, and other properties...')} onChange={onChange} onKeyDown={function (e) {
                        /**
                         * Do not allow enter key to submit the alerts form since it is unlikely
                         * users will be ready to create the rule as this sits above required fields.
                         */
                        if (e.key === 'Enter') {
                            e.preventDefault();
                            e.stopPropagation();
                        }
                        onKeyDown === null || onKeyDown === void 0 ? void 0 : onKeyDown(e);
                    }} onBlur={function (query) {
                        onFilterSearch(query);
                        onBlur(query);
                    }} onSearch={function (query) {
                        onFilterSearch(query);
                        onChange(query, {});
                    }}/>
              </SearchContainer>);
            }}
          </FormField>
        </FormRow>
        <StyledListItem>
          <StyledListTitle>
            <div>{intervalLabelText}</div>
            <Tooltip title={t('Time window over which the metric is evaluated. Alerts are evaluated every minute regardless of this value.')}>
              <IconQuestion size="sm" color="gray200"/>
            </Tooltip>
          </StyledListTitle>
        </StyledListItem>
        <FormRow>
          {timeWindowText && (<MetricField name="aggregate" help={null} organization={organization} disabled={disabled} style={__assign({}, formElemBaseStyle)} inline={false} flexibleControlStateSize columnWidth={200} alertType={alertType} required/>)}
          {timeWindowText && <FormRowText>{timeWindowText}</FormRowText>}
          <SelectField name="timeWindow" style={__assign(__assign({}, formElemBaseStyle), { flex: '0 150px 0', minWidth: 130, maxWidth: 300 })} choices={Object.entries(TIME_WINDOW_MAP)} required isDisabled={disabled} getValue={function (value) { return Number(value); }} setValue={function (value) { return "" + value; }} inline={false} flexibleControlStateSize/>
        </FormRow>
      </React.Fragment>);
    };
    return RuleConditionsFormForWizard;
}(React.PureComponent));
var StyledListTitle = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  span {\n    margin-left: ", ";\n  }\n"], ["\n  display: flex;\n  span {\n    margin-left: ", ";\n  }\n"])), space(1));
var ChartPanel = styled(Panel)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(4));
var StyledPanelBody = styled(PanelBody)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  ol,\n  h4 {\n    margin-bottom: ", ";\n  }\n"], ["\n  ol,\n  h4 {\n    margin-bottom: ", ";\n  }\n"])), space(1));
var SearchContainer = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var StyledSearchBar = styled(SearchBar)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  flex-grow: 1;\n"], ["\n  flex-grow: 1;\n"])));
var StyledListItem = styled(ListItem)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  margin-bottom: ", ";\n  font-size: ", ";\n  line-height: 1.3;\n"], ["\n  margin-bottom: ", ";\n  font-size: ", ";\n  line-height: 1.3;\n"])), space(1), function (p) { return p.theme.fontSizeExtraLarge; });
var FormRow = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: row;\n  align-items: center;\n  flex-wrap: wrap;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  flex-direction: row;\n  align-items: center;\n  flex-wrap: wrap;\n  margin-bottom: ", ";\n"])), space(4));
var FormRowText = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  margin: ", ";\n"], ["\n  margin: ", ";\n"])), space(1));
export default RuleConditionsFormForWizard;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=ruleConditionsFormForWizard.jsx.map