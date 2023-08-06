import { mountWithTheme } from 'sentry-test/enzyme';
import Banner from 'app/components/banner';
describe('Banner', function () {
    it('can be dismissed', function () {
        var banner = mountWithTheme(<Banner dismissKey="test"/>);
        expect(banner.find('BannerWrapper').exists()).toBe(true);
        banner.find('CloseButton').simulate('click');
        expect(banner.find('BannerWrapper').exists()).toBe(false);
        expect(localStorage.getItem('test-banner-dismissed')).toBe('true');
    });
    it('is not dismissable', function () {
        var banner = mountWithTheme(<Banner isDismissable={false}/>);
        expect(banner.find('CloseButton').exists()).toBe(false);
    });
});
//# sourceMappingURL=banner.spec.jsx.map