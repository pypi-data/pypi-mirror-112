import { __assign, __extends, __makeTemplateObject, __read, __rest } from "tslib";
import { Component, Fragment } from 'react';
import styled from '@emotion/styled';
import round from 'lodash/round';
import { loadStatsForProject } from 'app/actionCreators/projects';
import IdBadge from 'app/components/idBadge';
import Link from 'app/components/links/link';
import Placeholder from 'app/components/placeholder';
import BookmarkStar from 'app/components/projects/bookmarkStar';
import QuestionTooltip from 'app/components/questionTooltip';
import ScoreCard, { HeaderTitle, Score, ScoreWrapper, StyledPanel, Trend, } from 'app/components/scoreCard';
import { releaseHealth } from 'app/data/platformCategories';
import { IconArrow } from 'app/icons';
import { t } from 'app/locale';
import ProjectsStatsStore from 'app/stores/projectsStatsStore';
import space from 'app/styles/space';
import { defined } from 'app/utils';
import { callIfFunction } from 'app/utils/callIfFunction';
import { formatAbbreviatedNumber } from 'app/utils/formatters';
import withApi from 'app/utils/withApi';
import withOrganization from 'app/utils/withOrganization';
import MissingReleasesButtons, { StyledButtonBar, } from 'app/views/projectDetail/missingFeatureButtons/missingReleasesButtons';
import { CRASH_FREE_DECIMAL_THRESHOLD, displayCrashFreePercent, } from 'app/views/releases/utils';
import Chart from './chart';
import Deploys, { DeployRows, GetStarted, TextOverflow } from './deploys';
var ProjectCard = /** @class */ (function (_super) {
    __extends(ProjectCard, _super);
    function ProjectCard() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ProjectCard.prototype.componentDidMount = function () {
        var _a = this.props, organization = _a.organization, project = _a.project, api = _a.api;
        // fetch project stats
        loadStatsForProject(api, project.id, {
            orgId: organization.slug,
            projectId: project.id,
            query: {
                transactionStats: this.hasPerformance ? '1' : undefined,
                sessionStats: '1',
            },
        });
    };
    Object.defineProperty(ProjectCard.prototype, "hasPerformance", {
        get: function () {
            return this.props.organization.features.includes('performance-view');
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectCard.prototype, "crashFreeTrend", {
        get: function () {
            var _a = this.props.project.sessionStats || {}, currentCrashFreeRate = _a.currentCrashFreeRate, previousCrashFreeRate = _a.previousCrashFreeRate;
            if (!defined(currentCrashFreeRate) || !defined(previousCrashFreeRate)) {
                return undefined;
            }
            return round(currentCrashFreeRate - previousCrashFreeRate, currentCrashFreeRate > CRASH_FREE_DECIMAL_THRESHOLD ? 3 : 0);
        },
        enumerable: false,
        configurable: true
    });
    ProjectCard.prototype.renderMissingFeatureCard = function () {
        var _a = this.props, organization = _a.organization, project = _a.project;
        if (project.platform && releaseHealth.includes(project.platform)) {
            return (<ScoreCard title={t('Crash Free Sessions')} score={<MissingReleasesButtons organization={organization} health/>}/>);
        }
        return (<ScoreCard title={t('Crash Free Sessions')} score={<NotAvailable>
            {t('Not Available')}
            <QuestionTooltip title={t('Release Health is not yet supported on this platform.')} size="xs"/>
          </NotAvailable>}/>);
    };
    ProjectCard.prototype.renderTrend = function () {
        var currentCrashFreeRate = (this.props.project.sessionStats || {}).currentCrashFreeRate;
        if (!defined(currentCrashFreeRate) || !defined(this.crashFreeTrend)) {
            return null;
        }
        return (<div>
        {this.crashFreeTrend >= 0 ? (<IconArrow direction="up" size="xs"/>) : (<IconArrow direction="down" size="xs"/>)}
        {formatAbbreviatedNumber(Math.abs(this.crashFreeTrend)) + "%"}
      </div>);
    };
    ProjectCard.prototype.render = function () {
        var _a, _b;
        var _c = this.props, organization = _c.organization, project = _c.project, hasProjectAccess = _c.hasProjectAccess;
        var stats = project.stats, slug = project.slug, transactionStats = project.transactionStats, sessionStats = project.sessionStats;
        var _d = sessionStats || {}, hasHealthData = _d.hasHealthData, currentCrashFreeRate = _d.currentCrashFreeRate;
        var totalErrors = (_a = stats === null || stats === void 0 ? void 0 : stats.reduce(function (sum, _a) {
            var _b = __read(_a, 2), _ = _b[0], value = _b[1];
            return sum + value;
        }, 0)) !== null && _a !== void 0 ? _a : 0;
        var totalTransactions = (_b = transactionStats === null || transactionStats === void 0 ? void 0 : transactionStats.reduce(function (sum, _a) {
            var _b = __read(_a, 2), _ = _b[0], value = _b[1];
            return sum + value;
        }, 0)) !== null && _b !== void 0 ? _b : 0;
        var zeroTransactions = totalTransactions === 0;
        var hasFirstEvent = Boolean(project.firstEvent || project.firstTransactionEvent);
        return (<div data-test-id={slug}>
        <StyledProjectCard>
          <CardHeader>
            <HeaderRow>
              <StyledIdBadge project={project} avatarSize={18} hideOverflow disableLink={!hasProjectAccess}/>
              <BookmarkStar organization={organization} project={project}/>
            </HeaderRow>
            <SummaryLinks>
              {stats ? (<Fragment>
                  <Link data-test-id="project-errors" to={"/organizations/" + organization.slug + "/issues/?project=" + project.id}>
                    {t('errors: %s', formatAbbreviatedNumber(totalErrors))}
                  </Link>
                  {this.hasPerformance && (<Fragment>
                      <em>|</em>
                      <TransactionsLink data-test-id="project-transactions" to={"/organizations/" + organization.slug + "/performance/?project=" + project.id}>
                        {t('transactions: %s', formatAbbreviatedNumber(totalTransactions))}
                        {zeroTransactions && (<QuestionTooltip title={t('Click here to learn more about performance monitoring')} position="top" size="xs"/>)}
                      </TransactionsLink>
                    </Fragment>)}
                </Fragment>) : (<SummaryLinkPlaceholder />)}
            </SummaryLinks>
          </CardHeader>
          <ChartContainer>
            {stats ? (<Chart firstEvent={hasFirstEvent} stats={stats} transactionStats={transactionStats}/>) : (<Placeholder height="150px"/>)}
          </ChartContainer>
          <FooterWrapper>
            <ScoreCardWrapper>
              {!stats ? (<Fragment>
                  <ReleaseTitle>{t('Crash Free Sessions')}</ReleaseTitle>
                  <FooterPlaceholder />
                </Fragment>) : hasHealthData ? (<ScoreCard title={t('Crash Free Sessions')} score={defined(currentCrashFreeRate)
                    ? displayCrashFreePercent(currentCrashFreeRate)
                    : '\u2014'} trend={this.renderTrend()} trendStatus={this.crashFreeTrend
                    ? this.crashFreeTrend > 0
                        ? 'good'
                        : 'bad'
                    : undefined}/>) : (this.renderMissingFeatureCard())}
            </ScoreCardWrapper>
            <DeploysWrapper>
              <ReleaseTitle>{t('Latest Deploys')}</ReleaseTitle>
              {stats ? <Deploys project={project} shorten/> : <FooterPlaceholder />}
            </DeploysWrapper>
          </FooterWrapper>
        </StyledProjectCard>
      </div>);
    };
    return ProjectCard;
}(Component));
var ProjectCardContainer = /** @class */ (function (_super) {
    __extends(ProjectCardContainer, _super);
    function ProjectCardContainer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.getInitialState();
        _this.listeners = [
            ProjectsStatsStore.listen(function (itemsBySlug) {
                _this.onProjectStoreUpdate(itemsBySlug);
            }, undefined),
        ];
        return _this;
    }
    ProjectCardContainer.prototype.getInitialState = function () {
        var project = this.props.project;
        var initialState = ProjectsStatsStore.getInitialState() || {};
        return {
            projectDetails: initialState[project.slug] || null,
        };
    };
    ProjectCardContainer.prototype.componentWillUnmount = function () {
        this.listeners.forEach(callIfFunction);
    };
    ProjectCardContainer.prototype.onProjectStoreUpdate = function (itemsBySlug) {
        var project = this.props.project;
        // Don't update state if we already have stats
        if (!itemsBySlug[project.slug]) {
            return;
        }
        if (itemsBySlug[project.slug] === this.state.projectDetails) {
            return;
        }
        this.setState({
            projectDetails: itemsBySlug[project.slug],
        });
    };
    ProjectCardContainer.prototype.render = function () {
        var _a = this.props, project = _a.project, props = __rest(_a, ["project"]);
        var projectDetails = this.state.projectDetails;
        return (<ProjectCard {...props} project={__assign(__assign({}, project), (projectDetails || {}))}/>);
    };
    return ProjectCardContainer;
}(Component));
var ChartContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: relative;\n  background: ", ";\n"], ["\n  position: relative;\n  background: ", ";\n"])), function (p) { return p.theme.backgroundSecondary; });
var CardHeader = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin: ", " ", ";\n"], ["\n  margin: ", " ", ";\n"])), space(1.5), space(2));
var HeaderRow = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr auto;\n  justify-content: space-between;\n  align-items: center;\n"], ["\n  display: grid;\n  grid-template-columns: 1fr auto;\n  justify-content: space-between;\n  align-items: center;\n"])));
var StyledProjectCard = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  background-color: ", ";\n  border: 1px solid ", ";\n  border-radius: ", ";\n  box-shadow: ", ";\n  min-height: 330px;\n"], ["\n  background-color: ", ";\n  border: 1px solid ", ";\n  border-radius: ", ";\n  box-shadow: ", ";\n  min-height: 330px;\n"])), function (p) { return p.theme.background; }, function (p) { return p.theme.border; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.dropShadowLight; });
var FooterWrapper = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr 1fr;\n  div {\n    border: none;\n    box-shadow: none;\n    font-size: ", ";\n    padding: 0;\n  }\n  ", " {\n    a {\n      background-color: ", ";\n      border: 1px solid ", ";\n      border-radius: ", ";\n      color: ", ";\n    }\n  }\n"], ["\n  display: grid;\n  grid-template-columns: 1fr 1fr;\n  div {\n    border: none;\n    box-shadow: none;\n    font-size: ", ";\n    padding: 0;\n  }\n  ", " {\n    a {\n      background-color: ", ";\n      border: 1px solid ", ";\n      border-radius: ", ";\n      color: ", ";\n    }\n  }\n"])), function (p) { return p.theme.fontSizeMedium; }, StyledButtonBar, function (p) { return p.theme.background; }, function (p) { return p.theme.border; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.gray500; });
var ScoreCardWrapper = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  margin: ", " 0 0 ", ";\n  ", " {\n    min-height: auto;\n  }\n  ", " {\n    color: ", ";\n    font-weight: 600;\n  }\n  ", " {\n    flex-direction: column;\n    align-items: flex-start;\n  }\n  ", " {\n    font-size: 28px;\n  }\n  ", " {\n    margin-left: 0;\n    margin-top: ", ";\n  }\n"], ["\n  margin: ", " 0 0 ", ";\n  ", " {\n    min-height: auto;\n  }\n  ", " {\n    color: ", ";\n    font-weight: 600;\n  }\n  ", " {\n    flex-direction: column;\n    align-items: flex-start;\n  }\n  ", " {\n    font-size: 28px;\n  }\n  ", " {\n    margin-left: 0;\n    margin-top: ", ";\n  }\n"])), space(2), space(2), StyledPanel, HeaderTitle, function (p) { return p.theme.gray300; }, ScoreWrapper, Score, Trend, space(0.5));
var DeploysWrapper = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  margin-top: ", ";\n  ", " {\n    display: block;\n    height: 100%;\n  }\n  ", " {\n    display: grid;\n    grid-template-columns: 1fr 1fr;\n    grid-column-gap: ", ";\n    div {\n      white-space: nowrap;\n      text-overflow: ellipsis;\n      overflow: hidden;\n    }\n    a {\n      display: grid;\n    }\n  }\n  ", " {\n    grid-template-columns: 2fr auto;\n    margin-right: ", ";\n    height: auto;\n    svg {\n      display: none;\n    }\n  }\n"], ["\n  margin-top: ", ";\n  ", " {\n    display: block;\n    height: 100%;\n  }\n  ", " {\n    display: grid;\n    grid-template-columns: 1fr 1fr;\n    grid-column-gap: ", ";\n    div {\n      white-space: nowrap;\n      text-overflow: ellipsis;\n      overflow: hidden;\n    }\n    a {\n      display: grid;\n    }\n  }\n  ", " {\n    grid-template-columns: 2fr auto;\n    margin-right: ", ";\n    height: auto;\n    svg {\n      display: none;\n    }\n  }\n"])), space(2), GetStarted, TextOverflow, space(1), DeployRows, space(2));
var ReleaseTitle = styled('span')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  color: ", ";\n  font-weight: 600;\n"], ["\n  color: ", ";\n  font-weight: 600;\n"])), function (p) { return p.theme.gray300; });
var StyledIdBadge = styled(IdBadge)(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  overflow: hidden;\n  white-space: nowrap;\n  flex-shrink: 1;\n"], ["\n  overflow: hidden;\n  white-space: nowrap;\n  flex-shrink: 1;\n"])));
var SummaryLinks = styled('div')(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n\n  color: ", ";\n  font-size: ", ";\n\n  /* Need to offset for the project icon and margin */\n  margin-left: 26px;\n\n  a {\n    color: ", ";\n    :hover {\n      color: ", ";\n    }\n  }\n  em {\n    font-style: normal;\n    margin: 0 ", ";\n  }\n"], ["\n  display: flex;\n  align-items: center;\n\n  color: ", ";\n  font-size: ", ";\n\n  /* Need to offset for the project icon and margin */\n  margin-left: 26px;\n\n  a {\n    color: ", ";\n    :hover {\n      color: ", ";\n    }\n  }\n  em {\n    font-style: normal;\n    margin: 0 ", ";\n  }\n"])), function (p) { return p.theme.subText; }, function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.formText; }, function (p) { return p.theme.subText; }, space(0.5));
var TransactionsLink = styled(Link)(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n\n  > span {\n    margin-left: ", ";\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n\n  > span {\n    margin-left: ", ";\n  }\n"])), space(0.5));
var NotAvailable = styled('div')(templateObject_12 || (templateObject_12 = __makeTemplateObject(["\n  font-size: ", ";\n  font-weight: normal;\n  display: grid;\n  grid-template-columns: auto auto;\n  grid-gap: ", ";\n  align-items: center;\n"], ["\n  font-size: ", ";\n  font-weight: normal;\n  display: grid;\n  grid-template-columns: auto auto;\n  grid-gap: ", ";\n  align-items: center;\n"])), function (p) { return p.theme.fontSizeMedium; }, space(0.5));
var SummaryLinkPlaceholder = styled(Placeholder)(templateObject_13 || (templateObject_13 = __makeTemplateObject(["\n  height: 15px;\n  width: 180px;\n  margin-top: ", ";\n  margin-bottom: ", ";\n"], ["\n  height: 15px;\n  width: 180px;\n  margin-top: ", ";\n  margin-bottom: ", ";\n"])), space(0.75), space(0.5));
var FooterPlaceholder = styled(Placeholder)(templateObject_14 || (templateObject_14 = __makeTemplateObject(["\n  height: 40px;\n  width: auto;\n  margin-right: ", ";\n"], ["\n  height: 40px;\n  width: auto;\n  margin-right: ", ";\n"])), space(2));
export { ProjectCard };
export default withOrganization(withApi(ProjectCardContainer));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13, templateObject_14;
//# sourceMappingURL=projectCard.jsx.map