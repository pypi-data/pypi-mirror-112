import { __extends, __makeTemplateObject } from "tslib";
import { Component } from 'react';
import styled from '@emotion/styled';
import ProjectBadge from 'app/components/idBadge/projectBadge';
import BookmarkStar from 'app/components/projects/bookmarkStar';
import space from 'app/styles/space';
var ProjectItem = /** @class */ (function (_super) {
    __extends(ProjectItem, _super);
    function ProjectItem() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isBookmarked: _this.props.project.isBookmarked,
        };
        _this.handleToggleBookmark = function (isBookmarked) {
            _this.setState({ isBookmarked: isBookmarked });
        };
        return _this;
    }
    ProjectItem.prototype.render = function () {
        var _a = this.props, project = _a.project, organization = _a.organization;
        return (<Wrapper>
        <BookmarkLink organization={organization} project={project} isBookmarked={this.state.isBookmarked} onToggle={this.handleToggleBookmark}/>
        <ProjectBadge to={"/settings/" + organization.slug + "/projects/" + project.slug + "/"} avatarSize={18} project={project}/>
      </Wrapper>);
    };
    return ProjectItem;
}(Component));
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var BookmarkLink = styled(BookmarkStar)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-right: ", ";\n  margin-top: -", ";\n"], ["\n  margin-right: ", ";\n  margin-top: -", ";\n"])), space(1), space(0.25));
export default ProjectItem;
var templateObject_1, templateObject_2;
//# sourceMappingURL=settingsProjectItem.jsx.map