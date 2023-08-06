import { __assign, __extends, __makeTemplateObject, __rest } from "tslib";
import { components } from 'react-select';
import { withTheme } from '@emotion/react';
import styled from '@emotion/styled';
import cloneDeep from 'lodash/cloneDeep';
import set from 'lodash/set';
import ProjectBadge from 'app/components/idBadge/projectBadge';
import * as Layout from 'app/components/layouts/thirds';
import PickProjectToContinue from 'app/components/pickProjectToContinue';
import { t } from 'app/locale';
import { PageContent } from 'app/styles/organization';
import space from 'app/styles/space';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import withProjects from 'app/utils/withProjects';
import AsyncView from 'app/views/asyncView';
import SelectField from 'app/views/settings/components/forms/selectField';
import BuildStep from '../buildStep';
import BuildSteps from '../buildSteps';
import ChooseDataSetStep from '../choseDataStep';
import Header from '../header';
import { DataSet, DisplayType, displayTypes } from '../utils';
import Card from './card';
import Queries from './queries';
import SearchQueryField from './searchQueryField';
var MetricWidget = /** @class */ (function (_super) {
    __extends(MetricWidget, _super);
    function MetricWidget() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleFieldChange = function (field, value) {
            _this.setState(function (state) {
                var newState = cloneDeep(state);
                if (field === 'displayType') {
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
                return newState;
            });
        };
        _this.handleAddQuery = function () {
            _this.setState(function (state) {
                var newState = cloneDeep(state);
                newState.queries.push({});
                return newState;
            });
        };
        _this.handleChangeQuery = function (index, query) {
            var _a, _b;
            var isMetricNew = ((_a = _this.state.queries[index].metricMeta) === null || _a === void 0 ? void 0 : _a.name) !== ((_b = query.metricMeta) === null || _b === void 0 ? void 0 : _b.name);
            if (isMetricNew) {
                query.aggregation = query.metricMeta ? query.metricMeta.operations[0] : undefined;
            }
            _this.setState(function (state) {
                var newState = cloneDeep(state);
                set(newState, "queries." + index, query);
                return newState;
            });
        };
        _this.handleProjectChange = function (projectId) {
            var _a = _this.props, router = _a.router, location = _a.location;
            // if we change project, we need to sync the project slug in the URL
            router.replace({
                pathname: location.pathname,
                query: __assign(__assign({}, location.query), { project: projectId }),
            });
        };
        return _this;
    }
    MetricWidget.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { title: t('Custom %s Widget', displayTypes[DisplayType.AREA]), displayType: DisplayType.AREA, metricMetas: [], metricTags: [], queries: [{}] });
    };
    Object.defineProperty(MetricWidget.prototype, "project", {
        get: function () {
            var _a = this.props, projects = _a.projects, location = _a.location;
            var query = location.query;
            var projectId = query.project;
            return projects.find(function (project) { return project.id === projectId; });
        },
        enumerable: false,
        configurable: true
    });
    MetricWidget.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, loadingProjects = _a.loadingProjects;
        if (this.isProjectMissingInUrl() || loadingProjects || !this.project) {
            return [];
        }
        var orgSlug = organization.slug;
        var projectSlug = this.project.slug;
        return [
            ['metricMetas', "/projects/" + orgSlug + "/" + projectSlug + "/metrics/meta/"],
            ['metricTags', "/projects/" + orgSlug + "/" + projectSlug + "/metrics/tags/"],
        ];
    };
    MetricWidget.prototype.componentDidUpdate = function (prevProps, prevState) {
        var _a, _b;
        if (prevProps.loadingProjects && !this.props.loadingProjects) {
            this.reloadData();
        }
        if (!((_a = prevState.metricMetas) === null || _a === void 0 ? void 0 : _a.length) && !!((_b = this.state.metricMetas) === null || _b === void 0 ? void 0 : _b.length)) {
            this.handleChangeQuery(0, { metricMeta: this.state.metricMetas[0] });
        }
        _super.prototype.componentDidUpdate.call(this, prevProps, prevState);
    };
    MetricWidget.prototype.isProjectMissingInUrl = function () {
        var projectId = this.props.location.query.project;
        return !projectId || typeof projectId !== 'string';
    };
    MetricWidget.prototype.renderBody = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, router = _a.router, projects = _a.projects, onChangeDataSet = _a.onChangeDataSet, selection = _a.selection, location = _a.location, loadingProjects = _a.loadingProjects, goBackLocation = _a.goBackLocation, dashboardTitle = _a.dashboardTitle;
        var _b = this.state, title = _b.title, metricTags = _b.metricTags, searchQuery = _b.searchQuery, metricMetas = _b.metricMetas, queries = _b.queries, displayType = _b.displayType;
        var orgSlug = organization.slug;
        if (loadingProjects) {
            return this.renderLoading();
        }
        var selectedProject = this.project;
        if (this.isProjectMissingInUrl() || !selectedProject) {
            return (<PickProjectToContinue router={router} projects={projects.map(function (project) { return ({ id: project.id, slug: project.slug }); })} nextPath={{
                    pathname: location.pathname,
                    query: location.query,
                }} noProjectRedirectPath={goBackLocation}/>);
        }
        if (!metricTags || !metricMetas) {
            return null;
        }
        return (<StyledPageContent>
        <Header orgSlug={orgSlug} title={title} dashboardTitle={dashboardTitle} goBackLocation={goBackLocation} onChangeTitle={function (newTitle) { return _this.handleFieldChange('title', newTitle); }}/>
        <Layout.Body>
          <BuildSteps>
            <BuildStep title={t('Choose your visualization')} description={t('This is a preview of how your widget will appear in the dashboard.')}>
              <VisualizationWrapper>
                <StyledSelectField name="displayType" choices={[DisplayType.LINE, DisplayType.BAR, DisplayType.AREA].map(function (value) { return [value, displayTypes[value]]; })} value={displayType} onChange={function (value) {
                _this.handleFieldChange('displayType', value);
            }} inline={false} flexibleControlStateSize stacked/>
                <Card router={router} location={location} selection={selection} organization={organization} api={this.api} project={selectedProject} widget={{
                title: title,
                searchQuery: searchQuery,
                displayType: displayType,
                groupings: queries,
            }}/>
              </VisualizationWrapper>
            </BuildStep>
            <ChooseDataSetStep value={DataSet.METRICS} onChange={onChangeDataSet}/>
            <BuildStep title={t('Choose your project')} description={t('You’ll need to select a project to set metrics on.')}>
              <StyledSelectField name="project" choices={projects.map(function (project) { return [project, project.slug]; })} onChange={function (project) { return _this.handleProjectChange(project.id); }} value={selectedProject} components={{
                Option: function (_a) {
                    var label = _a.label, optionProps = __rest(_a, ["label"]);
                    var data = optionProps.data;
                    return (<components.Option label={label} {...optionProps}>
                        <ProjectBadge project={data.value} avatarSize={18} disableLink/>
                      </components.Option>);
                },
                SingleValue: function (_a) {
                    var data = _a.data, props = __rest(_a, ["data"]);
                    return (<components.SingleValue data={data} {...props}>
                      <ProjectBadge project={data.value} avatarSize={18} disableLink/>
                    </components.SingleValue>);
                },
            }} styles={{
                control: function (provided) { return (__assign(__assign({}, provided), { boxShadow: 'none' })); },
            }} allowClear={false} inline={false} flexibleControlStateSize stacked/>
            </BuildStep>
            <BuildStep title={t('Begin your search')} description={t('Select a tag to compare releases, session data, etc.')}>
              <SearchQueryField api={this.api} tags={metricTags} orgSlug={orgSlug} projectSlug={selectedProject.slug} query={searchQuery} onSearch={function (newQuery) { return _this.handleFieldChange('searchQuery', newQuery); }} onBlur={function (newQuery) { return _this.handleFieldChange('searchQuery', newQuery); }}/>
            </BuildStep>
            <BuildStep title={t('Add queries')} description={t('We’ll use this to determine what gets graphed in the y-axis and any additional overlays.')}>
              <Queries metricMetas={metricMetas} metricTags={metricTags} queries={queries} onAddQuery={this.handleAddQuery} onRemoveQuery={this.handleRemoveQuery} onChangeQuery={this.handleChangeQuery}/>
            </BuildStep>
          </BuildSteps>
        </Layout.Body>
      </StyledPageContent>);
    };
    return MetricWidget;
}(AsyncView));
export default withTheme(withProjects(withGlobalSelection(MetricWidget)));
var StyledPageContent = styled(PageContent)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: 0;\n"], ["\n  padding: 0;\n"])));
var StyledSelectField = styled(SelectField)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  padding-right: 0;\n"], ["\n  padding-right: 0;\n"])));
var VisualizationWrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n"])), space(1.5));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=index.jsx.map