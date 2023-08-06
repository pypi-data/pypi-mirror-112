import { __awaiter, __extends, __generator } from "tslib";
import { Component, Fragment } from 'react';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import Button from 'app/components/button';
import Confirm from 'app/components/confirm';
import { IconDelete } from 'app/icons';
import { t } from 'app/locale';
import withApi from 'app/utils/withApi';
import RulesPanel from 'app/views/settings/project/projectOwnership/rulesPanel';
var CodeOwnersPanel = /** @class */ (function (_super) {
    __extends(CodeOwnersPanel, _super);
    function CodeOwnersPanel() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleDelete = function (codeowner) { return __awaiter(_this, void 0, void 0, function () {
            var _a, api, organization, project, onDelete, endpoint, _b;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, api = _a.api, organization = _a.organization, project = _a.project, onDelete = _a.onDelete;
                        endpoint = "/api/0/projects/" + organization.slug + "/" + project.slug + "/codeowners/" + codeowner.id + "/";
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise(endpoint, {
                                method: 'DELETE',
                            })];
                    case 2:
                        _c.sent();
                        onDelete(codeowner);
                        addSuccessMessage(t('Deletion successful'));
                        return [3 /*break*/, 4];
                    case 3:
                        _b = _c.sent();
                        // no 4xx errors should happen on delete
                        addErrorMessage(t('An error occurred'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    CodeOwnersPanel.prototype.render = function () {
        var _this = this;
        var codeowners = this.props.codeowners;
        return (codeowners || []).map(function (codeowner) {
            var dateUpdated = codeowner.dateUpdated, provider = codeowner.provider, repoName = codeowner.codeMapping.repoName, ownershipSyntax = codeowner.ownershipSyntax;
            return (<Fragment key={codeowner.id}>
          <RulesPanel data-test-id="codeowners-panel" type="codeowners" raw={ownershipSyntax} dateUpdated={dateUpdated} provider={provider} repoName={repoName} readOnly controls={[
                    <Confirm onConfirm={function () { return _this.handleDelete(codeowner); }} message={t('Are you sure you want to remove this CODEOWNERS file?')} key="confirm-delete">
                <Button key="delete" icon={<IconDelete size="xs"/>} size="xsmall"/>
              </Confirm>,
                ]}/>
        </Fragment>);
        });
    };
    return CodeOwnersPanel;
}(Component));
export default withApi(CodeOwnersPanel);
//# sourceMappingURL=codeowners.jsx.map