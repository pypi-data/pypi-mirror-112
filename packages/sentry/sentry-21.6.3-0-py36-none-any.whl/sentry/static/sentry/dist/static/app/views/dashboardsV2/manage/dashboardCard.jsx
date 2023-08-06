import { __makeTemplateObject } from "tslib";
import * as React from 'react';
import styled from '@emotion/styled';
import ActivityAvatar from 'app/components/activity/item/avatar';
import Card from 'app/components/card';
import Link from 'app/components/links/link';
import { t } from 'app/locale';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
function DashboardCard(_a) {
    var title = _a.title, detail = _a.detail, createdBy = _a.createdBy, renderWidgets = _a.renderWidgets, dateStatus = _a.dateStatus, to = _a.to, onEventClick = _a.onEventClick, renderContextMenu = _a.renderContextMenu;
    function onClick() {
        onEventClick === null || onEventClick === void 0 ? void 0 : onEventClick();
    }
    return (<Link data-test-id={"card-" + title} onClick={onClick} to={to}>
      <StyledDashboardCard interactive>
        <CardHeader>
          <CardContent>
            <Title>{title}</Title>
            <Detail>{detail}</Detail>
          </CardContent>
          <AvatarWrapper>
            {createdBy ? (<ActivityAvatar type="user" user={createdBy} size={34}/>) : (<ActivityAvatar type="system" size={34}/>)}
          </AvatarWrapper>
        </CardHeader>
        <CardBody>{renderWidgets()}</CardBody>
        <CardFooter>
          <DateSelected>
            {dateStatus ? (<DateStatus>
                {t('Created')} {dateStatus}
              </DateStatus>) : (<DateStatus />)}
          </DateSelected>
          {renderContextMenu && renderContextMenu()}
        </CardFooter>
      </StyledDashboardCard>
    </Link>);
}
var AvatarWrapper = styled('span')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  border: 3px solid ", ";\n  border-radius: 50%;\n  height: min-content;\n"], ["\n  border: 3px solid ", ";\n  border-radius: 50%;\n  height: min-content;\n"])), function (p) { return p.theme.border; });
var CardContent = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  flex-grow: 1;\n  overflow: hidden;\n  margin-right: ", ";\n"], ["\n  flex-grow: 1;\n  overflow: hidden;\n  margin-right: ", ";\n"])), space(1));
var StyledDashboardCard = styled(Card)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  justify-content: space-between;\n  height: 100%;\n  &:focus,\n  &:hover {\n    top: -1px;\n  }\n"], ["\n  justify-content: space-between;\n  height: 100%;\n  &:focus,\n  &:hover {\n    top: -1px;\n  }\n"])));
var CardHeader = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n  padding: ", " ", ";\n"], ["\n  display: flex;\n  padding: ", " ", ";\n"])), space(1.5), space(2));
var Title = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  color: ", ";\n  ", ";\n"], ["\n  color: ", ";\n  ", ";\n"])), function (p) { return p.theme.textColor; }, overflowEllipsis);
var Detail = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  font-family: ", ";\n  font-size: ", ";\n  color: ", ";\n  ", ";\n  line-height: 1.5;\n"], ["\n  font-family: ", ";\n  font-size: ", ";\n  color: ", ";\n  ", ";\n  line-height: 1.5;\n"])), function (p) { return p.theme.text.familyMono; }, function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.gray300; }, overflowEllipsis);
var CardBody = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  background: ", ";\n  padding: ", " ", ";\n  max-height: 150px;\n  min-height: 150px;\n  overflow: hidden;\n"], ["\n  background: ", ";\n  padding: ", " ", ";\n  max-height: 150px;\n  min-height: 150px;\n  overflow: hidden;\n"])), function (p) { return p.theme.gray100; }, space(1.5), space(2));
var CardFooter = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n  padding: ", " ", ";\n"], ["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n  padding: ", " ", ";\n"])), space(1), space(2));
var DateSelected = styled('div')(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  font-size: ", ";\n  display: grid;\n  grid-column-gap: ", ";\n  color: ", ";\n  ", ";\n"], ["\n  font-size: ", ";\n  display: grid;\n  grid-column-gap: ", ";\n  color: ", ";\n  ", ";\n"])), function (p) { return p.theme.fontSizeSmall; }, space(1), function (p) { return p.theme.textColor; }, overflowEllipsis);
var DateStatus = styled('span')(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  color: ", ";\n  padding-left: ", ";\n"], ["\n  color: ", ";\n  padding-left: ", ";\n"])), function (p) { return p.theme.purple300; }, space(1));
export default DashboardCard;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10;
//# sourceMappingURL=dashboardCard.jsx.map