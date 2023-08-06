import { __assign, __extends, __makeTemplateObject, __read } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import AsyncComponent from 'app/components/asyncComponent';
import Pagination from 'app/components/pagination';
import { t } from 'app/locale';
import { sortProjects } from 'app/utils';
import { MIN_PROJECTS_FOR_PAGINATION, MIN_PROJECTS_FOR_SEARCH, } from 'app/views/settings/account/notifications/constants';
import { getParentData, getParentField, groupByOrganization, } from 'app/views/settings/account/notifications/utils';
import { SearchWrapper, } from 'app/views/settings/components/defaultSearchBar';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import Form from 'app/views/settings/components/forms/form';
import JsonForm from 'app/views/settings/components/forms/jsonForm';
var NotificationSettingsByProjects = /** @class */ (function (_super) {
    __extends(NotificationSettingsByProjects, _super);
    function NotificationSettingsByProjects() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.getProjectCount = function () {
            var _a;
            /** Check the notification settings for how many projects there are. */
            var _b = _this.props, notificationType = _b.notificationType, notificationSettings = _b.notificationSettings;
            return Object.values(((_a = notificationSettings[notificationType]) === null || _a === void 0 ? void 0 : _a.project) || {}).length;
        };
        _this.getGroupedProjects = function () {
            /**
             * The UI expects projects to be grouped by organization but can also use
             * this function to make a single group with all organizations.
             */
            var stateProjects = _this.state.projects;
            return Object.fromEntries(Object.values(groupByOrganization(sortProjects(stateProjects))).map(function (_a) {
                var organization = _a.organization, projects = _a.projects;
                return [organization.name + " Projects", projects];
            }));
        };
        return _this;
    }
    NotificationSettingsByProjects.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { projects: [] });
    };
    NotificationSettingsByProjects.prototype.getEndpoints = function () {
        return [['projects', '/projects/']];
    };
    NotificationSettingsByProjects.prototype.renderBody = function () {
        var _a = this.props, notificationType = _a.notificationType, notificationSettings = _a.notificationSettings, onChange = _a.onChange;
        var _b = this.state, projects = _b.projects, projectsPageLinks = _b.projectsPageLinks;
        var canSearch = this.getProjectCount() >= MIN_PROJECTS_FOR_SEARCH;
        var shouldPaginate = projects.length >= MIN_PROJECTS_FOR_PAGINATION;
        // eslint-disable-next-line react/prop-types
        var renderSearch = function (_a) {
            var defaultSearchBar = _a.defaultSearchBar;
            return (<StyledSearchWrapper>{defaultSearchBar}</StyledSearchWrapper>);
        };
        return (<React.Fragment>
        {canSearch &&
                this.renderSearchInput({
                    stateKey: 'projects',
                    url: '/projects/',
                    placeholder: t('Search Projects'),
                    children: renderSearch,
                })}
        <Form saveOnBlur apiMethod="PUT" apiEndpoint="/users/me/notification-settings/" initialData={getParentData(notificationType, notificationSettings, projects)}>
          {projects.length === 0 ? (<EmptyMessage>{t('No projects found')}</EmptyMessage>) : (Object.entries(this.getGroupedProjects()).map(function (_a) {
                var _b = __read(_a, 2), groupTitle = _b[0], parents = _b[1];
                return (<JsonForm key={groupTitle} title={groupTitle} fields={parents.map(function (parent) {
                        return getParentField(notificationType, notificationSettings, parent, onChange);
                    })}/>);
            }))}
        </Form>
        {canSearch && shouldPaginate && (<Pagination pageLinks={projectsPageLinks} {...this.props}/>)}
      </React.Fragment>);
    };
    return NotificationSettingsByProjects;
}(AsyncComponent));
export default NotificationSettingsByProjects;
var StyledSearchWrapper = styled(SearchWrapper)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  * {\n    width: 100%;\n  }\n"], ["\n  * {\n    width: 100%;\n  }\n"])));
var templateObject_1;
//# sourceMappingURL=notificationSettingsByProjects.jsx.map