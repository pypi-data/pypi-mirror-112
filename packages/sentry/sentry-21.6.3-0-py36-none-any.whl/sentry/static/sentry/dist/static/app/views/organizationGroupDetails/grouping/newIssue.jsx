import { __makeTemplateObject } from "tslib";
import { Fragment } from 'react';
import styled from '@emotion/styled';
import EventOrGroupHeader from 'app/components/eventOrGroupHeader';
import TimeSince from 'app/components/timeSince';
import { IconClock } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
function NewIssue(_a) {
    var sampleEvent = _a.sampleEvent, eventCount = _a.eventCount, organization = _a.organization;
    return (<Fragment>
      <EventDetails>
        <EventOrGroupHeader data={sampleEvent} organization={organization} hideIcons hideLevel/>
        <ExtraInfo>
          <TimeWrapper>
            <StyledIconClock size="11px"/>
            <TimeSince date={sampleEvent.dateCreated} suffix={t('old')}/>
          </TimeWrapper>
        </ExtraInfo>
      </EventDetails>
      <EventCount>{eventCount}</EventCount>
    </Fragment>);
}
export default NewIssue;
var EventDetails = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  overflow: hidden;\n  line-height: 1.1;\n"], ["\n  overflow: hidden;\n  line-height: 1.1;\n"])));
var ExtraInfo = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  justify-content: flex-start;\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  justify-content: flex-start;\n"])), space(2));
var TimeWrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: max-content 1fr;\n  align-items: center;\n  font-size: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: max-content 1fr;\n  align-items: center;\n  font-size: ", ";\n"])), space(0.5), function (p) { return p.theme.fontSizeSmall; });
var EventCount = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  align-items: center;\n  line-height: 1.1;\n"], ["\n  align-items: center;\n  line-height: 1.1;\n"])));
var StyledIconClock = styled(IconClock)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.subText; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=newIssue.jsx.map