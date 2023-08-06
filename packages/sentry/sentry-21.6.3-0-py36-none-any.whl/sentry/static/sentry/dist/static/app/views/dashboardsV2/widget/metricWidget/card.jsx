import { __makeTemplateObject } from "tslib";
import styled from '@emotion/styled';
import { HeaderTitle } from 'app/components/charts/styles';
import ErrorBoundary from 'app/components/errorBoundary';
import { Panel } from 'app/components/panels';
import Placeholder from 'app/components/placeholder';
import { t } from 'app/locale';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import Chart from './chart';
import StatsRequest from './statsRequest';
function Card(_a) {
    var widget = _a.widget, api = _a.api, location = _a.location, router = _a.router, organization = _a.organization, project = _a.project, selection = _a.selection;
    var groupings = widget.groupings, searchQuery = widget.searchQuery, title = widget.title, displayType = widget.displayType;
    return (<ErrorBoundary customComponent={<ErrorCard>{t('Error loading widget data')}</ErrorCard>}>
      <StyledPanel>
        <Title>{title}</Title>
        <StatsRequest api={api} location={location} organization={organization} projectSlug={project.slug} groupings={groupings} searchQuery={searchQuery} environments={selection.environments} datetime={selection.datetime}>
          {function (_a) {
            var isLoading = _a.isLoading, errored = _a.errored, series = _a.series;
            return (<Chart displayType={displayType} series={series} isLoading={isLoading} errored={errored} location={location} platform={project.platform} selection={selection} router={router}/>);
        }}
        </StatsRequest>
      </StyledPanel>
    </ErrorBoundary>);
}
export default Card;
var StyledPanel = styled(Panel)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin: 0;\n  /* If a panel overflows due to a long title stretch its grid sibling */\n  height: 100%;\n  min-height: 96px;\n  padding: ", " ", ";\n"], ["\n  margin: 0;\n  /* If a panel overflows due to a long title stretch its grid sibling */\n  height: 100%;\n  min-height: 96px;\n  padding: ", " ", ";\n"])), space(2), space(3));
var ErrorCard = styled(Placeholder)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  background-color: ", ";\n  border: 1px solid ", ";\n  color: ", ";\n  border-radius: ", ";\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  background-color: ", ";\n  border: 1px solid ", ";\n  color: ", ";\n  border-radius: ", ";\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.alert.error.backgroundLight; }, function (p) { return p.theme.alert.error.border; }, function (p) { return p.theme.alert.error.textLight; }, function (p) { return p.theme.borderRadius; }, space(2));
var Title = styled(HeaderTitle)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), overflowEllipsis);
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=card.jsx.map