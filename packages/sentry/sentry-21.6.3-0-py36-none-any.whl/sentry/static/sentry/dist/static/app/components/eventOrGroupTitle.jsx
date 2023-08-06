import { __extends, __makeTemplateObject } from "tslib";
import * as React from 'react';
import styled from '@emotion/styled';
import GuideAnchor from 'app/components/assistant/guideAnchor';
import ProjectsStore from 'app/stores/projectsStore';
import { getTitle } from 'app/utils/events';
import withOrganization from 'app/utils/withOrganization';
import StacktracePreview from './stacktracePreview';
var EventOrGroupTitle = /** @class */ (function (_super) {
    __extends(EventOrGroupTitle, _super);
    function EventOrGroupTitle() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    EventOrGroupTitle.prototype.render = function () {
        var _a;
        var _b = this.props, hasGuideAnchor = _b.hasGuideAnchor, data = _b.data, organization = _b.organization, withStackTracePreview = _b.withStackTracePreview, guideAnchorName = _b.guideAnchorName;
        var _c = getTitle(data, organization), title = _c.title, subtitle = _c.subtitle;
        var _d = data, id = _d.id, eventID = _d.eventID, groupID = _d.groupID, projectID = _d.projectID;
        var titleWithHoverStacktrace = (<StacktracePreview organization={organization} issueId={groupID ? groupID : id} 
        // we need eventId and projectSlug only when hovering over Event, not Group
        // (different API call is made to get the stack trace then)
        eventId={eventID} projectSlug={eventID ? (_a = ProjectsStore.getById(projectID)) === null || _a === void 0 ? void 0 : _a.slug : undefined} disablePreview={!withStackTracePreview}>
        {title}
      </StacktracePreview>);
        return subtitle ? (<span style={this.props.style}>
        <GuideAnchor disabled={!hasGuideAnchor} target={guideAnchorName} position="bottom">
          <span>{titleWithHoverStacktrace}</span>
        </GuideAnchor>
        <Spacer />
        <Subtitle title={subtitle}>{subtitle}</Subtitle>
        <br />
      </span>) : (<span style={this.props.style}>
        <GuideAnchor disabled={!hasGuideAnchor} target={guideAnchorName} position="bottom">
          {titleWithHoverStacktrace}
        </GuideAnchor>
      </span>);
    };
    EventOrGroupTitle.defaultProps = {
        guideAnchorName: 'issue_title',
    };
    return EventOrGroupTitle;
}(React.Component));
export default withOrganization(EventOrGroupTitle);
/**
 * &nbsp; is used instead of margin/padding to split title and subtitle
 * into 2 separate text nodes on the HTML AST. This allows the
 * title to be highlighted without spilling over to the subtitle.
 */
var Spacer = function () { return <span style={{ display: 'inline-block', width: 10 }}>&nbsp;</span>; };
var Subtitle = styled('em')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  color: ", ";\n  font-style: normal;\n"], ["\n  color: ", ";\n  font-style: normal;\n"])), function (p) { return p.theme.gray300; });
var templateObject_1;
//# sourceMappingURL=eventOrGroupTitle.jsx.map