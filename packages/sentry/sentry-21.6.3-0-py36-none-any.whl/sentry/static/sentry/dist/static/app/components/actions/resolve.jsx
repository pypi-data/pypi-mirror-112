import { __extends } from "tslib";
import * as React from 'react';
import { openModal } from 'app/actionCreators/modal';
import ActionLink from 'app/components/actions/actionLink';
import ButtonBar from 'app/components/buttonBar';
import CustomResolutionModal from 'app/components/customResolutionModal';
import DropdownLink from 'app/components/dropdownLink';
import Tooltip from 'app/components/tooltip';
import { IconCheckmark, IconChevron } from 'app/icons';
import { t } from 'app/locale';
import { ResolutionStatus, } from 'app/types';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import { formatVersion } from 'app/utils/formatters';
import withOrganization from 'app/utils/withOrganization';
import ActionButton from './button';
import MenuHeader from './menuHeader';
import MenuItemActionLink from './menuItemActionLink';
var defaultProps = {
    isResolved: false,
    isAutoResolved: false,
    confirmLabel: t('Resolve'),
    hasInbox: false,
};
var ResolveActions = /** @class */ (function (_super) {
    __extends(ResolveActions, _super);
    function ResolveActions() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleCurrentReleaseResolution = function () {
            var _a = _this.props, onUpdate = _a.onUpdate, organization = _a.organization, hasRelease = _a.hasRelease, latestRelease = _a.latestRelease;
            hasRelease &&
                onUpdate({
                    status: ResolutionStatus.RESOLVED,
                    statusDetails: {
                        inRelease: latestRelease ? latestRelease.version : 'latest',
                    },
                });
            trackAnalyticsEvent({
                eventKey: 'resolve_issue',
                eventName: 'Resolve Issue',
                release: 'current',
                organization_id: organization.id,
            });
        };
        _this.handleNextReleaseResolution = function () {
            var _a = _this.props, onUpdate = _a.onUpdate, organization = _a.organization, hasRelease = _a.hasRelease;
            hasRelease &&
                onUpdate({
                    status: ResolutionStatus.RESOLVED,
                    statusDetails: {
                        inNextRelease: true,
                    },
                });
            trackAnalyticsEvent({
                eventKey: 'resolve_issue',
                eventName: 'Resolve Issue',
                release: 'next',
                organization_id: organization.id,
            });
        };
        return _this;
    }
    ResolveActions.prototype.handleAnotherExistingReleaseResolution = function (statusDetails) {
        var _a = this.props, organization = _a.organization, onUpdate = _a.onUpdate;
        onUpdate({
            status: ResolutionStatus.RESOLVED,
            statusDetails: statusDetails,
        });
        trackAnalyticsEvent({
            eventKey: 'resolve_issue',
            eventName: 'Resolve Issue',
            release: 'anotherExisting',
            organization_id: organization.id,
        });
    };
    ResolveActions.prototype.renderResolved = function () {
        var _a = this.props, isAutoResolved = _a.isAutoResolved, onUpdate = _a.onUpdate;
        return (<Tooltip title={isAutoResolved
                ? t('This event is resolved due to the Auto Resolve configuration for this project')
                : t('Unresolve')}>
        <ActionButton priority="primary" icon={<IconCheckmark size="xs"/>} label={t('Unresolve')} disabled={isAutoResolved} onClick={function () { return onUpdate({ status: ResolutionStatus.UNRESOLVED }); }}/>
      </Tooltip>);
    };
    ResolveActions.prototype.renderDropdownMenu = function () {
        var _this = this;
        var _a = this.props, projectSlug = _a.projectSlug, isResolved = _a.isResolved, hasRelease = _a.hasRelease, latestRelease = _a.latestRelease, confirmMessage = _a.confirmMessage, shouldConfirm = _a.shouldConfirm, disabled = _a.disabled, confirmLabel = _a.confirmLabel, disableDropdown = _a.disableDropdown, hasInbox = _a.hasInbox;
        if (isResolved) {
            return this.renderResolved();
        }
        var actionTitle = !hasRelease
            ? t('Set up release tracking in order to use this feature.')
            : '';
        var actionLinkProps = {
            shouldConfirm: shouldConfirm,
            message: confirmMessage,
            confirmLabel: confirmLabel,
            disabled: disabled || !hasRelease,
        };
        return (<DropdownLink customTitle={!hasInbox && (<ActionButton label={t('More resolve options')} disabled={!projectSlug ? disabled : disableDropdown} icon={<IconChevron direction="down" size="xs"/>}/>)} caret={false} title={hasInbox && t('Resolve In\u2026')} alwaysRenderMenu disabled={!projectSlug ? disabled : disableDropdown} anchorRight={hasInbox} isNestedDropdown={hasInbox}>
        <MenuHeader>{t('Resolved In')}</MenuHeader>

        <MenuItemActionLink {...actionLinkProps} title={t('The next release')} onAction={this.handleNextReleaseResolution}>
          <Tooltip disabled={hasRelease} title={actionTitle}>
            {t('The next release')}
          </Tooltip>
        </MenuItemActionLink>

        <MenuItemActionLink {...actionLinkProps} title={t('The current release')} onAction={this.handleCurrentReleaseResolution}>
          <Tooltip disabled={hasRelease} title={actionTitle}>
            {latestRelease
                ? t('The current release (%s)', formatVersion(latestRelease.version))
                : t('The current release')}
          </Tooltip>
        </MenuItemActionLink>

        <MenuItemActionLink {...actionLinkProps} title={t('Another existing release')} onAction={function () { return hasRelease && _this.openCustomReleaseModal(); }} shouldConfirm={false}>
          <Tooltip disabled={hasRelease} title={actionTitle}>
            {t('Another existing release')}
          </Tooltip>
        </MenuItemActionLink>
      </DropdownLink>);
    };
    ResolveActions.prototype.openCustomReleaseModal = function () {
        var _this = this;
        var _a = this.props, orgSlug = _a.orgSlug, projectSlug = _a.projectSlug;
        openModal(function (deps) { return (<CustomResolutionModal {...deps} onSelected={function (statusDetails) {
                return _this.handleAnotherExistingReleaseResolution(statusDetails);
            }} orgSlug={orgSlug} projectSlug={projectSlug}/>); });
    };
    ResolveActions.prototype.render = function () {
        var _a = this.props, isResolved = _a.isResolved, onUpdate = _a.onUpdate, confirmMessage = _a.confirmMessage, shouldConfirm = _a.shouldConfirm, disabled = _a.disabled, confirmLabel = _a.confirmLabel, projectFetchError = _a.projectFetchError, hasInbox = _a.hasInbox;
        if (isResolved) {
            return this.renderResolved();
        }
        var actionLinkProps = {
            shouldConfirm: shouldConfirm,
            message: confirmMessage,
            confirmLabel: confirmLabel,
            disabled: disabled,
        };
        return (<Tooltip disabled={!projectFetchError} title={t('Error fetching project')}>
        {hasInbox ? (<div style={{ width: '100%' }}>
            <div className="dropdown-submenu flex expand-left">
              {this.renderDropdownMenu()}
            </div>
          </div>) : (<ButtonBar merged>
            <ActionLink {...actionLinkProps} type="button" title={t('Resolve')} icon={<IconCheckmark size="xs"/>} onAction={function () { return onUpdate({ status: ResolutionStatus.RESOLVED }); }}>
              {t('Resolve')}
            </ActionLink>
            {this.renderDropdownMenu()}
          </ButtonBar>)}
      </Tooltip>);
    };
    ResolveActions.defaultProps = defaultProps;
    return ResolveActions;
}(React.Component));
export default withOrganization(ResolveActions);
//# sourceMappingURL=resolve.jsx.map