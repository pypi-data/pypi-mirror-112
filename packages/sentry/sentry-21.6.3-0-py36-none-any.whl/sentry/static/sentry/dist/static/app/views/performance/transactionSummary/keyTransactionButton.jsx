import { __extends, __read } from "tslib";
import { Component } from 'react';
import { toggleKeyTransaction } from 'app/actionCreators/performance';
import Button from 'app/components/button';
import { IconStar } from 'app/icons';
import { t } from 'app/locale';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import withApi from 'app/utils/withApi';
var KeyTransactionButton = /** @class */ (function (_super) {
    __extends(KeyTransactionButton, _super);
    function KeyTransactionButton() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isLoading: true,
            keyFetchID: undefined,
            error: null,
            isKeyTransaction: false,
        };
        _this.fetchData = function () {
            var _a = _this.props, organization = _a.organization, eventView = _a.eventView, transactionName = _a.transactionName;
            var projects = eventView.project;
            if (projects.length !== 1) {
                return;
            }
            var url = "/organizations/" + organization.slug + "/is-key-transactions/";
            var keyFetchID = Symbol('keyFetchID');
            _this.setState({ isLoading: true, keyFetchID: keyFetchID });
            _this.props.api
                .requestPromise(url, {
                method: 'GET',
                includeAllArgs: true,
                query: {
                    project: projects.map(function (id) { return String(id); }),
                    transaction: transactionName,
                },
            })
                .then(function (_a) {
                var _b = __read(_a, 3), data = _b[0], _ = _b[1], _jqXHR = _b[2];
                if (_this.state.keyFetchID !== keyFetchID) {
                    // invariant: a different request was initiated after this request
                    return;
                }
                _this.setState({
                    isLoading: false,
                    keyFetchID: undefined,
                    error: null,
                    isKeyTransaction: !!(data === null || data === void 0 ? void 0 : data.isKey),
                });
            })
                .catch(function (err) {
                var _a, _b;
                _this.setState({
                    isLoading: false,
                    keyFetchID: undefined,
                    error: (_b = (_a = err.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) !== null && _b !== void 0 ? _b : null,
                    isKeyTransaction: false,
                });
            });
        };
        _this.toggleKeyTransactionHandler = function () {
            var _a = _this.props, eventView = _a.eventView, api = _a.api, organization = _a.organization, transactionName = _a.transactionName;
            var isKeyTransaction = _this.state.isKeyTransaction;
            var projects = eventView.project.map(String);
            trackAnalyticsEvent({
                eventName: 'Performance Views: Key Transaction toggle',
                eventKey: 'performance_views.key_transaction.toggle',
                organization_id: organization.id,
                action: isKeyTransaction ? 'remove' : 'add',
            });
            toggleKeyTransaction(api, isKeyTransaction, organization.slug, projects, transactionName).then(function () {
                _this.setState({ isKeyTransaction: !isKeyTransaction });
            });
        };
        return _this;
    }
    KeyTransactionButton.prototype.componentDidMount = function () {
        this.fetchData();
    };
    KeyTransactionButton.prototype.componentDidUpdate = function (prevProps) {
        var orgSlugChanged = prevProps.organization.slug !== this.props.organization.slug;
        var projectsChanged = prevProps.eventView.project.length === 1 &&
            this.props.eventView.project.length === 1 &&
            prevProps.eventView.project[0] !== this.props.eventView.project[0];
        if (orgSlugChanged || projectsChanged) {
            this.fetchData();
        }
    };
    KeyTransactionButton.prototype.render = function () {
        var _a = this.state, isKeyTransaction = _a.isKeyTransaction, isLoading = _a.isLoading;
        if (this.props.eventView.project.length !== 1 || isLoading) {
            return null;
        }
        return (<Button icon={isKeyTransaction ? <IconStar color="yellow300" isSolid/> : <IconStar />} onClick={this.toggleKeyTransactionHandler}>
        {t('Key Transaction')}
      </Button>);
    };
    return KeyTransactionButton;
}(Component));
export default withApi(KeyTransactionButton);
//# sourceMappingURL=keyTransactionButton.jsx.map