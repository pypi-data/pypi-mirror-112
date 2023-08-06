import isEmpty from 'lodash/isEmpty';
import Pills from 'app/components/pills';
import { defined, generateQueryWithTag } from 'app/utils';
import EventTagsPill from './eventTagsPill';
var EventTags = function (_a) {
    var tags = _a.event.tags, organization = _a.organization, projectId = _a.projectId, location = _a.location, hasQueryFeature = _a.hasQueryFeature;
    if (isEmpty(tags)) {
        return null;
    }
    var orgSlug = organization.slug;
    var streamPath = "/organizations/" + orgSlug + "/issues/";
    var releasesPath = "/organizations/" + orgSlug + "/releases/";
    return (<Pills>
      {tags.map(function (tag, index) { return (<EventTagsPill key={!defined(tag.key) ? "tag-pill-" + index : tag.key} tag={tag} projectId={projectId} organization={organization} query={generateQueryWithTag(location.query, tag)} streamPath={streamPath} releasesPath={releasesPath} hasQueryFeature={hasQueryFeature}/>); })}
    </Pills>);
};
export default EventTags;
//# sourceMappingURL=eventTags.jsx.map