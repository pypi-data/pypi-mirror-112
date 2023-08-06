import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import { IconNext, IconPrevious } from 'app/icons';
import { t } from 'app/locale';
var NavigationButtonGroup = function (_a) {
    var links = _a.links, _b = _a.hasNext, hasNext = _b === void 0 ? false : _b, _c = _a.hasPrevious, hasPrevious = _c === void 0 ? false : _c, className = _a.className, size = _a.size, onOldestClick = _a.onOldestClick, onOlderClick = _a.onOlderClick, onNewerClick = _a.onNewerClick, onNewestClick = _a.onNewestClick;
    return (<ButtonBar className={className} merged>
    <Button size={size} to={links[0]} disabled={!hasPrevious} label={t('Oldest')} icon={<IconPrevious size="xs"/>} onClick={onOldestClick}/>
    <Button size={size} to={links[1]} disabled={!hasPrevious} onClick={onOlderClick}>
      {t('Older')}
    </Button>
    <Button size={size} to={links[2]} disabled={!hasNext} onClick={onNewerClick}>
      {t('Newer')}
    </Button>
    <Button size={size} to={links[3]} disabled={!hasNext} label={t('Newest')} icon={<IconNext size="xs"/>} onClick={onNewestClick}/>
  </ButtonBar>);
};
export default NavigationButtonGroup;
//# sourceMappingURL=navigationButtonGroup.jsx.map