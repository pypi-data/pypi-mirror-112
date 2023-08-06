import { __makeTemplateObject } from "tslib";
import { Link, withRouter } from 'react-router';
import styled from '@emotion/styled';
import GuideAnchor from 'app/components/assistant/guideAnchor';
import EventAnnotation from 'app/components/events/eventAnnotation';
import InboxReason from 'app/components/group/inboxBadges/inboxReason';
import InboxShortId from 'app/components/group/inboxBadges/shortId';
import TimesTag from 'app/components/group/inboxBadges/timesTag';
import UnhandledTag from 'app/components/group/inboxBadges/unhandledTag';
import ProjectBadge from 'app/components/idBadge/projectBadge';
import Placeholder from 'app/components/placeholder';
import { IconChat } from 'app/icons';
import { tct } from 'app/locale';
import space from 'app/styles/space';
function EventOrGroupExtraDetails(_a) {
    var data = _a.data, showAssignee = _a.showAssignee, params = _a.params, hasGuideAnchor = _a.hasGuideAnchor, showInboxTime = _a.showInboxTime;
    var _b = data, id = _b.id, lastSeen = _b.lastSeen, firstSeen = _b.firstSeen, subscriptionDetails = _b.subscriptionDetails, numComments = _b.numComments, logger = _b.logger, assignedTo = _b.assignedTo, annotations = _b.annotations, shortId = _b.shortId, project = _b.project, lifetime = _b.lifetime, isUnhandled = _b.isUnhandled, inbox = _b.inbox;
    var issuesPath = "/organizations/" + params.orgId + "/issues/";
    var inboxReason = inbox && (<InboxReason inbox={inbox} showDateAdded={showInboxTime}/>);
    return (<GroupExtra>
      {inbox && (<GuideAnchor target="inbox_guide_reason" disabled={!hasGuideAnchor}>
          {inboxReason}
        </GuideAnchor>)}
      {shortId && (<InboxShortId shortId={shortId} avatar={project && (<ShadowlessProjectBadge project={project} avatarSize={12} hideName/>)}/>)}
      {isUnhandled && <UnhandledTag />}
      {!lifetime && !firstSeen && !lastSeen ? (<Placeholder height="14px" width="100px"/>) : (<TimesTag lastSeen={(lifetime === null || lifetime === void 0 ? void 0 : lifetime.lastSeen) || lastSeen} firstSeen={(lifetime === null || lifetime === void 0 ? void 0 : lifetime.firstSeen) || firstSeen}/>)}
      {/* Always display comment count on inbox */}
      {numComments > 0 && (<CommentsLink to={"" + issuesPath + id + "/activity/"} className="comments">
          <IconChat size="xs" color={(subscriptionDetails === null || subscriptionDetails === void 0 ? void 0 : subscriptionDetails.reason) === 'mentioned' ? 'green300' : undefined}/>
          <span>{numComments}</span>
        </CommentsLink>)}
      {logger && (<LoggerAnnotation>
          <Link to={{
                pathname: issuesPath,
                query: {
                    query: "logger:" + logger,
                },
            }}>
            {logger}
          </Link>
        </LoggerAnnotation>)}
      {annotations === null || annotations === void 0 ? void 0 : annotations.map(function (annotation, key) { return (<AnnotationNoMargin dangerouslySetInnerHTML={{
                __html: annotation,
            }} key={key}/>); })}

      {showAssignee && assignedTo && (<div>{tct('Assigned to [name]', { name: assignedTo.name })}</div>)}
    </GroupExtra>);
}
var GroupExtra = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: inline-grid;\n  grid-auto-flow: column dense;\n  grid-gap: ", ";\n  justify-content: start;\n  align-items: center;\n  color: ", ";\n  font-size: ", ";\n  position: relative;\n  min-width: 500px;\n  white-space: nowrap;\n\n  a {\n    color: inherit;\n  }\n"], ["\n  display: inline-grid;\n  grid-auto-flow: column dense;\n  grid-gap: ", ";\n  justify-content: start;\n  align-items: center;\n  color: ", ";\n  font-size: ", ";\n  position: relative;\n  min-width: 500px;\n  white-space: nowrap;\n\n  a {\n    color: inherit;\n  }\n"])), space(1.5), function (p) { return p.theme.textColor; }, function (p) { return p.theme.fontSizeSmall; });
var ShadowlessProjectBadge = styled(ProjectBadge)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  * > img {\n    box-shadow: none;\n  }\n"], ["\n  * > img {\n    box-shadow: none;\n  }\n"])));
var CommentsLink = styled(Link)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: inline-grid;\n  grid-gap: ", ";\n  align-items: center;\n  grid-auto-flow: column;\n  color: ", ";\n"], ["\n  display: inline-grid;\n  grid-gap: ", ";\n  align-items: center;\n  grid-auto-flow: column;\n  color: ", ";\n"])), space(0.5), function (p) { return p.theme.textColor; });
var AnnotationNoMargin = styled(EventAnnotation)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin-left: 0;\n  padding-left: 0;\n  border-left: none;\n  & > a {\n    color: ", ";\n  }\n"], ["\n  margin-left: 0;\n  padding-left: 0;\n  border-left: none;\n  & > a {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.textColor; });
var LoggerAnnotation = styled(AnnotationNoMargin)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.textColor; });
export default withRouter(EventOrGroupExtraDetails);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=eventOrGroupExtraDetails.jsx.map