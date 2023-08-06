import { __extends, __makeTemplateObject, __values } from "tslib";
import { Component, Fragment } from 'react';
import ReactDOM from 'react-dom';
import { Manager, Popper, Reference } from 'react-popper';
import styled from '@emotion/styled';
import MenuHeader from 'app/components/actions/menuHeader';
import CheckboxFancy from 'app/components/checkboxFancy/checkboxFancy';
import MenuItem from 'app/components/menuItem';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { defined } from 'app/utils';
import { MAX_TEAM_KEY_TRANSACTIONS } from 'app/utils/performance/constants';
var TeamKeyTransaction = /** @class */ (function (_super) {
    __extends(TeamKeyTransaction, _super);
    function TeamKeyTransaction(props) {
        var _this = _super.call(this, props) || this;
        _this.state = {
            isOpen: false,
        };
        _this.handleClickOutside = function (event) {
            if (!_this.menuEl) {
                return;
            }
            if (!(event.target instanceof Element)) {
                return;
            }
            if (_this.menuEl.contains(event.target)) {
                return;
            }
            _this.setState({ isOpen: false });
        };
        _this.toggleOpen = function () {
            _this.setState(function (_a) {
                var isOpen = _a.isOpen;
                return ({ isOpen: !isOpen });
            });
        };
        _this.toggleSelection = function (enabled, selection) { return function () {
            var handleToggleKeyTransaction = _this.props.handleToggleKeyTransaction;
            return enabled ? handleToggleKeyTransaction(selection) : undefined;
        }; };
        var portal = document.getElementById('team-key-transaction-portal');
        if (!portal) {
            portal = document.createElement('div');
            portal.setAttribute('id', 'team-key-transaction-portal');
            document.body.appendChild(portal);
        }
        _this.portalEl = portal;
        _this.menuEl = null;
        return _this;
    }
    TeamKeyTransaction.prototype.componentDidUpdate = function (_props, prevState) {
        if (this.state.isOpen && prevState.isOpen === false) {
            document.addEventListener('click', this.handleClickOutside, true);
        }
        if (this.state.isOpen === false && prevState.isOpen) {
            document.removeEventListener('click', this.handleClickOutside, true);
        }
    };
    TeamKeyTransaction.prototype.componentWillUnmount = function () {
        document.removeEventListener('click', this.handleClickOutside, true);
        this.portalEl.remove();
    };
    TeamKeyTransaction.prototype.partitionTeams = function (counts, keyedTeams) {
        var e_1, _a;
        var _b;
        var _c = this.props, teams = _c.teams, project = _c.project;
        var enabledTeams = [];
        var disabledTeams = [];
        var noAccessTeams = [];
        var projectTeams = new Set(project.teams.map(function (_a) {
            var id = _a.id;
            return id;
        }));
        try {
            for (var teams_1 = __values(teams), teams_1_1 = teams_1.next(); !teams_1_1.done; teams_1_1 = teams_1.next()) {
                var team = teams_1_1.value;
                if (!projectTeams.has(team.id)) {
                    noAccessTeams.push(team);
                }
                else if (keyedTeams.has(team.id) ||
                    ((_b = counts.get(team.id)) !== null && _b !== void 0 ? _b : 0) < MAX_TEAM_KEY_TRANSACTIONS) {
                    enabledTeams.push(team);
                }
                else {
                    disabledTeams.push(team);
                }
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (teams_1_1 && !teams_1_1.done && (_a = teams_1.return)) _a.call(teams_1);
            }
            finally { if (e_1) throw e_1.error; }
        }
        return {
            enabledTeams: enabledTeams,
            disabledTeams: disabledTeams,
            noAccessTeams: noAccessTeams,
        };
    };
    TeamKeyTransaction.prototype.renderMenuContent = function (counts, keyedTeams) {
        var _this = this;
        var _a = this.props, teams = _a.teams, project = _a.project, transactionName = _a.transactionName;
        var _b = this.partitionTeams(counts, keyedTeams), enabledTeams = _b.enabledTeams, disabledTeams = _b.disabledTeams, noAccessTeams = _b.noAccessTeams;
        var isMyTeamsEnabled = enabledTeams.length > 0;
        var myTeamsHandler = this.toggleSelection(isMyTeamsEnabled, {
            action: enabledTeams.length === keyedTeams.size ? 'unkey' : 'key',
            teamIds: enabledTeams.map(function (_a) {
                var id = _a.id;
                return id;
            }),
            project: project,
            transactionName: transactionName,
        });
        var hasTeamsWithAccess = enabledTeams.length + disabledTeams.length > 0;
        return (<DropdownContent>
        {hasTeamsWithAccess && (<Fragment>
            <DropdownMenuHeader first>
              {t('My Teams with Access')}
              <ActionItem>
                <CheckboxFancy isDisabled={!isMyTeamsEnabled} isChecked={teams.length === keyedTeams.size} isIndeterminate={teams.length > keyedTeams.size && keyedTeams.size > 0} onClick={myTeamsHandler}/>
              </ActionItem>
            </DropdownMenuHeader>
            {enabledTeams.map(function (team) { return (<TeamKeyTransactionItem key={team.slug} team={team} isKeyed={keyedTeams.has(team.id)} disabled={false} onSelect={_this.toggleSelection(true, {
                        action: keyedTeams.has(team.id) ? 'unkey' : 'key',
                        teamIds: [team.id],
                        project: project,
                        transactionName: transactionName,
                    })}/>); })}
            {disabledTeams.map(function (team) { return (<TeamKeyTransactionItem key={team.slug} team={team} isKeyed={keyedTeams.has(team.id)} disabled onSelect={_this.toggleSelection(true, {
                        action: keyedTeams.has(team.id) ? 'unkey' : 'key',
                        teamIds: [team.id],
                        project: project,
                        transactionName: transactionName,
                    })}/>); })}
          </Fragment>)}
        {noAccessTeams.length > 0 && (<Fragment>
            <DropdownMenuHeader first={!hasTeamsWithAccess}>
              {t('My Teams without Access')}
            </DropdownMenuHeader>
            {noAccessTeams.map(function (team) { return (<TeamKeyTransactionItem key={team.slug} team={team} disabled/>); })}
          </Fragment>)}
      </DropdownContent>);
    };
    TeamKeyTransaction.prototype.renderMenu = function () {
        var _this = this;
        var _a = this.props, isLoading = _a.isLoading, counts = _a.counts, keyedTeams = _a.keyedTeams;
        if (isLoading || !defined(counts) || !defined(keyedTeams)) {
            return null;
        }
        var modifiers = {
            hide: {
                enabled: false,
            },
            preventOverflow: {
                padding: 10,
                enabled: true,
                boundariesElement: 'viewport',
            },
        };
        return ReactDOM.createPortal(<Popper placement="top" modifiers={modifiers}>
        {function (_a) {
                var popperRef = _a.ref, style = _a.style, placement = _a.placement;
                return (<DropdownWrapper ref={function (ref) {
                        popperRef(ref);
                        _this.menuEl = ref;
                    }} style={style} data-placement={placement}>
            {_this.renderMenuContent(counts, keyedTeams)}
          </DropdownWrapper>);
            }}
      </Popper>, this.portalEl);
    };
    TeamKeyTransaction.prototype.render = function () {
        var _this = this;
        var _a = this.props, isLoading = _a.isLoading, error = _a.error, Title = _a.title, keyedTeams = _a.keyedTeams, initialValue = _a.initialValue, teams = _a.teams;
        var isOpen = this.state.isOpen;
        var menu = isOpen ? this.renderMenu() : null;
        return (<Manager>
        <Reference>
          {function (_a) {
                var ref = _a.ref;
                return (<div ref={ref}>
              <Title isOpen={isOpen} disabled={isLoading || Boolean(error)} keyedTeams={keyedTeams ? teams.filter(function (_a) {
                        var id = _a.id;
                        return keyedTeams.has(id);
                    }) : null} initialValue={initialValue} onClick={_this.toggleOpen}/>
            </div>);
            }}
        </Reference>
        {menu}
      </Manager>);
    };
    return TeamKeyTransaction;
}(Component));
function TeamKeyTransactionItem(_a) {
    var team = _a.team, isKeyed = _a.isKeyed, disabled = _a.disabled, onSelect = _a.onSelect;
    return (<DropdownMenuItem key={team.slug} disabled={disabled} onSelect={onSelect} stopPropagation>
      <MenuItemContent>
        {team.slug}
        <ActionItem>
          {!defined(isKeyed) ? null : disabled ? (t('Max %s', MAX_TEAM_KEY_TRANSACTIONS)) : (<CheckboxFancy isChecked={isKeyed}/>)}
        </ActionItem>
      </MenuItemContent>
    </DropdownMenuItem>);
}
var DropdownWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  /* Adapted from the dropdown-menu class */\n  border: none;\n  border-radius: 2px;\n  box-shadow: 0 0 0 1px rgba(52, 60, 69, 0.2), 0 1px 3px rgba(70, 82, 98, 0.25);\n  background-clip: padding-box;\n  background-color: ", ";\n  width: 220px;\n  overflow: visible;\n  z-index: ", ";\n\n  &:before,\n  &:after {\n    width: 0;\n    height: 0;\n    content: '';\n    display: block;\n    position: absolute;\n    right: auto;\n  }\n\n  &:before {\n    border-left: 9px solid transparent;\n    border-right: 9px solid transparent;\n    left: calc(50% - 9px);\n    z-index: -2;\n  }\n\n  &:after {\n    border-left: 8px solid transparent;\n    border-right: 8px solid transparent;\n    left: calc(50% - 8px);\n    z-index: -1;\n  }\n\n  &[data-placement*='bottom'] {\n    margin-top: 9px;\n\n    &:before {\n      border-bottom: 9px solid ", ";\n      top: -9px;\n    }\n\n    &:after {\n      border-bottom: 8px solid ", ";\n      top: -8px;\n    }\n  }\n\n  &[data-placement*='top'] {\n    margin-bottom: 9px;\n\n    &:before {\n      border-top: 9px solid ", ";\n      bottom: -9px;\n    }\n\n    &:after {\n      border-top: 8px solid ", ";\n      bottom: -8px;\n    }\n  }\n"], ["\n  /* Adapted from the dropdown-menu class */\n  border: none;\n  border-radius: 2px;\n  box-shadow: 0 0 0 1px rgba(52, 60, 69, 0.2), 0 1px 3px rgba(70, 82, 98, 0.25);\n  background-clip: padding-box;\n  background-color: ", ";\n  width: 220px;\n  overflow: visible;\n  z-index: ", ";\n\n  &:before,\n  &:after {\n    width: 0;\n    height: 0;\n    content: '';\n    display: block;\n    position: absolute;\n    right: auto;\n  }\n\n  &:before {\n    border-left: 9px solid transparent;\n    border-right: 9px solid transparent;\n    left: calc(50% - 9px);\n    z-index: -2;\n  }\n\n  &:after {\n    border-left: 8px solid transparent;\n    border-right: 8px solid transparent;\n    left: calc(50% - 8px);\n    z-index: -1;\n  }\n\n  &[data-placement*='bottom'] {\n    margin-top: 9px;\n\n    &:before {\n      border-bottom: 9px solid ", ";\n      top: -9px;\n    }\n\n    &:after {\n      border-bottom: 8px solid ", ";\n      top: -8px;\n    }\n  }\n\n  &[data-placement*='top'] {\n    margin-bottom: 9px;\n\n    &:before {\n      border-top: 9px solid ", ";\n      bottom: -9px;\n    }\n\n    &:after {\n      border-top: 8px solid ", ";\n      bottom: -8px;\n    }\n  }\n"])), function (p) { return p.theme.background; }, function (p) { return p.theme.zIndex.tooltip; }, function (p) { return p.theme.border; }, function (p) { return p.theme.background; }, function (p) { return p.theme.border; }, function (p) { return p.theme.background; });
var DropdownContent = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  max-height: 250px;\n  overflow-y: auto;\n"], ["\n  max-height: 250px;\n  overflow-y: auto;\n"])));
var DropdownMenuHeader = styled(MenuHeader)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: row;\n  justify-content: space-between;\n  align-items: center;\n  padding: ", " ", ";\n\n  background: ", ";\n  ", ";\n"], ["\n  display: flex;\n  flex-direction: row;\n  justify-content: space-between;\n  align-items: center;\n  padding: ", " ", ";\n\n  background: ", ";\n  ", ";\n"])), space(1), space(2), function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.first && 'border-radius: 2px'; });
var DropdownMenuItem = styled(MenuItem)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  font-size: ", ";\n\n  &:not(:last-child) {\n    border-bottom: 1px solid ", ";\n  }\n"], ["\n  font-size: ", ";\n\n  &:not(:last-child) {\n    border-bottom: 1px solid ", ";\n  }\n"])), function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.innerBorder; });
var MenuItemContent = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: row;\n  justify-content: space-between;\n  align-items: center;\n  width: 100%;\n"], ["\n  display: flex;\n  flex-direction: row;\n  justify-content: space-between;\n  align-items: center;\n  width: 100%;\n"])));
var ActionItem = styled('span')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  min-width: ", ";\n  margin-left: ", ";\n"], ["\n  min-width: ", ";\n  margin-left: ", ";\n"])), space(2), space(1));
export default TeamKeyTransaction;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=teamKeyTransaction.jsx.map