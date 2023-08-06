import { __assign, __awaiter, __extends, __generator, __read, __spreadArray } from "tslib";
import { Fragment } from 'react';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import { openModal } from 'app/actionCreators/modal';
import AsyncComponent from 'app/components/asyncComponent';
import IntegrationExternalMappingForm from 'app/components/integrationExternalMappingForm';
import IntegrationExternalMappings from 'app/components/integrationExternalMappings';
import { t } from 'app/locale';
import withOrganization from 'app/utils/withOrganization';
var IntegrationExternalUserMappings = /** @class */ (function (_super) {
    __extends(IntegrationExternalUserMappings, _super);
    function IntegrationExternalUserMappings() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleDelete = function (mapping) { return __awaiter(_this, void 0, void 0, function () {
            var organization, endpoint, _a;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        organization = this.props.organization;
                        endpoint = "/organizations/" + organization.slug + "/external-users/" + mapping.id + "/";
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise(endpoint, {
                                method: 'DELETE',
                            })];
                    case 2:
                        _b.sent();
                        // remove config and update state
                        addSuccessMessage(t('Deletion successful'));
                        this.fetchData();
                        return [3 /*break*/, 4];
                    case 3:
                        _a = _b.sent();
                        // no 4xx errors should happen on delete
                        addErrorMessage(t('An error occurred'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleSubmitSuccess = function () {
            // Don't bother updating state. The info is in array of objects for each object in another array of objects.
            // Easier and less error-prone to re-fetch the data and re-calculate state.
            _this.fetchData();
        };
        _this.openModal = function (mapping) {
            var _a = _this.props, organization = _a.organization, integration = _a.integration;
            openModal(function (_a) {
                var Body = _a.Body, Header = _a.Header, closeModal = _a.closeModal;
                return (<Fragment>
        <Header closeButton>{t('Configure External User Mapping')}</Header>
        <Body>
          <IntegrationExternalMappingForm organization={organization} integration={integration} onSubmitSuccess={function () {
                        _this.handleSubmitSuccess();
                        closeModal();
                    }} mapping={mapping} sentryNamesMapper={_this.sentryNamesMapper} type="user" url={"/organizations/" + organization.slug + "/members/"} onCancel={closeModal} baseEndpoint={"/organizations/" + organization.slug + "/external-users/"}/>
        </Body>
      </Fragment>);
            });
        };
        return _this;
    }
    IntegrationExternalUserMappings.prototype.getEndpoints = function () {
        var organization = this.props.organization;
        return [
            [
                'members',
                "/organizations/" + organization.slug + "/members/",
                { query: { query: 'hasExternalUsers:true', expand: 'externalUsers' } },
            ],
        ];
    };
    Object.defineProperty(IntegrationExternalUserMappings.prototype, "mappings", {
        get: function () {
            var integration = this.props.integration;
            var members = this.state.members;
            var externalUserMappings = members.reduce(function (acc, member) {
                var externalUsers = member.externalUsers, user = member.user;
                acc.push.apply(acc, __spreadArray([], __read(externalUsers
                    .filter(function (externalUser) { return externalUser.provider === integration.provider.key; })
                    .map(function (externalUser) { return (__assign(__assign({}, externalUser), { sentryName: user.name })); }))));
                return acc;
            }, []);
            return externalUserMappings.sort(function (a, b) { return parseInt(a.id, 10) - parseInt(b.id, 10); });
        },
        enumerable: false,
        configurable: true
    });
    IntegrationExternalUserMappings.prototype.sentryNamesMapper = function (members) {
        return members
            .filter(function (member) { return member.user; })
            .map(function (_a) {
            var id = _a.user.id, email = _a.email, name = _a.name;
            var label = email !== name ? name + " - " + email : "" + email;
            return { id: id, name: label };
        });
    };
    IntegrationExternalUserMappings.prototype.renderBody = function () {
        var integration = this.props.integration;
        return (<Fragment>
        <IntegrationExternalMappings integration={integration} type="user" mappings={this.mappings} onCreateOrEdit={this.openModal} onDelete={this.handleDelete}/>
      </Fragment>);
    };
    return IntegrationExternalUserMappings;
}(AsyncComponent));
export default withOrganization(IntegrationExternalUserMappings);
//# sourceMappingURL=integrationExternalUserMappings.jsx.map