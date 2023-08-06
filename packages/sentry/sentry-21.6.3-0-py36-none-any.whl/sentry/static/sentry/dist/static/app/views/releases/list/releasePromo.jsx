import { __extends, __makeTemplateObject } from "tslib";
import { Component } from 'react';
import styled from '@emotion/styled';
import emptyStateImg from 'sentry-images/spot/releases-empty-state.svg';
import commitImage from 'sentry-images/spot/releases-tour-commits.svg';
import emailImage from 'sentry-images/spot/releases-tour-email.svg';
import resolutionImage from 'sentry-images/spot/releases-tour-resolution.svg';
import statsImage from 'sentry-images/spot/releases-tour-stats.svg';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import FeatureTourModal, { TourImage, TourText, } from 'app/components/modals/featureTourModal';
import OnboardingPanel from 'app/components/onboardingPanel';
import { t } from 'app/locale';
import { trackAnalyticsEvent } from 'app/utils/analytics';
var releasesSetupUrl = 'https://docs.sentry.io/product/releases/';
var docsLink = (<Button external href={releasesSetupUrl}>
    {t('Setup')}
  </Button>);
export var RELEASES_TOUR_STEPS = [
    {
        title: t('Suspect Commits'),
        image: <TourImage src={commitImage}/>,
        body: (<TourText>
        {t('Sentry suggests which commit caused an issue and who is likely responsible so you can triage.')}
      </TourText>),
        actions: docsLink,
    },
    {
        title: t('Release Stats'),
        image: <TourImage src={statsImage}/>,
        body: (<TourText>
        {t('Get an overview of the commits in each release, and which issues were introduced or fixed.')}
      </TourText>),
        actions: docsLink,
    },
    {
        title: t('Easily Resolve'),
        image: <TourImage src={resolutionImage}/>,
        body: (<TourText>
        {t('Automatically resolve issues by including the issue number in your commit message.')}
      </TourText>),
        actions: docsLink,
    },
    {
        title: t('Deploy Emails'),
        image: <TourImage src={emailImage}/>,
        body: (<TourText>
        {t('Receive email notifications about when your code gets deployed. This can be customized in settings.')}
      </TourText>),
    },
];
var ReleasePromo = /** @class */ (function (_super) {
    __extends(ReleasePromo, _super);
    function ReleasePromo() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleTourAdvance = function (step, duration) {
            var _a = _this.props, organization = _a.organization, projectId = _a.projectId;
            trackAnalyticsEvent({
                eventKey: 'releases.tour.advance',
                eventName: 'Releases: Tour Advance',
                organization_id: parseInt(organization.id, 10),
                project_id: projectId,
                step: step,
                duration: duration,
            });
        };
        _this.handleClose = function (step, duration) {
            var _a = _this.props, organization = _a.organization, projectId = _a.projectId;
            trackAnalyticsEvent({
                eventKey: 'releases.tour.close',
                eventName: 'Releases: Tour Close',
                organization_id: parseInt(organization.id, 10),
                project_id: projectId,
                step: step,
                duration: duration,
            });
        };
        return _this;
    }
    ReleasePromo.prototype.componentDidMount = function () {
        var _a = this.props, organization = _a.organization, projectId = _a.projectId;
        trackAnalyticsEvent({
            eventKey: 'releases.landing_card_viewed',
            eventName: 'Releases: Landing Card Viewed',
            organization_id: parseInt(organization.id, 10),
            project_id: projectId,
        });
    };
    ReleasePromo.prototype.render = function () {
        return (<OnboardingPanel image={<img src={emptyStateImg}/>}>
        <h3>{t('Demystify Releases')}</h3>
        <p>
          {t('Did you know how many errors your latest release triggered? We do. And more, too.')}
        </p>
        <ButtonList gap={1}>
          <FeatureTourModal steps={RELEASES_TOUR_STEPS} onAdvance={this.handleTourAdvance} onCloseModal={this.handleClose} doneText={t('Start Setup')} doneUrl={releasesSetupUrl}>
            {function (_a) {
                var showModal = _a.showModal;
                return (<Button priority="default" onClick={showModal}>
                {t('Take a Tour')}
              </Button>);
            }}
          </FeatureTourModal>
          <Button priority="primary" href={releasesSetupUrl} external>
            {t('Start Setup')}
          </Button>
        </ButtonList>
      </OnboardingPanel>);
    };
    return ReleasePromo;
}(Component));
var ButtonList = styled(ButtonBar)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  grid-template-columns: repeat(auto-fit, minmax(130px, max-content));\n"], ["\n  grid-template-columns: repeat(auto-fit, minmax(130px, max-content));\n"])));
export default ReleasePromo;
var templateObject_1;
//# sourceMappingURL=releasePromo.jsx.map