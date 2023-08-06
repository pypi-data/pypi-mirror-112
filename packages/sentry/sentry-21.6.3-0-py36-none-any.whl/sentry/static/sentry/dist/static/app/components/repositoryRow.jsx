import { __extends, __makeTemplateObject } from "tslib";
import { Component, Fragment } from 'react';
import styled from '@emotion/styled';
import { cancelDeleteRepository, deleteRepository } from 'app/actionCreators/integrations';
import { openModal } from 'app/actionCreators/modal';
import Access from 'app/components/acl/access';
import Button from 'app/components/button';
import Confirm from 'app/components/confirm';
import ExternalLink from 'app/components/links/externalLink';
import { PanelItem } from 'app/components/panels';
import RepositoryEditForm from 'app/components/repositoryEditForm';
import Tooltip from 'app/components/tooltip';
import { IconDelete, IconEdit } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { RepositoryStatus } from 'app/types';
import withOrganization from 'app/utils/withOrganization';
var RepositoryRow = /** @class */ (function (_super) {
    __extends(RepositoryRow, _super);
    function RepositoryRow() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.cancelDelete = function () {
            var _a = _this.props, api = _a.api, orgId = _a.orgId, repository = _a.repository, onRepositoryChange = _a.onRepositoryChange;
            cancelDeleteRepository(api, orgId, repository.id).then(function (data) {
                if (onRepositoryChange) {
                    onRepositoryChange(data);
                }
            }, function () { });
        };
        _this.deleteRepo = function () {
            var _a = _this.props, api = _a.api, orgId = _a.orgId, repository = _a.repository, onRepositoryChange = _a.onRepositoryChange;
            deleteRepository(api, orgId, repository.id).then(function (data) {
                if (onRepositoryChange) {
                    onRepositoryChange(data);
                }
            }, function () { });
        };
        _this.handleEditRepo = function (data) {
            var onRepositoryChange = _this.props.onRepositoryChange;
            if (onRepositoryChange) {
                onRepositoryChange(data);
            }
        };
        _this.openModal = function () {
            var _a = _this.props, repository = _a.repository, orgId = _a.orgId;
            openModal(function (_a) {
                var Body = _a.Body, Header = _a.Header, closeModal = _a.closeModal;
                return (<Fragment>
        <Header closeButton>{t('Edit Repository')}</Header>
        <Body>
          <RepositoryEditForm orgSlug={orgId} repository={repository} onSubmitSuccess={_this.handleEditRepo} closeModal={closeModal} onCancel={closeModal}/>
        </Body>
      </Fragment>);
            });
        };
        return _this;
    }
    RepositoryRow.prototype.getStatusLabel = function (repo) {
        switch (repo.status) {
            case RepositoryStatus.PENDING_DELETION:
                return 'Deletion Queued';
            case RepositoryStatus.DELETION_IN_PROGRESS:
                return 'Deletion in Progress';
            case RepositoryStatus.DISABLED:
                return 'Disabled';
            case RepositoryStatus.HIDDEN:
                return 'Disabled';
            default:
                return null;
        }
    };
    Object.defineProperty(RepositoryRow.prototype, "isActive", {
        get: function () {
            return this.props.repository.status === RepositoryStatus.ACTIVE;
        },
        enumerable: false,
        configurable: true
    });
    RepositoryRow.prototype.renderDeleteButton = function (hasAccess) {
        var repository = this.props.repository;
        var isActive = this.isActive;
        return (<Tooltip title={t('You must be an organization owner, manager or admin to remove a repository.')} disabled={hasAccess}>
        <Confirm disabled={!hasAccess || (!isActive && repository.status !== RepositoryStatus.DISABLED)} onConfirm={this.deleteRepo} message={t('Are you sure you want to remove this repository? All associated commit data will be removed in addition to the repository.')}>
          <StyledButton size="xsmall" icon={<IconDelete size="xs"/>} label={t('delete')} disabled={!hasAccess}/>
        </Confirm>
      </Tooltip>);
    };
    RepositoryRow.prototype.render = function () {
        var _this = this;
        var _a = this.props, repository = _a.repository, showProvider = _a.showProvider, organization = _a.organization;
        var isActive = this.isActive;
        var isCustomRepo = organization.features.includes('integrations-custom-scm') &&
            repository.provider.id === 'integrations:custom_scm';
        return (<Access access={['org:integrations']}>
        {function (_a) {
                var hasAccess = _a.hasAccess;
                return (<StyledPanelItem status={repository.status}>
            <RepositoryTitleAndUrl>
              <RepositoryTitle>
                <strong>{repository.name}</strong>
                {!isActive && <small> &mdash; {_this.getStatusLabel(repository)}</small>}
                {repository.status === RepositoryStatus.PENDING_DELETION && (<StyledButton size="xsmall" onClick={_this.cancelDelete} disabled={!hasAccess} data-test-id="repo-cancel">
                    {t('Cancel')}
                  </StyledButton>)}
              </RepositoryTitle>
              <div>
                {showProvider && <small>{repository.provider.name}</small>}
                {showProvider && repository.url && <span>&nbsp;&mdash;&nbsp;</span>}
                {repository.url && (<small>
                    <ExternalLink href={repository.url}>
                      {repository.url.replace('https://', '')}
                    </ExternalLink>
                  </small>)}
              </div>
            </RepositoryTitleAndUrl>
            {isCustomRepo ? (<EditAndDelete>
                <StyledButton size="xsmall" icon={<IconEdit size="xs"/>} label={t('edit')} disabled={!hasAccess ||
                            (!isActive && repository.status !== RepositoryStatus.DISABLED)} onClick={function () { return _this.openModal(); }}/>
                {_this.renderDeleteButton(hasAccess)}
              </EditAndDelete>) : (_this.renderDeleteButton(hasAccess))}
          </StyledPanelItem>);
            }}
      </Access>);
    };
    RepositoryRow.defaultProps = {
        showProvider: false,
    };
    return RepositoryRow;
}(Component));
var StyledPanelItem = styled(PanelItem)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  /* shorter top padding because of title lineheight */\n  padding: ", " ", " ", ";\n  justify-content: space-between;\n  align-items: center;\n  flex: 1;\n\n  ", ";\n\n  &:last-child {\n    border-bottom: none;\n  }\n"], ["\n  /* shorter top padding because of title lineheight */\n  padding: ", " ", " ", ";\n  justify-content: space-between;\n  align-items: center;\n  flex: 1;\n\n  ", ";\n\n  &:last-child {\n    border-bottom: none;\n  }\n"])), space(1), space(2), space(2), function (p) {
    return p.status === RepositoryStatus.DISABLED &&
        "\n    filter: grayscale(1);\n    opacity: 0.4;\n  ";
});
var StyledButton = styled(Button)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space(1));
var RepositoryTitleAndUrl = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n"], ["\n  display: flex;\n  flex-direction: column;\n"])));
var EditAndDelete = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n  margin-left: ", ";\n"], ["\n  display: flex;\n  margin-left: ", ";\n"])), space(1));
var RepositoryTitle = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  margin-bottom: ", ";\n  /* accommodate cancel button height */\n  line-height: 26px;\n"], ["\n  margin-bottom: ", ";\n  /* accommodate cancel button height */\n  line-height: 26px;\n"])), space(1));
export default withOrganization(RepositoryRow);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=repositoryRow.jsx.map