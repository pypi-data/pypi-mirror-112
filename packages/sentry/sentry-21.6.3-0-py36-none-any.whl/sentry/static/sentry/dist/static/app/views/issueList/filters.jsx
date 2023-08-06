import { __extends, __makeTemplateObject } from "tslib";
import * as React from 'react';
import { ClassNames } from '@emotion/react';
import styled from '@emotion/styled';
import Feature from 'app/components/acl/feature';
import GuideAnchor from 'app/components/assistant/guideAnchor';
import ButtonBar from 'app/components/buttonBar';
import { PageHeader } from 'app/styles/organization';
import space from 'app/styles/space';
import IssueListDisplayOptions from './displayOptions';
import IssueListSearchBar from './searchBar';
import IssueListSortOptions from './sortOptions';
var IssueListFilters = /** @class */ (function (_super) {
    __extends(IssueListFilters, _super);
    function IssueListFilters() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    IssueListFilters.prototype.render = function () {
        var _a = this.props, organization = _a.organization, savedSearch = _a.savedSearch, query = _a.query, isSearchDisabled = _a.isSearchDisabled, sort = _a.sort, display = _a.display, hasSessions = _a.hasSessions, selectedProjects = _a.selectedProjects, onSidebarToggle = _a.onSidebarToggle, onSearch = _a.onSearch, onSortChange = _a.onSortChange, onDisplayChange = _a.onDisplayChange, tagValueLoader = _a.tagValueLoader, tags = _a.tags;
        var isAssignedQuery = /\bassigned:/.test(query);
        return (<PageHeader>
        <SearchContainer>
          <ClassNames>
            {function (_a) {
                var css = _a.css;
                return (<GuideAnchor target="assigned_or_suggested_query" disabled={!isAssignedQuery} containerClassName={css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n                  width: 100%;\n                "], ["\n                  width: 100%;\n                "])))}>
                <IssueListSearchBar organization={organization} query={query || ''} sort={sort} onSearch={onSearch} disabled={isSearchDisabled} excludeEnvironment supportedTags={tags} tagValueLoader={tagValueLoader} savedSearch={savedSearch} onSidebarToggle={onSidebarToggle}/>
              </GuideAnchor>);
            }}
          </ClassNames>
          <ButtonBar gap={1}>
            <Feature features={['issue-percent-display']} organization={organization}>
              <IssueListDisplayOptions onDisplayChange={onDisplayChange} display={display} hasSessions={hasSessions} hasMultipleProjectsSelected={selectedProjects.length !== 1}/>
            </Feature>
            <IssueListSortOptions sort={sort} query={query} onSelect={onSortChange}/>
          </ButtonBar>
        </SearchContainer>
      </PageHeader>);
    };
    return IssueListFilters;
}(React.Component));
var SearchContainer = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  grid-gap: ", ";\n  align-items: start;\n  width: 100%;\n"], ["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  grid-gap: ", ";\n  align-items: start;\n  width: 100%;\n"])), space(1));
export default IssueListFilters;
var templateObject_1, templateObject_2;
//# sourceMappingURL=filters.jsx.map