import { __assign, __awaiter, __extends, __generator, __makeTemplateObject, __read } from "tslib";
import * as React from 'react';
import styled from '@emotion/styled';
import cloneDeep from 'lodash/cloneDeep';
import pick from 'lodash/pick';
import set from 'lodash/set';
import { validateWidget } from 'app/actionCreators/dashboards';
import { addSuccessMessage } from 'app/actionCreators/indicator';
import WidgetQueryFields from 'app/components/dashboards/widgetQueryFields';
import SelectControl from 'app/components/forms/selectControl';
import * as Layout from 'app/components/layouts/thirds';
import { PanelAlert } from 'app/components/panels';
import { t } from 'app/locale';
import { PageContent } from 'app/styles/organization';
import space from 'app/styles/space';
import { defined } from 'app/utils';
import Measurements from 'app/utils/measurements/measurements';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import withOrganization from 'app/utils/withOrganization';
import withTags from 'app/utils/withTags';
import AsyncView from 'app/views/asyncView';
import WidgetCard from 'app/views/dashboardsV2/widgetCard';
import { generateFieldOptions } from 'app/views/eventsV2/utils';
import { DisplayType } from '../../types';
import BuildStep from '../buildStep';
import BuildSteps from '../buildSteps';
import ChooseDataSetStep from '../choseDataStep';
import Header from '../header';
import { DataSet, displayTypes } from '../utils';
import Queries from './queries';
import { mapErrors, normalizeQueries } from './utils';
var newQuery = {
    name: '',
    fields: ['count()'],
    conditions: '',
    orderby: '',
};
var EventWidget = /** @class */ (function (_super) {
    __extends(EventWidget, _super);
    function EventWidget() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleFieldChange = function (field, value) {
            _this.setState(function (state) {
                var newState = cloneDeep(state);
                if (field === 'displayType') {
                    set(newState, 'queries', normalizeQueries(value, state.queries));
                    if (state.title === t('Custom %s Widget', state.displayType) ||
                        state.title === t('Custom %s Widget', DisplayType.AREA)) {
                        return __assign(__assign({}, newState), { title: t('Custom %s Widget', displayTypes[value]), widgetErrors: undefined });
                    }
                    set(newState, field, value);
                }
                return __assign(__assign({}, newState), { widgetErrors: undefined });
            });
        };
        _this.handleRemoveQuery = function (index) {
            _this.setState(function (state) {
                var newState = cloneDeep(state);
                newState.queries.splice(index, 1);
                return __assign(__assign({}, newState), { widgetErrors: undefined });
            });
        };
        _this.handleAddQuery = function () {
            _this.setState(function (state) {
                var newState = cloneDeep(state);
                newState.queries.push(cloneDeep(newQuery));
                return newState;
            });
        };
        _this.handleChangeQuery = function (index, query) {
            _this.setState(function (state) {
                var newState = cloneDeep(state);
                set(newState, "queries." + index, query);
                return __assign(__assign({}, newState), { widgetErrors: undefined });
            });
        };
        _this.handleSave = function (event) { return __awaiter(_this, void 0, void 0, function () {
            var _a, organization, onAdd, isEditing, onUpdate, widget, widgetData, err_1, widgetErrors;
            var _b;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        event.preventDefault();
                        this.setState({ loading: true });
                        _a = this.props, organization = _a.organization, onAdd = _a.onAdd, isEditing = _a.isEditing, onUpdate = _a.onUpdate, widget = _a.widget;
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, 4, 5]);
                        widgetData = pick(this.state, [
                            'title',
                            'displayType',
                            'interval',
                            'queries',
                        ]);
                        return [4 /*yield*/, validateWidget(this.api, organization.slug, widgetData)];
                    case 2:
                        _c.sent();
                        if (isEditing) {
                            onUpdate(__assign({ id: widget.id }, widgetData));
                            addSuccessMessage(t('Updated widget'));
                            return [2 /*return*/];
                        }
                        onAdd(widgetData);
                        addSuccessMessage(t('Added widget'));
                        return [3 /*break*/, 5];
                    case 3:
                        err_1 = _c.sent();
                        widgetErrors = mapErrors((_b = err_1 === null || err_1 === void 0 ? void 0 : err_1.responseJSON) !== null && _b !== void 0 ? _b : {}, {});
                        this.setState({ widgetErrors: widgetErrors });
                        return [3 /*break*/, 5];
                    case 4:
                        this.setState({ loading: false });
                        return [7 /*endfinally*/];
                    case 5: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    EventWidget.prototype.getDefaultState = function () {
        var widget = this.props.widget;
        if (!widget) {
            return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { title: t('Custom %s Widget', displayTypes[DisplayType.AREA]), displayType: DisplayType.AREA, interval: '5m', queries: [__assign({}, newQuery)] });
        }
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { title: widget.title, displayType: widget.displayType, interval: widget.interval, queries: normalizeQueries(widget.displayType, widget.queries), widgetErrors: undefined });
    };
    EventWidget.prototype.getFirstQueryError = function (field) {
        var _a;
        var _b;
        var widgetErrors = this.state.widgetErrors;
        if (!widgetErrors) {
            return undefined;
        }
        var _c = __read((_b = Object.entries(widgetErrors).find(function (widgetErrorKey, _) { return String(widgetErrorKey) === field; })) !== null && _b !== void 0 ? _b : [], 2), key = _c[0], value = _c[1];
        if (defined(key) && defined(value)) {
            return _a = {}, _a[key] = value, _a;
        }
        return undefined;
    };
    EventWidget.prototype.renderBody = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, onChangeDataSet = _a.onChangeDataSet, selection = _a.selection, tags = _a.tags, isEditing = _a.isEditing, goBackLocation = _a.goBackLocation, dashboardTitle = _a.dashboardTitle, onDelete = _a.onDelete;
        var _b = this.state, title = _b.title, displayType = _b.displayType, queries = _b.queries, interval = _b.interval, widgetErrors = _b.widgetErrors;
        var orgSlug = organization.slug;
        function fieldOptions(measurementKeys) {
            return generateFieldOptions({
                organization: organization,
                tagKeys: Object.values(tags).map(function (_a) {
                    var key = _a.key;
                    return key;
                }),
                measurementKeys: measurementKeys,
            });
        }
        return (<StyledPageContent>
        <Header dashboardTitle={dashboardTitle} orgSlug={orgSlug} title={title} isEditing={isEditing} onChangeTitle={function (newTitle) { return _this.handleFieldChange('title', newTitle); }} onSave={this.handleSave} onDelete={onDelete} goBackLocation={goBackLocation}/>
        <Layout.Body>
          <BuildSteps>
            <BuildStep title={t('Choose your visualization')} description={t('This is a preview of how your widget will appear in the dashboard.')}>
              <VisualizationWrapper>
                <SelectControl name="displayType" options={Object.keys(displayTypes).map(function (value) { return ({
                label: displayTypes[value],
                value: value,
            }); })} value={displayType} onChange={function (option) {
                _this.handleFieldChange('displayType', option.value);
            }} error={widgetErrors === null || widgetErrors === void 0 ? void 0 : widgetErrors.displayType}/>
                <WidgetCard api={this.api} organization={organization} selection={selection} widget={{ title: title, queries: queries, displayType: displayType, interval: interval }} isEditing={false} onDelete={function () { return undefined; }} onEdit={function () { return undefined; }} renderErrorMessage={function (errorMessage) {
                return typeof errorMessage === 'string' && (<PanelAlert type="error">{errorMessage}</PanelAlert>);
            }} isSorting={false} currentWidgetDragging={false}/>
              </VisualizationWrapper>
            </BuildStep>
            <ChooseDataSetStep value={DataSet.EVENTS} onChange={onChangeDataSet}/>
            <BuildStep title={t('Begin your search')} description={t('Add another query to compare projects, tags, etc.')}>
              <Queries queries={queries} selectedProjectIds={selection.projects} organization={organization} displayType={displayType} onRemoveQuery={this.handleRemoveQuery} onAddQuery={this.handleAddQuery} onChangeQuery={this.handleChangeQuery} errors={widgetErrors === null || widgetErrors === void 0 ? void 0 : widgetErrors.queries}/>
            </BuildStep>
            <Measurements organization={organization}>
              {function (_a) {
                var measurements = _a.measurements;
                var measurementKeys = Object.values(measurements).map(function (_a) {
                    var key = _a.key;
                    return key;
                });
                var amendedFieldOptions = fieldOptions(measurementKeys);
                var buildStepContent = (<WidgetQueryFields style={{ padding: 0 }} errors={_this.getFirstQueryError('fields')} displayType={displayType} fieldOptions={amendedFieldOptions} fields={queries[0].fields} organization={organization} onChange={function (fields) {
                        queries.forEach(function (query, queryIndex) {
                            var clonedQuery = cloneDeep(query);
                            clonedQuery.fields = fields;
                            _this.handleChangeQuery(queryIndex, clonedQuery);
                        });
                    }}/>);
                return (<BuildStep title={displayType === DisplayType.TABLE
                        ? t('Choose your columns')
                        : t('Choose your y-axis')} description={t('We’ll use this to determine what gets graphed in the y-axis and any additional overlays.')}>
                    {buildStepContent}
                  </BuildStep>);
            }}
            </Measurements>
          </BuildSteps>
        </Layout.Body>
      </StyledPageContent>);
    };
    return EventWidget;
}(AsyncView));
export default withOrganization(withGlobalSelection(withTags(EventWidget)));
var StyledPageContent = styled(PageContent)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: 0;\n"], ["\n  padding: 0;\n"])));
var VisualizationWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n"])), space(1.5));
var templateObject_1, templateObject_2;
//# sourceMappingURL=index.jsx.map