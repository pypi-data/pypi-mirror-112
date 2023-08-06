import { __makeTemplateObject } from "tslib";
import styled from '@emotion/styled';
import classNames from 'classnames';
import DropdownMenu from 'app/components/dropdownMenu';
import { IconEllipsis } from 'app/icons';
var ContextMenu = function (_a) {
    var children = _a.children;
    return (<DropdownMenu>
    {function (_a) {
            var isOpen = _a.isOpen, getRootProps = _a.getRootProps, getActorProps = _a.getActorProps, getMenuProps = _a.getMenuProps;
            var topLevelCx = classNames('dropdown', {
                'anchor-right': true,
                open: isOpen,
            });
            return (<MoreOptions {...getRootProps({
                className: topLevelCx,
            })}>
          <DropdownTarget {...getActorProps({
                onClick: function (event) {
                    event.stopPropagation();
                    event.preventDefault();
                },
            })}>
            <IconEllipsis data-test-id="context-menu" size="md"/>
          </DropdownTarget>
          {isOpen && (<ul {...getMenuProps({})} className={classNames('dropdown-menu')}>
              {children}
            </ul>)}
        </MoreOptions>);
        }}
  </DropdownMenu>);
};
var MoreOptions = styled('span')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  color: ", ";\n"], ["\n  display: flex;\n  color: ", ";\n"])), function (p) { return p.theme.textColor; });
var DropdownTarget = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  cursor: pointer;\n  padding: 0 5px;\n"], ["\n  display: flex;\n  cursor: pointer;\n  padding: 0 5px;\n"])));
export default ContextMenu;
var templateObject_1, templateObject_2;
//# sourceMappingURL=contextMenu.jsx.map