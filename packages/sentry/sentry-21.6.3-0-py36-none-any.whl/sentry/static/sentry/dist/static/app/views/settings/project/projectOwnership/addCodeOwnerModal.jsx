import { __assign, __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import { Component, Fragment } from 'react';
import styled from '@emotion/styled';
import Alert from 'app/components/alert';
import Button from 'app/components/button';
import Link from 'app/components/links/link';
import LoadingIndicator from 'app/components/loadingIndicator';
import { Panel, PanelBody } from 'app/components/panels';
import { IconCheckmark, IconNot } from 'app/icons';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import { getIntegrationIcon } from 'app/utils/integrationUtil';
import withApi from 'app/utils/withApi';
import Form from 'app/views/settings/components/forms/form';
import SelectField from 'app/views/settings/components/forms/selectField';
var AddCodeOwnerModal = /** @class */ (function (_super) {
    __extends(AddCodeOwnerModal, _super);
    function AddCodeOwnerModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            codeownerFile: null,
            codeMappingId: null,
            isLoading: false,
            error: false,
            errorJSON: null,
        };
        _this.fetchFile = function (codeMappingId) { return __awaiter(_this, void 0, void 0, function () {
            var organization, data, _err_1;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        organization = this.props.organization;
                        this.setState({
                            codeMappingId: codeMappingId,
                            codeownerFile: null,
                            error: false,
                            errorJSON: null,
                            isLoading: true,
                        });
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.props.api.requestPromise("/organizations/" + organization.slug + "/code-mappings/" + codeMappingId + "/codeowners/", {
                                method: 'GET',
                            })];
                    case 2:
                        data = _a.sent();
                        this.setState({ codeownerFile: data, isLoading: false });
                        return [3 /*break*/, 4];
                    case 3:
                        _err_1 = _a.sent();
                        this.setState({ isLoading: false });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.addFile = function () { return __awaiter(_this, void 0, void 0, function () {
            var _a, organization, project, codeMappings, _b, codeownerFile, codeMappingId, data, codeMapping, _err_2;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, organization = _a.organization, project = _a.project, codeMappings = _a.codeMappings;
                        _b = this.state, codeownerFile = _b.codeownerFile, codeMappingId = _b.codeMappingId;
                        if (!codeownerFile) return [3 /*break*/, 4];
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.props.api.requestPromise("/projects/" + organization.slug + "/" + project.slug + "/codeowners/", {
                                method: 'POST',
                                data: {
                                    codeMappingId: codeMappingId,
                                    raw: codeownerFile.raw,
                                },
                            })];
                    case 2:
                        data = _c.sent();
                        codeMapping = codeMappings.find(function (mapping) { return mapping.id === (codeMappingId === null || codeMappingId === void 0 ? void 0 : codeMappingId.toString()); });
                        this.handleAddedFile(__assign(__assign({}, data), { codeMapping: codeMapping }));
                        return [3 /*break*/, 4];
                    case 3:
                        _err_2 = _c.sent();
                        this.setState({ error: true, errorJSON: _err_2.responseJSON, isLoading: false });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    AddCodeOwnerModal.prototype.handleAddedFile = function (data) {
        this.props.onSave(data);
        this.props.closeModal();
    };
    AddCodeOwnerModal.prototype.sourceFile = function (codeownerFile) {
        return (<Panel>
        <SourceFileBody>
          <IconCheckmark size="md" isCircled color="green200"/>
          {codeownerFile.filepath}
          <Button size="small" href={codeownerFile.html_url} target="_blank">
            {t('Preview File')}
          </Button>
        </SourceFileBody>
      </Panel>);
    };
    AddCodeOwnerModal.prototype.errorMessage = function (baseUrl) {
        var _a;
        var _b = this.state, errorJSON = _b.errorJSON, codeMappingId = _b.codeMappingId;
        var codeMappings = this.props.codeMappings;
        var codeMapping = codeMappings.find(function (mapping) { return mapping.id === codeMappingId; });
        var _c = codeMapping, integrationId = _c.integrationId, provider = _c.provider;
        return (<Alert type="error" icon={<IconNot size="md"/>}>
        <p>{(_a = errorJSON === null || errorJSON === void 0 ? void 0 : errorJSON.raw) === null || _a === void 0 ? void 0 : _a[0]}</p>
        {codeMapping && (<p>
            {tct('Configure [userMappingsLink:User Mappings] or [teamMappingsLink:Team Mappings] for any missing associations.', {
                    userMappingsLink: (<Link to={baseUrl + "/" + (provider === null || provider === void 0 ? void 0 : provider.key) + "/" + integrationId + "/?tab=userMappings&referrer=add-codeowners"}/>),
                    teamMappingsLink: (<Link to={baseUrl + "/" + (provider === null || provider === void 0 ? void 0 : provider.key) + "/" + integrationId + "/?tab=teamMappings&referrer=add-codeowners"}/>),
                })}
          </p>)}
      </Alert>);
    };
    AddCodeOwnerModal.prototype.noSourceFile = function () {
        var _a = this.state, codeMappingId = _a.codeMappingId, isLoading = _a.isLoading;
        if (isLoading) {
            return (<Container>
          <LoadingIndicator mini/>
        </Container>);
        }
        if (!codeMappingId) {
            return null;
        }
        return (<Panel>
        <NoSourceFileBody>
          {codeMappingId ? (<Fragment>
              <IconNot size="md" color="red200"/>
              {t('No codeowner file found.')}
            </Fragment>) : null}
        </NoSourceFileBody>
      </Panel>);
    };
    AddCodeOwnerModal.prototype.render = function () {
        var _a = this.props, Header = _a.Header, Body = _a.Body, Footer = _a.Footer;
        var _b = this.state, codeownerFile = _b.codeownerFile, error = _b.error, errorJSON = _b.errorJSON;
        var _c = this.props, codeMappings = _c.codeMappings, integrations = _c.integrations, organization = _c.organization;
        var baseUrl = "/settings/" + organization.slug + "/integrations";
        return (<Fragment>
        <Header closeButton>{t('Add Code Owner File')}</Header>
        <Body>
          {!codeMappings.length && (<Fragment>
              <div>
                {t("Configure code mapping to add your CODEOWNERS file. Select the integration you'd like to use for mapping:")}
              </div>
              <IntegrationsList>
                {integrations.map(function (integration) { return (<Button key={integration.id} type="button" to={baseUrl + "/" + integration.provider.key + "/" + integration.id + "/?tab=codeMappings&referrer=add-codeowners"}>
                    {getIntegrationIcon(integration.provider.key)}
                    <IntegrationName>{integration.name}</IntegrationName>
                  </Button>); })}
              </IntegrationsList>
            </Fragment>)}
          {codeMappings.length > 0 && (<Form apiMethod="POST" apiEndpoint="/code-mappings/" hideFooter initialData={{}}>
              <StyledSelectField name="codeMappingId" label={t('Apply an existing code mapping')} choices={codeMappings.map(function (cm) { return [
                    cm.id,
                    cm.repoName,
                ]; })} onChange={this.fetchFile} required inline={false} flexibleControlStateSize stacked/>

              <FileResult>
                {codeownerFile ? this.sourceFile(codeownerFile) : this.noSourceFile()}
                {error && errorJSON && this.errorMessage(baseUrl)}
              </FileResult>
            </Form>)}
        </Body>
        <Footer>
          <Button disabled={codeownerFile ? false : true} label={t('Add File')} priority="primary" onClick={this.addFile}>
            {t('Add File')}
          </Button>
        </Footer>
      </Fragment>);
    };
    return AddCodeOwnerModal;
}(Component));
export default withApi(AddCodeOwnerModal);
export { AddCodeOwnerModal };
var StyledSelectField = styled(SelectField)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  border-bottom: None;\n  padding-right: 16px;\n"], ["\n  border-bottom: None;\n  padding-right: 16px;\n"])));
var FileResult = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  width: inherit;\n"], ["\n  width: inherit;\n"])));
var NoSourceFileBody = styled(PanelBody)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: grid;\n  padding: 12px;\n  grid-template-columns: 30px 1fr;\n  align-items: center;\n"], ["\n  display: grid;\n  padding: 12px;\n  grid-template-columns: 30px 1fr;\n  align-items: center;\n"])));
var SourceFileBody = styled(PanelBody)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: grid;\n  padding: 12px;\n  grid-template-columns: 30px 1fr 100px;\n  align-items: center;\n"], ["\n  display: grid;\n  padding: 12px;\n  grid-template-columns: 30px 1fr 100px;\n  align-items: center;\n"])));
var IntegrationsList = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  justify-items: center;\n  margin-top: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  justify-items: center;\n  margin-top: ", ";\n"])), space(1), space(2));
var IntegrationName = styled('p')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  padding-left: 10px;\n"], ["\n  padding-left: 10px;\n"])));
var Container = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  display: flex;\n  justify-content: center;\n"], ["\n  display: flex;\n  justify-content: center;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=addCodeOwnerModal.jsx.map