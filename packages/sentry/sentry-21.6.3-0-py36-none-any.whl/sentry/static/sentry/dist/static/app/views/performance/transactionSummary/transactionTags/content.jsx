import { __assign, __makeTemplateObject, __read, __spreadArray } from "tslib";
import React, { Fragment, useEffect, useState } from 'react';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import { SectionHeading } from 'app/components/charts/styles';
import SearchBar from 'app/components/events/searchBar';
import { getParams } from 'app/components/organizations/globalSelectionHeader/getParams';
import QuestionTooltip from 'app/components/questionTooltip';
import Radio from 'app/components/radio';
import { t } from 'app/locale';
import space from 'app/styles/space';
import SegmentExplorerQuery from 'app/utils/performance/segmentExplorer/segmentExplorerQuery';
import { decodeScalar } from 'app/utils/queryString';
import { SidebarSpacer } from 'app/views/performance/transactionSummary/utils';
import { getCurrentLandingDisplay, LandingDisplayField } from '../../landing/utils';
import { SpanOperationBreakdownFilter } from '../filter';
import TransactionHeader, { Tab } from '../header';
import { getTransactionField } from '../tagExplorer';
import TagsDisplay from './tagsDisplay';
import { decodeSelectedTagKey } from './utils';
var TagsPageContent = function (props) {
    var eventView = props.eventView, location = props.location, organization = props.organization, projects = props.projects, transactionName = props.transactionName;
    var handleIncompatibleQuery = function () { };
    var aggregateColumn = getTransactionField(SpanOperationBreakdownFilter.None, projects, eventView);
    return (<Fragment>
      <TransactionHeader eventView={eventView} location={location} organization={organization} projects={projects} transactionName={transactionName} currentTab={Tab.Tags} hasWebVitals={getCurrentLandingDisplay(location, projects, eventView).field ===
            LandingDisplayField.FRONTEND_PAGELOAD} handleIncompatibleQuery={handleIncompatibleQuery}/>

      <SegmentExplorerQuery eventView={eventView} orgSlug={organization.slug} location={location} aggregateColumn={aggregateColumn} limit={20} sort="-sumdelta" allTagKeys>
        {function (_a) {
            var isLoading = _a.isLoading, tableData = _a.tableData;
            return <InnerContent {...props} isLoading={isLoading} tableData={tableData}/>;
        }}
      </SegmentExplorerQuery>
    </Fragment>);
};
function getTagKeyOptions(tableData) {
    var suspectTags = [];
    var otherTags = [];
    tableData.data.forEach(function (row) {
        var tagArray = row.comparison > 1 ? suspectTags : otherTags;
        tagArray.push(row.tags_key);
    });
    return {
        suspectTags: suspectTags,
        otherTags: otherTags,
    };
}
var InnerContent = function (props) {
    var _eventView = props.eventView, location = props.location, organization = props.organization, tableData = props.tableData;
    var eventView = _eventView.clone();
    if (!tableData) {
        return null;
    }
    var tagOptions = getTagKeyOptions(tableData);
    var decodedTagKey = decodeSelectedTagKey(location);
    var allTags = __spreadArray(__spreadArray([], __read(tagOptions.suspectTags)), __read(tagOptions.otherTags));
    var decodedTagFromOptions = decodedTagKey
        ? allTags.find(function (tag) { return tag === decodedTagKey; })
        : undefined;
    var defaultTag = tagOptions.suspectTags.length
        ? tagOptions.suspectTags[0]
        : tagOptions.otherTags.length
            ? tagOptions.otherTags[0]
            : '';
    var initialTag = decodedTagFromOptions !== null && decodedTagFromOptions !== void 0 ? decodedTagFromOptions : defaultTag;
    var _a = __read(useState(initialTag), 2), tagSelected = _a[0], _changeTagSelected = _a[1];
    var changeTagSelected = function (tagKey) {
        var queryParams = getParams(__assign(__assign({}, (location.query || {})), { tagKey: tagKey }));
        browserHistory.push({
            pathname: location.pathname,
            query: queryParams,
        });
        _changeTagSelected(tagKey);
    };
    useEffect(function () {
        if (!decodedTagFromOptions) {
            changeTagSelected(initialTag);
        }
    }, [decodedTagFromOptions]);
    var handleSearch = function (query) {
        var queryParams = getParams(__assign(__assign({}, (location.query || {})), { query: query }));
        browserHistory.push({
            pathname: location.pathname,
            query: queryParams,
        });
    };
    var changeTag = function (tag) {
        return changeTagSelected(tag);
    };
    if (tagSelected) {
        eventView.additionalConditions.setTagValues('has', [tagSelected]);
    }
    var query = decodeScalar(location.query.query, '');
    return (<ReversedLayoutBody>
      <TagsSideBar suspectTags={tagOptions.suspectTags} otherTags={tagOptions.otherTags} tagSelected={tagSelected} changeTag={changeTag}/>
      <StyledMain>
        <StyledActions>
          <StyledSearchBar organization={organization} projectIds={eventView.project} query={query} fields={eventView.fields} onSearch={handleSearch}/>
        </StyledActions>
        <TagsDisplay {...props} tagKey={tagSelected}/>
      </StyledMain>
    </ReversedLayoutBody>);
};
var TagsSideBar = function (props) {
    var suspectTags = props.suspectTags, otherTags = props.otherTags, changeTag = props.changeTag, tagSelected = props.tagSelected;
    return (<StyledSide>
      {suspectTags.length ? (<React.Fragment>
          <StyledSectionHeading>
            {t('Suspect Tags')}
            <QuestionTooltip position="top" title={t('Suspect tags are tags that often correspond to slower transaction')} size="sm"/>
          </StyledSectionHeading>
          {suspectTags.map(function (tag) { return (<RadioLabel key={tag}>
              <Radio aria-label={tag} checked={tagSelected === tag} onChange={function () { return changeTag(tag); }}/>
              <SidebarTagValue className="truncate">{tag}</SidebarTagValue>
            </RadioLabel>); })}

          <SidebarSpacer />
        </React.Fragment>) : null}
      {otherTags.length ? (<StyledSectionHeading>
          {t('Other Tags')}
          <QuestionTooltip position="top" title={t('Other common tags for this transaction')} size="sm"/>
        </StyledSectionHeading>) : null}
      {otherTags.map(function (tag) { return (<RadioLabel key={tag}>
          <Radio aria-label={tag} checked={tagSelected === tag} onChange={function () { return changeTag(tag); }}/>
          <SidebarTagValue className="truncate">{tag}</SidebarTagValue>
        </RadioLabel>); })}
    </StyledSide>);
};
var RadioLabel = styled('label')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  cursor: pointer;\n  margin-bottom: ", ";\n  font-weight: normal;\n  display: grid;\n  grid-auto-flow: column;\n  grid-auto-columns: max-content 1fr;\n  align-items: center;\n  grid-gap: ", ";\n"], ["\n  cursor: pointer;\n  margin-bottom: ", ";\n  font-weight: normal;\n  display: grid;\n  grid-auto-flow: column;\n  grid-auto-columns: max-content 1fr;\n  align-items: center;\n  grid-gap: ", ";\n"])), space(1), space(1));
var SidebarTagValue = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  width: 100%;\n"], ["\n  width: 100%;\n"])));
var StyledSectionHeading = styled(SectionHeading)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(2));
// TODO(k-fish): Adjust thirds layout to allow for this instead.
var ReversedLayoutBody = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  padding: ", ";\n  margin: 0;\n  background-color: ", ";\n  flex-grow: 1;\n\n  @media (min-width: ", ") {\n    padding: ", " ", ";\n  }\n\n  @media (min-width: ", ") {\n    display: grid;\n    grid-template-columns: auto 66%;\n    align-content: start;\n    grid-gap: ", ";\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: 225px minmax(100px, auto);\n  }\n"], ["\n  padding: ", ";\n  margin: 0;\n  background-color: ", ";\n  flex-grow: 1;\n\n  @media (min-width: ", ") {\n    padding: ", " ", ";\n  }\n\n  @media (min-width: ", ") {\n    display: grid;\n    grid-template-columns: auto 66%;\n    align-content: start;\n    grid-gap: ", ";\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: 225px minmax(100px, auto);\n  }\n"])), space(2), function (p) { return p.theme.background; }, function (p) { return p.theme.breakpoints[0]; }, space(3), space(4), function (p) { return p.theme.breakpoints[1]; }, space(3), function (p) { return p.theme.breakpoints[2]; });
var StyledSide = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  grid-column: 1/2;\n"], ["\n  grid-column: 1/2;\n"])));
var StyledMain = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  grid-column: 2/4;\n  max-width: 100%;\n"], ["\n  grid-column: 2/4;\n  max-width: 100%;\n"])));
var StyledSearchBar = styled(SearchBar)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  flex-grow: 1;\n"], ["\n  flex-grow: 1;\n"])));
var StyledActions = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(1));
export default TagsPageContent;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=content.jsx.map